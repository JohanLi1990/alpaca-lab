# alpaca-lab

Repository to practice common rule-based strategies.

## Run Modes

Activate the project environment first:

```bash
conda activate strategy-lab
```

## Account Profiles

This repository uses two Alpaca paper-account credential profiles:
- `v1`: momentum strategy (live weekly rebalance)
- `v2`: PEAD strategy (live daily cronjob)

Data-layer calls default to profile `v1`, which keeps backtests and data-only workflows on V1 unless a call site explicitly passes another profile.

Copy `.env.example` to `.env` and set profile credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `V1_APCA_API_KEY_ID`
- `V1_APCA_API_SECRET_KEY`
- `V2_APCA_API_KEY_ID`
- `V2_APCA_API_SECRET_KEY`

Migration note:
- Previous V2 key name `V2_APCA_API_KEY` has been replaced by `V2_APCA_API_KEY_ID`.

- Backtest:

```bash
python run.py --mode backtest
```

- Live paper rebalance (one-shot):

```bash
python run.py --mode live
```

- Live paper rebalance with max deployable capital cap:

```bash
python run.py --mode live --capital-cap 30000
```

- PEAD ML backtest (GOOGL earnings gap prediction):

```bash
python run.py --mode pead-backtest
```

This mode runs the full pipeline:
1. Fetch earnings events from yfinance
2. Fetch daily bars from Alpaca (GOOGL + QQQ)
3. Build pre-earnings features using the configured entry offset
4. Run walk-forward classification
5. Backtest event-driven entries/exits

Logs are written to `output/pead_backtest_*.log`.

PEAD timing is configurable via `config.PEAD_ENTRY_OFFSET_DAYS`.
- Default: `3`, which means enter at `T-3 open`
- Derived feature anchor: `T-(E+1)` close, so the default feature window is `T-10..T-4`
- Exit timing remains controlled by `config.PEAD_EXIT_MODE`

- PEAD live paper trading (multi-symbol daily cronjob):

```bash
python run.py --mode pead-live
```

This mode runs live paper trading execution for configured symbols (NXPI, AMD, AVGO):
1. Fetch nearest earnings dates for each symbol
2. Check if today is the configured entry day `T-E` or an exit day `T+1+`
3. If today is `T-E`, build features only from bars available through `T-(E+1)` close and evaluate the classifier
4. If T+1+ and position is open: place SELL order (at market price)
5. Log all trades to CSV, track state in JSON file
6. Auto-cleanup stale positions after 30 days

Logs are written to `output/pead_live_*.log`.
State file: `output/pead_live_state.json` (tracks open positions per symbol)
Trade log: `output/pead_live_trades.csv` (permanent audit trail)

### PEAD Daily Automation (DigitalOcean Droplet)

Set up a weekday cronjob to run PEAD live in a New York pre-open window.

Recommended execution window:
- Run between `9:20 AM` and `9:28 AM` America/New_York time
- This is after `T-4` has fully closed and before `T-3` regular session starts
- A single run at `9:25 AM ET` is a practical default

Example crontab entry (DST-safe via `CRON_TZ`):

```cron
CRON_TZ=America/New_York
25 9 * * 1-5 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python run.py --mode pead-live >> output/pead_live.log 2>&1
```

**Timing rationale:**
- Running in an ET-defined window prevents timezone drift when the server is in Singapore or UTC
- Supports offset-driven entry-at-open logic because the signal only uses bars available by `T-(E+1)` close
- If today is `T-3` and the run happens after the US close, skip entry and wait for the next valid event (do not force late execution)
- For T+1 exits, if cronjob runs before market close, position is exited at market open
- If cronjob misses T+1 (droplet down), position exits on T+2 when cronjob runs next (handles recovery)

**Testing alternate entry offsets:**
- Default config-driven run: set `PEAD_ENTRY_OFFSET_DAYS` in `config.py`, then run `python run.py --mode pead-backtest`
- One-off alternate offset without editing config permanently:

```bash
conda run -n strategy-lab python -c "import config; config.PEAD_ENTRY_OFFSET_DAYS = 4; import run; run.run_pead_backtest()"
```

- Typical interpretations:
	- `3` => enter at `T-3 open`, feature window ends at `T-4 close`
	- `4` => enter at `T-4 open`, feature window ends at `T-5 close`
	- `5` => enter at `T-5 open`, feature window ends at `T-6 close`

**Migration note:**
- PEAD results produced before this timing change used different entry/feature semantics and are not directly comparable to current runs.

**State file and trade log:**
- State file persists open positions across cronjob runs
- Idempotency check prevents double-trading the same symbol/earnings-event pair
- Trade log is append-only for permanent audit trail
- Auto-cleanup removes stale entries after 30 days

## Weekly Automation (DigitalOcean Droplet)

Comprehensive backtest analysis (2016–2025) reveals **PEAD signal is highly sector-specific**, with semiconductors significantly outperforming mega-cap tech:

