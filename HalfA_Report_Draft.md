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

For Question 1, the best-performing three-bridge subset was Brooklyn Bridge, Manhattan Bridge, and Williamsburg Bridge, which means Queensboro Bridge was the best bridge to leave out. The test-set results were:

| Bridges used | Bridge dropped | R^2 | MSE |
| --- | --- | ---: | ---: |
| Manhattan Bridge, Williamsburg Bridge, Queensboro Bridge | Brooklyn Bridge | 0.983056 | 697676.76 |
| Brooklyn Bridge, Williamsburg Bridge, Queensboro Bridge | Manhattan Bridge | 0.985601 | 592865.58 |
| Brooklyn Bridge, Manhattan Bridge, Queensboro Bridge | Williamsburg Bridge | 0.995999 | 164725.04 |
| Brooklyn Bridge, Manhattan Bridge, Williamsburg Bridge | Queensboro Bridge | 0.997635 | 97363.42 |

The recommended sensor placement is Brooklyn Bridge, Manhattan Bridge, and Williamsburg Bridge. This subset had the highest R^2 and lowest MSE among the four tested subsets, so it gave the most accurate test-set prediction of total bridge traffic. The best model had coefficients of 1.193464 for Brooklyn Bridge, 0.942880 for Manhattan Bridge, and 1.592113 for Williamsburg Bridge, with an intercept of 360.055795.

For Question 2, the fitted weather model had coefficients of 380.087778 for `High Temp`, -177.041748 for `Low Temp`, and -8681.587256 for `Precipitation`, with an intercept of 1896.017071. The test-set R^2 was 0.575017, the MSE was 17498379.32, and the RMSE was 4183.11. The positive high-temperature coefficient and negative precipitation coefficient match the expectation that warmer days increase ridership and rainy days reduce ridership. However, the moderate R^2 suggests weather alone is not enough for highly reliable police deployment planning because the model ignores day-of-week effects, special events, commuting patterns, and seasonal changes within the April-to-October period. The predicted-vs-actual plot is saved as `q2_predicted_vs_actual.png`.
