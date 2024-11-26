from db import SessionLocal, init_db
from models import Url, Listing

import httpx
import logging
import os
import pandas as pd 
from bs4 import BeautifulSoup
from extruct.jsonld import JsonLdExtractor
from rich import print
from rich.logging import RichHandler
from sqlalchemy.exc import IntegrityError

FILEPATH_CSV = 'links.csv'
FILEPATH_PROXY = 'proxies.csv'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0"
}
BASEDIR = os.path.dirname(os.path.realpath("__file__"))

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()]
)


def get_links(url: str, proxy: str = None) -> list:
    resp = httpx.get(url, headers=HEADERS, proxy=proxy)
    if resp.status_code != 200:
        logging.warn(
            f"Url {url} responded with bad status code {resp.status_code}."
        )
        return []
    else:
        soup = BeautifulSoup(resp.text, 'html.parser')
        hrefs = [li.a['href'] for li in 
                 soup.find_all('li', class_='searchCardList--listItem')
                 if li.a is not None]
        return hrefs


def load_links(session, urls: list, city: str):
    for url in urls:
        new_url = Url(
            city = city,
            url = url
            )
        
        try:
            session.add(new_url)
            session.commit()
        except IntegrityError as err:
            session.rollback()
            logging.exception(err)


if __name__ == "__main__":
    
    try:
        init_db()
        session = SessionLocal()
        df = pd.read_csv(FILEPATH_CSV)
        dfproxy = pd.read_csv(FILEPATH_PROXY)
        for _, row in df.iterrows():
            
            links = get_links(
                row["url"], 
                proxy=dfproxy['proxy'].sample(1).values[0]
            )
            load_links(session, links, city=row["city"])
    except Exception as err:
        logging.exception(err)
    finally:
        session.close()
