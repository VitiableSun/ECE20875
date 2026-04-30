import pandas
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

''' 
The following is the starting code for path2 for data reading to make your first step easier.
'dataset_2' is the clean data for path1.
'''
dataset_2 = pandas.read_csv('nyc_bicycle_counts_2016.csv')
dataset_2['Brooklyn Bridge']      = pandas.to_numeric(dataset_2['Brooklyn Bridge'].replace(',','', regex=True))
dataset_2['Manhattan Bridge']     = pandas.to_numeric(dataset_2['Manhattan Bridge'].replace(',','', regex=True))
dataset_2['Queensboro Bridge']    = pandas.to_numeric(dataset_2['Queensboro Bridge'].replace(',','', regex=True))
dataset_2['Williamsburg Bridge']  = pandas.to_numeric(dataset_2['Williamsburg Bridge'].replace(',','', regex=True))
# print(dataset_2.to_string()) #This line will print out your data

dataset_2['Total'] = pandas.to_numeric(dataset_2['Total'].replace(',','', regex=True))
count_columns = ['Brooklyn Bridge', 'Manhattan Bridge', 'Queensboro Bridge', 'Williamsburg Bridge', 'Total']
missing_counts = dataset_2[count_columns].isna().sum()
if missing_counts.sum() > 0:
    print('Missing values found after conversion:')
    print(missing_counts.to_string())
    dataset_2 = dataset_2.dropna(subset=count_columns)
print('No NaN values remaining after cleaning:', dataset_2[count_columns].isna().sum().sum() == 0)

bridges = ['Brooklyn Bridge', 'Manhattan Bridge', 'Williamsburg Bridge', 'Queensboro Bridge']
y = dataset_2['Total']
q1_results = []
for dropped_bridge in bridges:
    selected_bridges = [bridge for bridge in bridges if bridge != dropped_bridge]
    X = dataset_2[selected_bridges]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    r2 = r2_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    q1_results.append({
        'dropped_bridge': dropped_bridge,
        'selected_bridges': selected_bridges,
        'r2': r2,
        'mse': mse,
        'coefficients': dict(zip(selected_bridges, model.coef_)),
        'intercept': model.intercept_
    })

print('\nQuestion 1: Sensor placement')
for result in q1_results:
    print('Install on ' + ', '.join(result['selected_bridges']) + '; drop ' + result['dropped_bridge'] + ': R^2=' + format(result['r2'], '.6f') + ', MSE=' + format(result['mse'], '.2f'))
best_q1 = max(q1_results, key=lambda item: item['r2'])
print('Recommendation: Install sensors on: ' + ', '.join(best_q1['selected_bridges']) + '. Drop: ' + best_q1['dropped_bridge'] + '.')
for bridge, coefficient in best_q1['coefficients'].items():
    print(bridge + ' coefficient: ' + format(coefficient, '.6f'))
print('Best model intercept: ' + format(best_q1['intercept'], '.6f'))

weather_features = ['High Temp', 'Low Temp', 'Precipitation']
X_weather = dataset_2[weather_features]
X_train, X_test, y_train, y_test = train_test_split(X_weather, y, test_size=0.2, random_state=42)
weather_model = LinearRegression()
weather_model.fit(X_train, y_train)
weather_predictions = weather_model.predict(X_test)
weather_r2 = r2_score(y_test, weather_predictions)
weather_mse = mean_squared_error(y_test, weather_predictions)
weather_rmse = np.sqrt(weather_mse)

print('\nQuestion 2: Weather prediction')
for feature, coefficient in zip(weather_features, weather_model.coef_):
    print(feature + ' coefficient: ' + format(coefficient, '.6f'))
print('Intercept: ' + format(weather_model.intercept_, '.6f'))
print('R^2: ' + format(weather_r2, '.6f'))
print('MSE: ' + format(weather_mse, '.2f'))
print('RMSE: ' + format(weather_rmse, '.2f'))

plt.figure(figsize=(7, 5))
plt.scatter(weather_predictions, y_test)
line_min = min(weather_predictions.min(), y_test.min())
line_max = max(weather_predictions.max(), y_test.max())
plt.plot([line_min, line_max], [line_min, line_max])
plt.xlabel('Predicted Total')
plt.ylabel('Actual Total')
plt.title('Weather Model: Predicted vs Actual Total Bike Traffic')
plt.tight_layout()
plt.savefig('q2_predicted_vs_actual.png', dpi=200)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_avg = dataset_2.groupby('Day')['Total'].mean().reindex(day_order)
print(daily_avg)
plt.figure(figsize=(7, 5))
plt.bar(day_order, daily_avg.values)
plt.xlabel('Day of Week')
plt.ylabel('Average Total Bicyclists')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('q3a_weekly_pattern.png', dpi=200)

day_map = {day: i for i, day in enumerate(day_order)}
dataset_2['day_num'] = dataset_2['Day'].map(day_map)
X_day = dataset_2[['Brooklyn Bridge', 'Manhattan Bridge', 'Williamsburg Bridge', 'Queensboro Bridge']].values
y_day = dataset_2['day_num'].values
X_day_train, X_day_test, y_day_train, y_day_test = train_test_split(X_day, y_day, test_size=0.2, random_state=42)
for clf in [LogisticRegression(max_iter=1000), KNeighborsClassifier(), DecisionTreeClassifier(), RandomForestClassifier()]:
    clf.fit(X_day_train, y_day_train)
    y_day_pred = clf.predict(X_day_test)
    print(type(clf).__name__, accuracy_score(y_day_test, y_day_pred))
    print(confusion_matrix(y_day_test, y_day_pred))
    print(classification_report(y_day_test, y_day_pred))
