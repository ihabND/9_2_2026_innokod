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

#### OVO IZNAD SE NE MENJA
#### MI RADIMO S OVIM ISPOD (s 20tom linijom)

with Session(engine) as session:
    # u statement (linija ispod) stavljamo ime Tabele iz koje selektujemo podatke 
    # i filtere ako su nam potrebi
    statement = select() ### menjas samo ovu liniju
    result = session.exec(statement).all()
    print_results(result)