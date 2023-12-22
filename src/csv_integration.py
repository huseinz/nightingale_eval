import csv
from pathlib import Path
from typing import Iterable

from sqlalchemy import (
    Engine,
    create_engine,
    select,
)
from sqlalchemy.orm import Session

from models import (
    Base,
    Cities
)


def load_csv_to_db(engine: Engine, csv_filepath: Path) -> int:
    with open(csv_filepath, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
        cities = [Cities(**row) for row in csv_reader]

    with Session(engine) as session:
        session.add_all(cities)
        session.commit()

    return len(cities)


def select_cities_all(engine: Engine) -> Iterable[dict]:
    with Session(engine) as session:
        pq = session.execute(select(Cities)).all()
        return [i[0].__dict__ for i in pq]


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    db_filepath = root_dir / 'data' / 'data.db'
    csv_filepath = root_dir / 'data' / 'cities.csv'

    engine = create_engine(f'sqlite:///{db_filepath}')

    # drop cities table before load
    Base.metadata.drop_all(engine, tables=[Cities.__table__])
    Base.metadata.create_all(engine)

    success_count = load_csv_to_db(engine, csv_filepath)
    print(f'Wrote {success_count} records from {csv_filepath} to {db_filepath}')

    #for c in select_cities_all(engine):
    #    if '_sa_instance_state' in c:
    #        del c['_sa_instance_state']
    #    print(c)
