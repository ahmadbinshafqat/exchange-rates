from db import store_exchange_rate
import xml.etree.ElementTree as ET
import requests
from datetime import datetime


def fetch_exchange_rates():
    """Fetch exchange rates from ECB and parse the XML data."""
    ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    response = requests.get(ECB_URL)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
        rates = []

        for cube in root.findall(".//ns:Cube[@currency]", namespaces):
            rates.append({
                'currency': cube.attrib['currency'],
                'rate': cube.attrib['rate']
            })
        return rates
    else:
        return {"error": "Failed to fetch exchange rates"}


async def fetch_and_store_exchange_rates():
    """Fetch and store today's exchange rates in DynamoDB."""
    today = datetime.utcnow().date().isoformat()
    rates_today = fetch_exchange_rates()

    if rates_today and "error" not in rates_today:
        for rate in rates_today:
            store_exchange_rate(rate['currency'], rate['rate'], today)

