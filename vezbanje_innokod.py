from knjiga_app_2 import Author, Book, engine
from sqlmodel import select, func, Session, select
from sqlalchemy import desc

def print_results(data):
    if isinstance(data, list):
        for item in data:
            print(item)
    else:
        print(data)
    print("-----------------------------------")

##################
# Book (naslov, zanr, broj_strana, ocena, dostupna)
# Author (ime, prezime, godina_rodjenja)

with Session(engine) as session:
    statement = select(Book)
    result = session.exec(statement).all()
    print_results(result)