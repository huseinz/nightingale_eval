from pathlib import Path
from typing import Iterable
from jsonschema import validate

import requests
from sqlalchemy import (
    select,
    Engine,
    create_engine,
)
from sqlalchemy.orm import Session

from models import (
    Base,
    Product,
    ProductImage,
    ProductSchemaJSON,
)

from itertools import groupby
from pprint import pprint


# helper to get list of products from API endpoint, validate schema, and handle pagination
def get_products(url: str, schema: dict, limit=30, skip=0) -> Iterable[dict]:
    while True:
        r = requests.get(url, params={'limit': limit, 'skip': skip})
        r.raise_for_status()

        data = r.json()

        # validate json payload
        validate(data, schema)

        total = data.get('total', 0)
        products = data.get('products', [])

        yield from products

        skip += limit
        if skip >= total:
            break


# given a SQLAlchemy engine connection and a list of product dicts:
# - create Product object
# - create ProductImage objects from the images field
# - insert or update Product object to product table
# - delete any existing ProductImages associated with the Product. We need to do this to handle the scenario where
#   an image was removed or modified from the list of product images
# - insert ProductImage objects to product_image table
def update_products(engine: Engine, products: Iterable[dict]) -> int:

    success_count = 0

    with Session(engine) as session:
        for p in products:
            product_id = p['id']
            images_urls = p['images']

            # create Product object
            product_orm = Product(
                id=p['id'],
                title=p['title'],
                description=p['description'],
                price=p['price'],
                discount_percentage=p['discountPercentage'],
                rating=p['rating'],
                stock=p['stock'],
                brand=p['brand'],
                category=p['category'],
                thumbnail=p['thumbnail'],
            )

            # create ProductImage objects
            images_orm = []
            for i in images_urls:
                images_orm.append(ProductImage(product_id=product_id, url=i))

            # delete product images if they already exist in product_image table
            # we need to do this to handle the scenario of deleting/modifying product images
            session.query(ProductImage).filter_by(product_id=product_id).delete()

            # add new objects and commit
            session.merge(product_orm)
            session.add_all(images_orm)
            success_count += 1

        # commit once loop is complete and all objects are created
        session.commit()

        return success_count


# return all rows in product table
def query_product_all(engine: Engine) -> Iterable[dict]:
    with Session(engine) as session:
        sql = select(Product)
        pq = session.execute(sql).all()
        return [i[0].__dict__ for i in pq]


# return all rows in product_image table
def query_product_images_all(engine: Engine) -> Iterable[dict]:
    with Session(engine) as session:
        sql = select(ProductImage)
        pq = session.execute(sql).all()
        return [{'id': i[0].id, 'product_id': i[0].product_id, 'url': i[0].url} for i in pq]


# return a dict where the keys are product_id and the values are the list of product image URLs
def query_join_product_images_all(engine: Engine) -> dict:
    with Session(engine) as session:
        sql = select(Product.id, ProductImage.url).join(Product, Product.id == ProductImage.product_id)
        pq = session.execute(sql).all()

        result = {}
        for k, g in groupby(pq, lambda x: x[0]):
            result[k] = [i[1] for i in list(g)]
        return result


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    db_filepath = root_dir / 'data' / 'data.db'

    engine = create_engine(f'sqlite:///{db_filepath}')
    Base.metadata.create_all(engine)

    products = get_products("https://dummyjson.com/products", ProductSchemaJSON)

    success_count = update_products(engine, products)
    print(f'Wrote {success_count} products to {db_filepath}')

    #print('Product ID, [Image URLs]')
    #pprint(query_join_product_images_all(engine))
    #print()

    #print('product_image')
    #pprint(query_product_images_all(engine))
    #print()

    #pprint(query_product_all(engine))

