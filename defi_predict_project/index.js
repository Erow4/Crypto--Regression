const express = require('express');
const axios = require('axios');
const { execFile } = require('child_process');
const path = require('path');

const app = express();
app.use(express.json());

// Function to run Python model
function getAIPrediction(latestPrice) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, 'regress_model.py');

    execFile('python', [scriptPath, latestPrice], (error, stdout, stderr) => {
      if (error) {
        console.error('Error executing Python script:', error);
        return reject(error);
      }

      if (stderr) {
        console.error('Python script stderr:', stderr);
        return reject(stderr);
        // Often harmless, but can indicate issues
      }

      try {
        const result = JSON.parse(stdout);
        resolve(result.prediction);
      } catch (parseError) {
        console.error('Error parsing Python output:', parseError);
        reject(parseError);
      }
    });
  });
}

// API Endpoint to Predict Price
app.get('/predict_price', async (req, res) => {
  try {
    // Fetch latest BTC price from CoinGecko
    const response = await axios.get('https://api.coingecko.com/api/v3/simple/price', {
      params: { ids: 'bitcoin', vs_currencies: 'usd' },
    });

    const latestPrice = response.data.bitcoin.usd;

    // Get AI prediction from Python model
    const predictedPrice = await getAIPrediction(latestPrice);

    res.json({
      latest_price: {
        value: latestPrice,
        currency: 'USD',
      },
      predicted_price: {
        value: predictedPrice,
        currency: 'USD',
      },
    });

  } catch (error) {
    console.error('Error in /predict_price endpoint:', error);
    res.status(500).json({ error: 'Failed to get prediction', details: error.message });
  }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// Startup action: Predict price and suggest action
(async () => {
  try {
    const response = await axios.get('https://api.coingecko.com/api/v3/simple/price', {
      params: { ids: 'bitcoin', vs_currencies: 'usd' },
    });

    const latestPrice = response.data.bitcoin.usd;
    console.log(`Latest Bitcoin Price: $${latestPrice}`);

    const predictedPrice = await getAIPrediction(latestPrice);
    console.log(`AI Predicted Price: $${predictedPrice.toFixed(2)} USD`);

    // Naive trading suggestion
    if (predictedPrice > latestPrice * 1.01) {
      console.log('Prediction suggests price will increase. Consider buying.');
    } else if (predictedPrice < latestPrice * 0.99) {
      console.log('Prediction suggests price will decrease. Consider selling.');
    } else {
      console.log('Prediction suggests price will remain stable. Hold position.');
    }

  } catch (error) {
    console.error('Error during initial prediction check:', error);
  }
})();
