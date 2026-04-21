# alpaca-lab

Repository to practice common rule-based strategies.

## Run Modes

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

Example crontab entry (every Monday pre-close, 19:45 UTC / 2:45 PM ET — 5-min buffer before Alpaca MOC cutoff):

```cron
45 19 * * 1 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_rebalance.log 2>&1
```

This timing submits Market-on-Close (MOC) orders, aligning live execution with the closing price the backtest assumes. 19:45 UTC is DST-safe and provides a 5-minute buffer before the NYSE MOC cutoff (19:50 UTC).
