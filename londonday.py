from sender import send_email
from weather import get_auto_weather
from stock_summ import get_stock_summary
from open import get_smart_news_summary
from config import EMAIL_SENDER, OPENAI_KEY


def compose_daily_brief():
    sections = [
        "🌤 WEATHER UPDATE\n" + get_auto_weather(),
        get_stock_summary(),
        "\n🧠 SMART NEWS SUMMARY\n" + get_smart_news_summary(),
    ]
    return "\n\n".join(sections)


def main():
    subject = "Morning AI Brief"
    body = compose_daily_brief()
    send_email(subject, body)
    
if __name__ == "__main__":
    main()