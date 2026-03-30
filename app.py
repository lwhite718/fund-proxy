from flask import Flask, jsonify, request
import yfinance as yf
from curl_cffi.requests import Session

app = Flask(__name__)

@app.route('/fetch-fund-data', methods=['POST'])
def fetch_fund_data():
    data = request.json or {}
    ticker = (data.get('ticker') or '').strip().upper()
    if not ticker:
        return jsonify({'error': 'ticker required'}), 400
    try:
        session = Session(impersonate="chrome")
        t = yf.Ticker(ticker, session=session)
        info = t.info or {}
        if not info:
            return jsonify({'error': 'No data returned'}), 404
        return jsonify({
            'available': True,
            'ticker': ticker,
            'fund_name': info.get('longName') or info.get('shortName') or ticker,
            'fund_type': 'equity',
            'raw_metrics': {
                'expense_ratio': info.get('annualReportExpenseRatio') or info.get('expenseRatio'),
                'return_5yr': info.get('fiveYearAverageReturn'),
                'return_3yr': info.get('threeYearAverageReturn'),
                'dividend_yield': info.get('yield') or info.get('dividendYield'),
                'dividend_yield_5yr': info.get('fiveYearAvgDividendYield'),
                'payout_ratio': info.get('payoutRatio'),
                'beta': info.get('beta'),
                'aum': info.get('totalAssets'),
                'turnover': info.get('annualHoldingsTurnover'),
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

---

**File 2: `requirements.txt`**
```
flask
gunicorn
yfinance==0.2.66
curl_cffi
```

---

**File 3: `Procfile`** (no file extension)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
