from db import SessionLocal, init_db
from models import Url, Listing
import httpx
import logging
from extruct.jsonld import JsonLdExtractor
from rich import print
from rich.logging import RichHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)

def get_data(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0"
    }

    resp = httpx.get(url, headers=headers)

    if resp.status_code != 200:
        logging.info(f"Url {url} responded with bad status code {resp.status_code}.")
    else:
        jslde = JsonLdExtractor()
        data = jslde.extract(resp.text)
        return data

if __name__ == "__main__":
    init_db()
    dt = get_data("https://streeteasy.com/building/1200-grand-street-hoboken/rental/4596613")
    print(type(dt))
    print(dt)
