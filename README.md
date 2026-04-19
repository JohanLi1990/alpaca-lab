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

Example crontab entry (every Monday pre-market, 13:00 UTC):

```cron
0 13 * * 1 cd /home/chenyang/Git/alpaca-lab && /usr/bin/python3 scripts/weekly_live_rebalance.py --capital-cap 30000 >> output/live_weekly.log 2>&1
```

Pick a time that matches your desired session timing.
