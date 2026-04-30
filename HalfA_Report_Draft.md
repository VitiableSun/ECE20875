# Mini Project Report Draft - Half A

Name 1 (Leader): [Name]
Purdue username 1: [Purdue username]

Name 2: [Name]
Purdue username 2: [Purdue username]

Path chosen (1, 2, or 3): 2

## Dataset Description

This project uses `nyc_bicycle_counts_2016.csv`, which contains daily bicycle traffic counts in New York City from April 1, 2016 through October 31, 2016. Each row represents one day. The dataset has 214 rows and 10 columns: `Date`, `Day`, `High Temp`, `Low Temp`, `Precipitation`, `Brooklyn Bridge`, `Manhattan Bridge`, `Williamsburg Bridge`, `Queensboro Bridge`, and `Total`.

The weather columns describe the daily high temperature, low temperature, and precipitation accumulation. The four bridge columns record bicycle traffic on the Brooklyn, Manhattan, Williamsburg, and Queensboro bridges. `Total` is the combined bicycle traffic across all four bridges for that day. The bridge count columns and `Total` were stored with comma formatting, so those five columns were cleaned by removing commas and converting the values to numeric form. After conversion, the code checks whether any missing values remain and drops rows with missing count values if needed.

## Methods and Analyses

For Question 1, I used linear regression to determine which three bridges should receive sensors if the goal is to estimate total bicycle traffic across all four bridges. The target variable was `Total`, and each model used three of the four bridge count columns as input features. I evaluated all four possible three-bridge subsets by dropping one bridge at a time. Each model used an 80/20 train/test split with `random_state=42`, and the models were compared using test-set R^2 and mean squared error. Linear regression is appropriate here because `Total` is a continuous variable and is directly related to the sum of the individual bridge counts. I expected the least useful bridge to be the one whose information was either lower in volume or most redundant with the other bridge counts.

For Question 2, I used linear regression to test whether weather forecast variables could predict total daily bicycle traffic. The input features were `High Temp`, `Low Temp`, and `Precipitation`, and the target variable was `Total`. The model used an 80/20 train/test split with `random_state=42`. I evaluated the model using R^2, mean squared error, and root mean squared error, and I inspected the fitted coefficients to understand the direction of each weather effect. I expected warmer temperatures to increase predicted ridership and precipitation to decrease predicted ridership.

## Results

For Question 1, the script prints the R^2 and mean squared error for each possible three-bridge subset, then recommends the subset with the highest test-set R^2. Based on the implemented analysis, the report should use the printed recommendation from `MiniProjectPath2.py` after the script is run in an environment with the required dependencies.

For Question 2, the script prints the fitted weather model coefficients, intercept, R^2, mean squared error, and root mean squared error. It also saves a predicted-vs-actual plot as `q2_predicted_vs_actual.png`, with predicted total bicycle traffic on the x-axis and actual total bicycle traffic on the y-axis. If the model has a low R^2, that would suggest weather alone is not enough for reliable police deployment planning because the model ignores day-of-week effects, special events, commuting patterns, and seasonal changes within the April-to-October period.
