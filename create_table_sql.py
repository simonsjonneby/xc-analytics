import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL=os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE flights (id SERIAL PRIMARY KEY,origin VARCHAR NOT NULL,destination VARCHAR NOT NULL,duration INTEGER NOT NULL);")
    db.commit()

if __name__ == "__main__":
    main()