#### Semiconductor Universe (6 tested symbols)

| Symbol | Type | Events | Hit Rate | Avg Return | Sharpe | Uplift vs Always-Buy | Signal |
|--------|------|--------|----------|------------|--------|----------------------|--------|
| **NXPI** | Auto/Analog | 16 | 92.31% | 2.66% | 0.87 | **+1.56%** | 🟢 Strongest |
| **AMD** | Processor | 19 | 75.00% | 4.72% | 0.56 | **+1.90%** | 🟢 Excellent |
| **AVGO** | Broadband | 18 | 70.00% | 4.84% | 0.45 | **+1.32%** | 🟢 Excellent |
| **MU** | Memory | 20 | 62.50% | 2.48% | 0.26 | **+0.60%** | 🟡 Good |
| **QCOM** | Mobile SoC | 17 | 42.86% | 0.06% | 0.01 | **+0.78%** | 🟡 Marginal |
| **INTC** | Processor | 18 | 41.67% | -1.23% | -0.19 | **+1.05%** | 🟡 Paradoxical* |

*INTC shows negative returns but still beats always-buy because underlying earnings gap is weaker.

#### Mega-Cap Tech (7 tested symbols)

| Symbol | Events | Hit Rate | Avg Return | Sharpe | Uplift vs Always-Buy | Signal |
|--------|--------|----------|------------|--------|----------------------|--------|
| **GOOGL** | 20 | 56.25% | 1.23% | 0.59 | **+1.03%** | ✓ Only winner |
| **NVDA** | 20 | 60.00% | 2.56% | 0.31 | -0.58% | ✗ |
| **MSFT** | 19 | 52.63% | 2.01% | 0.31 | -0.14% | ✗ |
| **META** | 20 | 56.25% | 1.23% | 0.11 | -0.44% | ✗ |
| **AMZN** | 19 | 47.06% | 0.87% | 0.07 | -0.02% | ✗ |
| **AAPL** | 14 | 50.00% | 0.34% | 0.07 | -0.09% | ✗ |
| **ORCL** | 8 | 37.50% | -0.79% | -0.07 | -3.61% | ✗ Worst |

#### Key Insights

- **Semiconductors dominate**: 6/6 tested show positive uplift vs always-buy (avg +1.04%); mega-caps only 1/7 (avg -0.27%)
- **Highest hit rates in semicon**: NXPI (92%), AMD (75%), AVGO (70%) vs mega-cap range (37–60%)
- **Better risk-adjusted returns**: Semiconductor Sharpe ratios (0.26–0.87) exceed mega-cap tech (0.01–0.59)
- **Sector cyclicality matters**: PEAD drift patterns are predictable in cyclical semicon segment but noise-dominated in mega-cap tech
- **Recommendation**: Focus PEAD portfolio on **NXPI, AMD, AVGO** for highest signal quality and consistent alpha

#### Testing Methodology

- **Entry**: Configurable `T-E open` (default `T-3 open`)
- **Feature window**: 7 trading days ending at `T-(E+1)` close (default `T-10..T-4`)
- **Exit**: T+1 open (next trading day open post-earnings)
- **ML Model**: Walk-forward logistic regression (7-day momentum, volatility, QQQ drift features)
- **Training seed**: Minimum 20 events per stock
- **Transaction costs**: 0.1% per leg
- **Benchmark**: Always-buy comparison on evaluated events

#### Failed Symbols

- **TSM**: Only 7 AMC events in history (below 20-event minimum for training)
- **ADI**: No AMC earnings call data available

## Weekly Automation (DigitalOcean Droplet)

Use the weekly runner:

```bash
python scripts/weekly_live_rebalance.py
```

It includes a Monday-only UTC safety check. If the script is triggered on a non-Monday UTC day, it exits without placing orders.

Optional capital cap:

```bash
python scripts/weekly_live_rebalance.py --capital-cap 30000
```

Alpaca data fetch resilience (used by weekly rebalance bar queries):

- Retries transient connection/timeout errors
- Default policy: `10` retries with `60s` delay between retries
- Worst-case added wait before hard failure: about `10` minutes
- Runtime banner in `output/live_rebalance.log` prints active retry settings each run

Environment overrides:

```bash
export APCA_DATA_RETRY_COUNT=10
export APCA_DATA_RETRY_DELAY_SEC=60
```

Example crontab entry (every Monday pre-close, 3:45 PM ET — 5-min buffer before Alpaca MOC cutoff):

```cron
CRON_TZ=America/New_York
45 15 * * 1 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_rebalance.log 2>&1
```

This timing submits Market-on-Close (MOC) orders, aligning live execution with the closing price the backtest assumes. 3:45 PM ET is DST-safe when paired with `CRON_TZ=America/New_York` and provides a 5-minute buffer before the NYSE MOC cutoff (3:50 PM ET).
