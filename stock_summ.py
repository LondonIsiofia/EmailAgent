import yfinance as yf
from config import CRYPTO_TICKERS

def get_stock_summary():
    lines = ["📈 Market Summary:"]
    for ticker in CRYPTO_TICKERS:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev = float(hist["Close"].iloc[-2])
                last = float(hist["Close"].iloc[-1])
                pct = ((last - prev) / prev) * 100.0
                lines.append(f"{ticker}: {last:.2f} ({pct:+.2f}%)")
        except Exception:
            lines.append(f"{ticker}: (data error)")
    return "\n".join(lines)
