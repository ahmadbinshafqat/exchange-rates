from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import create_exchange_rates_table, get_rates_by_date
from background_job import fetch_and_store_exchange_rates, fetch_exchange_rates
from datetime import datetime, timedelta

app = FastAPI()
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    """Create table if it doesn't exist on FastAPI startup."""
    create_exchange_rates_table()
    scheduler.add_job(fetch_and_store_exchange_rates, 'cron', hour=22)  # Schedule job at 10 PM
    scheduler.start()


@app.get("/exchange-rates")
def get_exchange_rates_route():
    """API endpoint to return exchange rates with comparison to previous day."""
    return get_exchange_rates()


def get_exchange_rates():
    """Retrieve current and previous exchange rates for comparison."""
    today = datetime.utcnow().date().isoformat()
    rates_today = fetch_exchange_rates()

    current_rates = rates_today if rates_today and "error" not in rates_today else []

    previous_day = (datetime.utcnow() - timedelta(days=1)).date().isoformat()
    previous_rates = get_rates_by_date(previous_day)

    response = []
    previous_rates_map = {rate['Currency']: rate['Rate'] for rate in previous_rates}

    for rate in current_rates:
        currency = rate['currency']
        current_rate = float(rate['rate'])
        previous_rate = float(previous_rates_map.get(currency, 0))
        rate_change = current_rate - previous_rate if previous_rate else None
        response.append({
            'currency': currency,
            'current_rate': current_rate,
            'previous_rate': previous_rate if previous_rate else "N/A",
            'change': rate_change if rate_change else "N/A"
        })

    return {"exchange_rates": response}
