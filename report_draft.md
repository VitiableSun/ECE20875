# Mini Project Report

## Team Information

Name 1 (Leader): [Name]
Purdue username 1: [Purdue username]

Name 2: [Name]
Purdue username 2: [Purdue username]

Path: 2

---

## Dataset Description

This project uses `nyc_bicycle_counts_2016.csv`, which contains daily bicycle traffic counts in New York City from April 1, 2016 through October 31, 2016. Each row represents one day. The dataset has 214 rows and 10 columns: `Date`, `Day`, `High Temp`, `Low Temp`, `Precipitation`, `Brooklyn Bridge`, `Manhattan Bridge`, `Williamsburg Bridge`, `Queensboro Bridge`, and `Total`.

The weather columns describe the daily high temperature, low temperature, and precipitation accumulation. The four bridge columns record bicycle traffic on the Brooklyn, Manhattan, Williamsburg, and Queensboro bridges. `Total` is the combined bicycle traffic across all four bridges for that day. The bridge count columns and `Total` were stored with comma formatting, so those five columns were cleaned by removing commas and converting the values to numeric form. After conversion, the code checks whether any missing values remain and drops rows with missing count values if needed.

---

## Methods

**Question 1**

To determine which three bridges should receive sensors, I used linear regression to predict total bicycle traffic from a subset of three bridge counts. The target variable was `Total`, and each model used three of the four bridge count columns as features. I evaluated all four possible three-bridge subsets by dropping one bridge at a time and fitting a separate model for each. Each model used an 80/20 train/test split with `random_state=42`, and I compared models using test-set R² and mean squared error (MSE). Linear regression is appropriate here because `Total` is a continuous variable and is directly related to the sum of the individual bridge counts, so a linear relationship is a reasonable assumption. I expected the least useful bridge to be the one whose traffic volume was lowest or most redundant relative to the other three.

**Question 2**

To test whether next-day weather forecasts could predict total ridership, I used linear regression with `High Temp`, `Low Temp`, and `Precipitation` as input features and `Total` as the target variable. The model used an 80/20 train/test split with `random_state=42`. I evaluated performance using R², MSE, and RMSE, and I examined the fitted coefficients to see whether the direction of each weather effect matched intuition. I expected higher temperatures to be associated with higher ridership and greater precipitation to reduce ridership. Linear regression was chosen because the relationship between temperature and outdoor activity is plausibly linear over the range covered in this dataset, and the coefficients offer a direct interpretation of each weather variable's effect.

**Question 3**

For Part A, I analyzed weekly traffic patterns by grouping the dataset by day of the week and computing the mean total bicycle traffic for each day. I then plotted these averages as a bar chart with days ordered Monday through Sunday. This approach directly addresses the question of whether there are consistent day-of-week patterns and makes any weekday versus weekend difference immediately visible.

For Part B, I built four classifiers — Logistic Regression, K-Nearest Neighbors, Decision Tree, and Random Forest — to predict the day of the week (Monday through Sunday, encoded as integers 0 through 6) from the four bridge counts. Using the four bridge columns as features captures the total shape of a given day's traffic across the city. I tested all four classifiers so their accuracy could be compared directly, and I used an 80/20 train/test split with `random_state=42` for consistency with the other analyses. With only 214 rows across 7 classes, I expected accuracy to be limited, particularly for distinguishing adjacent weekdays that likely have similar traffic profiles. I expected weekend days to be easier to classify correctly given their distinctly lower average counts.

---

## Results

**Question 1**

The best-performing three-bridge subset was Brooklyn Bridge, Manhattan Bridge, and Williamsburg Bridge, meaning the Queensboro Bridge is the one that should be left without a sensor. The test-set results across all four subsets were:

