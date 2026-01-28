import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CMC_API_KEY = os.getenv("CMC_API_KEY")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def get_usdc_ratio():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": "USDC"}

    r = requests.get(url, headers=headers, params=params).json()
    data = r["data"]["USDC"]["quote"]["USD"]

    vol = data["volume_24h"]
    mcap = data["market_cap"]

    return vol / mcap * 100


def get_rank490_volume():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {
        "start": 1,
        "limit": 1000,
        "sort": "volume_24h",
        "sort_dir": "desc"
    }

    r = requests.get(url, headers=headers, params=params).json()
    token = r["data"][489]  # rank 490

    name = token["name"]
    symbol = token["symbol"]
    vol = token["quote"]["USD"]["volume_24h"]

    return name, symbol, vol


def main():
    usdc_ratio = get_usdc_ratio()
    name, symbol, vol490 = get_rank490_volume()

    msg = (
        f"📊 Daily Volume Report\n\n"
        f"1) USDC Vol/Marketcap = {usdc_ratio:.2f}%\n\n"
        f"2) Rank #490 Volume Token: {name} ({symbol})\n"
        f"   Volume 24h = ${vol490:,.0f}"
    )

    send_telegram(msg)


if __name__ == "__main__":
    main()
