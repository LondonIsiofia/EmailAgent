import os

NEWSAPI_KEY = ""
OPENWEATHER_API_KEY = ""
EMAIL_SENDER = ""
EMAIL_RECIEVER = ""
EMAIL_PASS = ""
OUTLOOK_CLIENT_ID = os.environ.get("OUTLOOK_CLIENT_ID")
OUTLOOK_CLIENT_SECRET = os.environ.get("OUTLOOK_CLIENT_SECRET")
OUTLOOK_TENANT_ID = "commmon"
OUTLOOK_SCOPES = ["Mail.Read"]
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
RELIABLE_SOURCES = ["Reuters", "Bloomberg", "CNBC", "CoinDesk", "CoinTelegraph", "The Wall Street Journal"]
CRYPTO_TICKERS = ["BTC-USD", "XRP-USD", "DOGE-USD", "AVAX-USD", "VIX-USD"]
EQ_TICKER = "SPY"
COINGECKO = "https://api.coingecko.com/api/v3/simple/price"
BULL_THRESHOLD = 55.0
ALERT_THRESHOLD = 70.0
IPINFO_URL = "https://ipinfo.io/json"
OPENAI_KEY = ""
