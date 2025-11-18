import requests, os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from config import NEWSAPI_KEY, RELIABLE_SOURCES, OPENAI_KEY, COINGECKO, NEWSAPI_KEY
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

if torch.backends.mps.is_available():
    dtype = torch.float16
    device = "mps"
else:
    dtype = torch.float32
    device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=dtype,
    device_map={"": device},
)
model.to(device)


def get_market_data():
    data = {}
    try:
        params = {
            "ids": "bitcoin,ripple",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24h_vol": "true",
            "include_24h_change": "true",
            "include_last_updated_at": "true"
        }
        r = requests.get(COINGECKO, params=params, timeout=10)
        r.raise_for_status()
        try:
            res = r.json()
        except Exception as e:
            print("Coin Gecko rate limit", e)
            return data
        
        btc = res.get("bitcoin", {})
        xrp = res.get("ripple", {})
        
        if not btc or not xrp:
            print("⚠️ Missing BTC/XRP data in CoinGecko response")
        
        data["BTC"] = {
            "price": btc.get("usd"),
            "volume": btc.get("usd_24h_vol"),
            "change": btc.get("usd_24h_change"),
            "market_cap": btc.get("usd_market_cap")
        }
        data["XRP"] = {
            "price": xrp.get("usd"),
            "volume": xrp.get("usd_24h_vol"),
            "change": xrp.get("usd_24h_change"),
            "market_cap": xrp.get("usd_market_cap")
        }
    except Exception as e:
        print("Error fetching crypto:", e)
    
    try:
        API_KEY = "4cd89003ea12429abc85e2564cb036e9"
        base_url = "https://api.twelvedata.com/quote"
        symbols = ["SPX", "VIX"]
        params = {
            "symbol": ",".join(symbols),
            "apikey": API_KEY,
            "format": "JSON"
            }
        response = requests.get(base_url, params=params, timeout=15)

        if response.status_code != 200:
            print(f"⚠️ Twelve Data returned {response.status_code}")
            return data

        result = response.json()
        if "SPX" in result and "VIX" in result:
            spx_quote = result.get("SPX", {})
            vix_quote = result.get("VIX", {})
        else:
            spx_quote = result if result.get("symbol") == "SPX" else {}
            vix_quote = result if result.get("symbol") == "VIX" else {}

        spx_data = {
            "price": float(spx_quote.get("close", 0.0)),
            "open": float(spx_quote.get("open", 0.0)),
            "high": float(spx_quote.get("high", 0.0)),
            "low": float(spx_quote.get("low", 0.0)),
            "volume": float(spx_quote.get("volume", 0.0)),
            "change": float(spx_quote.get("change", 0.0)),
            "percent_change": float(spx_quote.get("percent_change", 0.0)),
        }

        vix_data = {
            "value": float(vix_quote.get("close", 0.0)),
            "open": float(vix_quote.get("open", 0.0)),
            "high": float(vix_quote.get("high", 0.0)),
            "low": float(vix_quote.get("low", 0.0)),
            "volume": float(vix_quote.get("volume", 0.0)),
            "change": float(vix_quote.get("change", 0.0)),
            "percent_change": float(vix_quote.get("percent_change", 0.0)),
        }

        data["S&P500"] = spx_data
        data["VIX"] = vix_data

        return data

    except Exception as e:
        print("Error fetching indicators:", e)
        return data

def fetch_articles(category= "business", max_results=3):
    if not NEWSAPI_KEY:
        return []
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "language": "en",
        "pageSize": max_results,
        "apiKey": NEWSAPI_KEY,
        "category": category
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"[News] Error {response.status_code}: {response.text}")
            return []
        else:
            data = response.json()
            articles = data.get("articles", [])
            results = [
                (a["title"], a["url"])
                for a in articles
                if a.get("title") and a.get("url")
            ]
            return results[:max_results]
    except Exception as e:
        print(f"[News] Exception: {e}")
        return []

def get_ai_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": f"You are a professional market analyst.\n\n{prompt}",
                "stream": False
            }
        )

        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        return f"Failed to call Agent. {e}"




def get_market_summary(market_data):
    if not market_data or not isinstance(market_data, dict):
        return "⚠️ No valid market data available to analyze."
    btc = market_data.get('BTC', {})
    xrp = market_data.get('XRP', {})
    spx = market_data.get('S&P500', {})
    vix = market_data.get('VIX', {})
    
    prompt = f"""
    Today’s date: {datetime.now().strftime("%B %d, %Y")}

    Market Data:
    Market Data Snapshot:
    🪙 Bitcoin (BTC)
    • Price: ${btc.get("price")}
    • 24h Change: {btc.get("change")}%
    • 24h Volume: {btc.get("volume")}
    • Market Cap: {btc.get("market_cap")}

    💠 Ripple (XRP)
    • Price: ${xrp.get("price")}
    • 24h Change: {xrp.get("change")}%
    • 24h Volume: {xrp.get("volume")}
    • Market Cap: {xrp.get("market_cap")}

    📈 S&P 500
    • Index Level: {spx.get("price")}

    😬 VIX (Volatility Index)
    • Current Value: {vix.get("value")}

    TASK:
    Analyze short-term market sentiment and probability of bullish vs bearish outcomes (0–100%) for BTC, XRP, and S&P 500 over the next 24 hours.

    Then, for each asset:
    1. State Bullish Probability and Bearish Probability.
    2. Give a likely profitable LONG or SHORT recommendation.
    3. Suggest an Entry Price, Stop Loss, and Take Profit level (reasonable values based on direction and volatility).
    4. Provide a short 1–2 sentence reasoning behind each call.

    Format neatly and make sure it's concise, data-driven, and professional."""
    print("\n🤖 Analyzing market sentiment...")
    try:
        return get_ai_response(prompt)

    except Exception as e:
        return f"Market summary unavailable due to prompt pass error: {e}"
    
def get_smart_news_summary():
    today = datetime.now().strftime("%B %d, %Y")
    market_news = fetch_articles(category="business")
    tech_news = fetch_articles(category="technology")
    
    mdata = get_market_data()
    ai_summary = get_market_summary(mdata)
    summary = f"🧠 SMART MARKET BRIEF — {today}\n\n"
    summary += f"{ai_summary}\n\n"
    summary += "📈 Top Market/Stock News:\n"
    market_section = (
        "\n".join([f"• {title}\n🔗 {url}" for title, url in market_news])
        if market_news
        else "No recent market news available."
    )
    summary += f"{market_section}\n\n"
    tech_section = (
        "\n".join([f"• {title}\n🔗 {url}" for title, url in tech_news])
        if tech_news
        else "No recent tech news available."
    )
    summary += "📈 Top Tech News:\n"
    summary += f"{tech_section}"
    return summary
