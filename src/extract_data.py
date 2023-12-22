import csv
from pathlib import Path
from typing import Iterable

from sqlalchemy import (
    select,
    Engine,
    create_engine,
    func,
    cast,
    Integer,
)
from sqlalchemy.orm import Session

from models import (
    Base,
    Product,
    ProductImage,
)


def query_count_product_images_all(engine: Engine) -> Iterable[dict]:
    with Session(engine) as session:
        sql = select(Product.id, Product.title, cast(Product.price, Integer), func.count(ProductImage.url).label('image_count')) \
              .join(Product, Product.id == ProductImage.product_id) \
              .group_by(Product.id)

        pq = session.execute(sql)
        col_names = pq.keys()
        rows = pq.all()

        # return as dicts with keys as column names
        return [dict(zip(col_names, r)) for r in rows]


def write_product_csv(products: list[dict], csv_filepath: Path) -> int:
    success_count = 0
    if not products:
        return 0

    with open(csv_filepath, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(products[0].keys()), quoting=csv.QUOTE_NONNUMERIC, quotechar='"')

        writer.writeheader()
        for p in products:
            writer.writerow(p)
            success_count += 1

    return success_count


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    db_filepath = root_dir / 'data' / 'data.db'
    csv_filepath = root_dir / 'data' / 'count_product_images.csv'

    engine = create_engine(f'sqlite:///{db_filepath}')
    products = query_count_product_images_all(engine)

    success_count = write_product_csv(products, csv_filepath)
    print(f'Wrote {success_count} records to {csv_filepath}')
