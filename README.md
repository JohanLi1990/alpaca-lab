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

Example crontab entry (every Monday regular session, 14:35 UTC):

```cron
35 14 * * 1 cd /home/chenyang/Git/alpaca-lab && /home/chenyang/miniconda3/envs/strategy-lab/bin/python scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_rebalance.log 2>&1
```

This timing is a conservative regular-hours choice across DST changes and avoids pre-market execution.
