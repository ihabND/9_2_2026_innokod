from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

### DATABASE

# KLASA Autor
# id (primarni kljuc)
# ime (maksimalna duzina = 50)
# prezime (maksimalna duzina = 50)
# godina_rodjenja (moze da ne postoji, default je None)


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    naslov: str = Field(max_length=200)
    zanr: str = Field(max_length=50)
    broj_strana: int = Field(default=0, ge=0, le=10000)
    ocena: float = Field(default=0.0, ge=0.0, le=5.0)
    dostupna: bool = Field(default=True)

engine = create_engine("sqlite:///library_with_author.db")


def create_db():
    SQLModel.metadata.create_all(engine)


### CRUD - BOOK

def napravi_knjigu(
    naslov: str,
    zanr: str,
    broj_strana: int = 0,
    ocena: float = 0.0,
    dostupna: bool = True,
):
    knjiga = Book(
        naslov=naslov,
        zanr=zanr,
        broj_strana=broj_strana,
        ocena=ocena,
        dostupna=dostupna,
    )
    with Session(engine) as session:
        session.add(knjiga)
        session.commit()
        session.refresh(knjiga)
    return "Knjiga napravljena"


def procitaj_knjigu(naslov: str):
    with Session(engine) as session:
        statement = select(Book).where(Book.naslov == naslov)
        knjiga = session.exec(statement).first()
    return knjiga


def obrisi_knjigu(naslov: str):
    with Session(engine) as session:
        statement = select(Book).where(Book.naslov == naslov)
        knjiga = session.exec(statement).first()
        if knjiga:
            session.delete(knjiga)
            session.commit()
            return True
    return False


def update_knjigu(
    naslov: str,
    novi_zanr: str | None = None,
    novi_broj_strana: int | None = None,
    nova_ocena: float | None = None,
    nova_dostupna: bool | None = None
):
    with Session(engine) as session:
        statement = select(Book).where(Book.naslov == naslov)
        knjiga = session.exec(statement).first()
        if knjiga:
            if novi_zanr is not None:
                knjiga.zanr = novi_zanr
            if novi_broj_strana is not None:
                knjiga.broj_strana = novi_broj_strana
            if nova_ocena is not None:
                knjiga.ocena = nova_ocena
            if nova_dostupna is not None:
                knjiga.dostupna = nova_dostupna
            session.add(knjiga)
            session.commit()
            session.refresh(knjiga)
            return knjiga
    return None

### MAIN

create_db()