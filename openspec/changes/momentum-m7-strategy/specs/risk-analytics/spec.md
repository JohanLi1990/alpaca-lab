## ADDED Requirements

### Requirement: Compute annualized Sharpe ratio from equity curve
The risk module SHALL compute the annualized Sharpe ratio from a weekly equity curve using the formula: `mean(weekly_returns) / std(weekly_returns) * sqrt(52)`, assuming risk-free rate of 0.

#### Scenario: Sharpe ratio computed correctly
- **WHEN** `sharpe_ratio(equity_curve, periods_per_year=52)` is called with a pandas Series of weekly portfolio values
- **THEN** it returns a float representing the annualized Sharpe ratio

#### Scenario: Flat equity curve returns zero Sharpe
- **WHEN** all equity values are equal (zero volatility)
- **THEN** the function returns 0.0 (not NaN or error)

### Requirement: Compute maximum drawdown
The risk module SHALL compute maximum drawdown as the largest peak-to-trough decline in the equity curve, expressed as a percentage: `(trough - peak) / peak * 100`.

#### Scenario: Maximum drawdown computed
- **WHEN** `max_drawdown(equity_curve)` is called
- **THEN** it returns a negative float representing the worst percentage decline from any peak

#### Scenario: Always-rising equity has zero drawdown
- **WHEN** the equity curve is monotonically increasing
- **THEN** `max_drawdown` returns 0.0

### Requirement: Compute Calmar ratio
The risk module SHALL compute the Calmar ratio as `annualized_return / abs(max_drawdown)`, where annualized return is `(final_value / initial_value) ^ (periods_per_year / n_periods) - 1`.

#### Scenario: Calmar ratio computed
- **WHEN** `calmar_ratio(equity_curve, periods_per_year=52)` is called
- **THEN** it returns a positive float when the strategy is profitable

### Requirement: Print risk summary
The risk module SHALL provide a `print_summary(equity_curve)` function that prints Sharpe ratio, maximum drawdown, Calmar ratio, total return (%), and number of periods to stdout.

#### Scenario: Summary printed after backtest
- **WHEN** `print_summary(equity_curve)` is called
- **THEN** all four metrics are printed with labels and rounded to 2 decimal places

### Requirement: Plot equity curve
The risk module SHALL provide a `plot_equity_curve(equity_curve, title)` function that renders a matplotlib line chart of portfolio value over time.

#### Scenario: Plot generated without error
- **WHEN** `plot_equity_curve(equity_curve, title="M7 Momentum")` is called
- **THEN** a matplotlib figure is created and displayed (or saved if a path is provided)
