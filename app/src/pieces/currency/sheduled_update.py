import json
import os

import requests
from crontab import CronTab

from app.src.database.common import get_db
from app.src.pieces.currency.models import CurrencyModel
from app.src.pieces.currency.schemas import CurrencyCreationSchema

script_dir = os.path.dirname(os.path.realpath(__file__))


def get_api_key():
    with open(f"{script_dir}/currency_api_config.json") as file:
        config = json.load(file)
        return config["api_key"]


def update_currency(name: str):
    fetch_currency_url = f"https://api.freecurrencyapi.com/v1/latest?apikey={get_api_key()}&currencies={name}"
    json_data = requests.get(fetch_currency_url).json()

    currency_value = json_data["data"][name]
    currency = CurrencyCreationSchema(name=name, value=currency_value)
    currency_model = CurrencyModel(**currency.dict())

    db = next(get_db())
    db.add(currency_model)
    db.commit()
    db.refresh(currency_model)


def schedule_currency_update(name: str):
    cron = CronTab(user="root")
    job = cron.new(command=update_currency(name))
    job.minute.every(1)
    cron.write()


def main():
    print(update_currency("RUB"))


if __name__ == "__main__":
    main()
