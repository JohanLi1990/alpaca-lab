## ADDED Requirements

### Requirement: Walk-forward event-level cross-validation
The ML classifier module SHALL train and evaluate using a strictly chronological, expanding-window walk-forward protocol. Events MUST be sorted by `earnings_date` before splitting. Random shuffling is prohibited.

#### Scenario: Walk-forward produces one prediction per test event
- **WHEN** `walk_forward_predict(features_df, min_train=20)` is called
- **THEN** the function returns a Series of predicted probabilities indexed by `earnings_date`, with one prediction per event from position `min_train` onward

#### Scenario: No future data leaks into training
- **WHEN** predicting the probability for event at index N
- **THEN** only events at indices 0 through N-1 are used for training

#### Scenario: Insufficient training data skips prediction
- **WHEN** fewer than `min_train` events precede the current event
- **THEN** no prediction is made for that event and it is excluded from evaluation

### Requirement: Logistic regression as Phase 1 baseline model
The module SHALL use `sklearn.linear_model.LogisticRegression` with standardized features (`sklearn.preprocessing.StandardScaler` fit on training fold only) as the primary classifier. Scaler MUST be fit exclusively on training data and applied to test data without re-fitting.

#### Scenario: Scaler fit on training fold only
- **WHEN** walk-forward prediction is run for fold N
- **THEN** the StandardScaler is fit on events 0..N-1 and applied (not re-fit) to event N

#### Scenario: Model coefficients logged per fold
- **WHEN** verbose mode is enabled
- **THEN** feature names and their logistic regression coefficients are logged after each fold fit

### Requirement: Prediction output includes probability and binary label
The module SHALL return both predicted probability (`prob_positive`) and thresholded binary label (`pred_label`) for each test event. Default threshold is 0.5; configurable via parameter.

#### Scenario: Probability output is in [0, 1]
- **WHEN** `walk_forward_predict` returns predictions
- **THEN** all `prob_positive` values are between 0.0 and 1.0 inclusive

#### Scenario: Custom threshold applied
- **WHEN** `threshold=0.60` is passed
- **THEN** `pred_label = 1` only for events where `prob_positive >= 0.60`

### Requirement: Evaluation report with hit rate, expectancy, and calibration
The module SHALL compute and return an evaluation report covering:

- `hit_rate`: Fraction of predicted positive events where `y == 1`.
- `baseline_rate`: Unconditional fraction of positive-gap events in the full sample.
- `avg_gap_return`: Mean `gap_return` across all predicted-positive events.
- `avg_gap_return_negative`: Mean `gap_return` across predicted-negative events (for comparison).
- `n_trades`: Count of events where `pred_label == 1`.
- `n_total`: Total events evaluated.

#### Scenario: Hit rate exceeds baseline rate to indicate edge
- **WHEN** the classifier has predictive power
- **THEN** `hit_rate > baseline_rate`

#### Scenario: Evaluation report prints to log
- **WHEN** `print_eval_report(report)` is called
- **THEN** all metrics are printed with labels to stdout

### Requirement: Feature importance logging for logistic regression
The module SHALL log sorted feature coefficients (by absolute magnitude) after fitting on the full training set, to validate whether the pre-earnings flow hypothesis is reflected in the model weights.

#### Scenario: Top features logged
- **WHEN** the final fold is fit
- **THEN** feature names ranked by absolute coefficient magnitude are logged in descending order