| Bridges Used | Bridge Dropped | R² | MSE |
|---|---|---:|---:|
| Manhattan, Williamsburg, Queensboro | Brooklyn Bridge | 0.983056 | 697,676.76 |
| Brooklyn, Williamsburg, Queensboro | Manhattan Bridge | 0.985601 | 592,865.58 |
| Brooklyn, Manhattan, Queensboro | Williamsburg Bridge | 0.995999 | 164,725.04 |
| Brooklyn, Manhattan, Williamsburg | Queensboro Bridge | 0.997635 | 97,363.42 |

The recommended sensor placement is Brooklyn Bridge, Manhattan Bridge, and Williamsburg Bridge. This subset achieved the highest R² (0.9976) and lowest MSE (97,363.42) among all four subsets. The fitted coefficients were 1.193 for Brooklyn Bridge, 0.943 for Manhattan Bridge, and 1.592 for Williamsburg Bridge, with an intercept of 360.06. The Queensboro Bridge being the least informative bridge is consistent with it being the bridge with the lowest average daily traffic count. Removing it results in the smallest performance drop because its contribution to the total is most predictable from the other three.

**Question 2**

The fitted weather model had the following coefficients: `High Temp` = 380.09, `Low Temp` = −177.04, and `Precipitation` = −8681.59, with an intercept of 1896.02. The test-set R² was 0.575, the MSE was 17,498,379.32, and the RMSE was 4183.11.

The positive coefficient on `High Temp` and the negative coefficient on `Precipitation` match the expectation that warmer and drier days attract more cyclists. The negative coefficient on `Low Temp` may seem counterintuitive, but it is explained by multicollinearity: `High Temp` and `Low Temp` are correlated with each other, so the model partially offsets their effects when fitting simultaneously, and the sign of `Low Temp` should not be interpreted in isolation.

The R² of 0.575 indicates that weather explains roughly 57% of the variance in daily ridership. This is a meaningful signal but leaves substantial unexplained variance. Weather alone is likely not sufficient for reliable police deployment decisions because the model does not account for day-of-week patterns (which Question 3 shows are significant), seasonal trends within the April–October window, or one-off factors like special events. The predicted vs. actual plot (`q2_predicted_vs_actual.png`) confirms this: the predictions track the general trend but show considerable scatter around the ideal diagonal.

**Question 3**

*[Run the code and fill in the values below before submitting.]*

The average total bicycle traffic by day of the week was:

| Day | Average Total Bicyclists |
|---|---:|
| Monday | [value] |
| Tuesday | [value] |
| Wednesday | [value] |
| Thursday | [value] |
| Friday | [value] |
| Saturday | [value] |
| Sunday | [value] |

The bar chart (`q3a_weekly_pattern.png`) shows that [describe pattern here — e.g., "weekdays had consistently higher average traffic than weekends, with a peak on [day] and a trough on [day]"]. This pattern is consistent with a commuter-dominated ridership, where Monday through Friday traffic is driven by work trips and weekend traffic drops as recreational riders partially offset the loss of commuters.

The classification results for predicting day of week from bridge counts were:

| Classifier | Test Accuracy |
|---|---:|
| Logistic Regression | [value] |
| K-Nearest Neighbors | [value] |
| Decision Tree | [value] |
| Random Forest | [value] |

[Describe which classifier performed best and which performed worst. Then reference the confusion matrix output.]

The confusion matrices revealed that [describe pattern — e.g., "weekday classes (Monday through Friday) were frequently confused with one another, while Saturday and Sunday were more reliably identified"]. This is expected: when weekday traffic volumes are similar to each other, the four bridge counts alone do not provide enough distinguishing signal. The overall classification accuracy was limited by the fact that this is a 7-class problem with only 4 numeric features, approximately 170 training samples, and roughly 43 test samples. The small test set also means that accuracy estimates may vary depending on which specific days fell into the test split.

The results for Question 3 taken together suggest that while day-of-week patterns in traffic volume do exist (as shown by the visualization in Part A), they are not distinct enough across all seven days for a classifier trained only on bridge counts to reliably identify each individual day.

---
