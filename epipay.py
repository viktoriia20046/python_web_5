import aiohttp
import asyncio
from datetime import datetime, timedelta
import json
import certifi
import ssl

BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

async def fetch_rates(date: str):
    url = f"{BASE_URL}{date}"
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as response:
            response.raise_for_status()
            data = await response.json()
            return data

def format_rates(data):
    rates = {}
    for item in data.get('exchangeRate', []):
        if item['currency'] in ['EUR', 'USD']:
            rates[item['currency']] = {
                'sale': item['saleRate'],
                'purchase': item['purchaseRate']
            }
    return rates

async def get_rates_for_last_days(days: int):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    tasks = []

    for i in range(days):
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime("%d.%m.%Y")
        tasks.append(fetch_rates(formatted_date))
    
    responses = await asyncio.gather(*tasks)
    
    result = []
    for i, data in enumerate(responses):
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime("%d.%m.%Y")
        rates = format_rates(data)
        result.append({formatted_date: rates})
    
    return result

if __name__ == "__main__":
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    if days > 10:
        print("Error: Can only fetch data for up to 10 days.")
    else:
        rates = asyncio.run(get_rates_for_last_days(days))
        print(rates)

        # Записати дані у файл JSON
        with open('exchange_rates.json', 'w') as f:
            json.dump(rates, f, indent=4, ensure_ascii=False)