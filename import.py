import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL=os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("data/Athletes.csv", 'r')
    reader = csv.reader(f,delimiter=';')
    for id, athlete, year_born, nation in reader:
        db.execute("INSERT INTO athletes (id, athlete, year_born, nation) VALUES (:id, :athlete, :year_born, :nation)",
                        {"id": id, "athlete": athlete, "year_born": year_born,"nation": nation})
        print(f"Added athlete  {athlete}")
        db.commit()

if __name__ == "__main__":
    main()
