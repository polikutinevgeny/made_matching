import csv
from pathlib import Path
from typing import List, Dict

import click
import sqlalchemy
from sqlmodel import Session, select
from tqdm import tqdm

from matching.database import models
from matching.database.main import create_db_and_tables, engine


def load_stores(path: Path):
    chains = dict()
    stores = []
    with open(path, "r") as csvfile:
        stores_reader = csv.DictReader(csvfile)
        for store in tqdm(stores_reader):
            chain_id = int(store["chain_id"])
            store_id = int(store["store_id"])
            chains[chain_id] = models.Chain(id=chain_id, name=store["chain_name"])
            stores.append(models.Store(store_id=store_id, chain_id=chain_id))

    with Session(engine) as session:
        with session.begin():
            session.add_all(chains.values())
            session.add_all(stores)


def decode_categories(string: str) -> List[str]:
    return string.strip("{}").split(",") if string else []


def load_categories(path: Path) -> Dict[str, models.Category]:
    categories: Dict[str, models.Category] = {}
    children: Dict[str, List[str]] = {}
    with open(path, "r") as csvfile:
        categories_reader = csv.DictReader(csvfile)
        for category in tqdm(categories_reader):
            category_id = category["category_id"]
            categories[category_id] = models.Category(
                category_id=category_id,
                chain_id=int(category["chain_id"]),
                name=category["name"],
                is_main=category["is_main"] == "true"
            )
            children[category_id] = decode_categories(category["children"])
        for category_id, category in categories.items():
            category.children = [categories[i] for i in children[category_id]]
    with Session(engine) as session:
        with session.begin():
            session.add_all(categories.values())
    return categories


def load_products(path: Path, loaded_categories: Dict[str, models.Category]):
    products = []
    categories = []
    external_categories = []
    with open(path, "r") as csvfile:
        products_reader = csv.DictReader(csvfile)
        for product in tqdm(products_reader):
            products.append(models.Product(
                item_id=product["item_id"],
                chain_id=int(product["chain_id"]),
                name=product["name"],
                brand_name=product["brand_name"],
                grammar=int(product["grammar"]) if product["grammar"] != '0' else None,
                volume=int(product["volume"]) if product["volume"] != '0' else None,
                weight=int(product["weight"]) if product["weight"] != '0' else None
            ))
            categories.append(decode_categories(product["categories_ids"]))
            external_categories.append(decode_categories(product["external_categories_ids"]))
    with Session(engine) as session:
        with session.begin():
            for product, cats, external_cats in tqdm(zip(products, categories, external_categories)):
                product.categories = [loaded_categories[i] for i in cats if i in loaded_categories]
                product.external_categories = [loaded_categories[i] for i in external_cats if i in loaded_categories]
            session.add_all(products)


def load_prices(path: Path):
    with Session(engine) as session:
        product_ids = set(session.exec(select(models.Product.item_id)))
    prices = []
    with open(path, "r") as csvfile:
        prices_reader = csv.DictReader(csvfile)
        for price in tqdm(prices_reader):
            if price["item_id"] not in product_ids:
                continue
            prices.append(models.Price(
                store_id=int(price["store_id"]),
                item_id=price["item_id"],
                price=price["price"],
                discount_price=price["discount_price"]
            ))
            if len(prices) >= 10000:
                with Session(engine) as session:
                    with session.begin():
                        session.add_all(prices)
                prices.clear()
    with Session(engine) as session:
        with session.begin():
            session.add_all(prices)


@click.command()
@click.option("--input-dir", help="Directory with files to load", type=click.Path(path_type=Path))
def load_files(input_dir: Path):
    try:
        create_db_and_tables()
        load_stores(input_dir / "stores.csv")
        categories = load_categories(input_dir / "categories.csv")
        load_products(input_dir / "products.csv", categories)
        load_prices(input_dir / "prices.csv")
    except sqlalchemy.exc.IntegrityError as e:
        print("Already loaded")


if __name__ == '__main__':
    load_files()
