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

# 9.2.2026.
##################
# Book (naslov, zanr, broj_strana, ocena, dostupna)
# Author (ime, prezime, godina_rodjenja)

# select() # biras tabelu
# .where() # filtriras po uslovima za kolone
# .limit() # koliko rezultata se vrace
# .order_by() # sortiras dobijene rezultate 
# desc() # descedning order
# .contains() # pronadji vrednosti koje sadrze nesto

# CURRENT QUERY: Find titles containing "King"
with Session(engine) as session:
    statement = select()
    result = session.exec(statement).all()
    print_results(result)
