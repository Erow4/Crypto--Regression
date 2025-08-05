import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
import json
import warnings
# File Description: this file holds the linear regression that I used to
#  give a prediction for the next bitcoin price based on the prices of the 
#  previous 30 days (pulled using 'data_collector.py' from 'market_data.csv')


warnings.filterwarnings("ignore")

# Load historical market data
data = pd.read_csv('market_data.csv')

# Feature Engineering: Use previous price as a feature
data['prev_price'] = data['price'].shift(1)
data = data.dropna()

# Prepare the data
X = data[['prev_price']]
y = data['price']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Make a prediction using latest price
try:
    if len(sys.argv) > 1:
        latest_price = float(sys.argv[1])
    else:
        latest_price = X.iloc[-1]['prev_price']  # Use the last known price

    prediction = model.predict([[latest_price]])
    output = {'prediction': float(prediction[0])}

except Exception as e:
    output = {'error': str(e)}

# Output the prediction in JSON format
print(json.dumps(output))
