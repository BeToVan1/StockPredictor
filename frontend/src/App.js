import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('AMD');
  const [daysAhead, setDaysAhead] = useState(5);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:3000/predict', {
        params: {
          ticker,
          days: daysAhead,
        },
      });

      setPrediction(response.data.prediction);
      //console.log(`PREDICTION: ${response.data.prediction}`);
      setError(null);
    } catch (err) {
      //console.log(err);
      setError(err.response?.data?.message || 'Something went wrong');
      setPrediction(null);
    } finally{
      setLoading(false);
    }
  };

  return (
  <div className="container">
    <div className="predictor-box">
      <h1>📈 Stock Price Predictor</h1>

      <div>
        <label>Ticker Symbol: </label>
        <input value={ticker} onChange={(e) => setTicker(e.target.value)} />
      </div>

      <div>
        <label>Days Ahead: </label>
        <input
          type="number"
          value={daysAhead}
          onChange={(e) => setDaysAhead(e.target.value)}
        />
      </div>

      <button onClick={handlePredict} disabled={loading}>Predict</button>

      <div className="result">
        {loading && <p>🔄 Loading prediction...</p>}
        {!loading && prediction && (
          <h2>
            📊 Predicted Price in {daysAhead} day(s): ${parseFloat(prediction).toFixed(2)}
          </h2>
        )}
        {error && <p className="error">❌ {error}</p>}
      </div>
    </div>
  </div>
  );
}

export default App;
