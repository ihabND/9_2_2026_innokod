from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship

### DATABASE

class Author(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ime: str = Field(max_length=50)
    prezime: str = Field(max_length=50)
    godina_rodjenja: int | None = Field(default=None)

    knjige: list["Book"] = Relationship(back_populates="autor")


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    naslov: str = Field(max_length=200)
    zanr: str = Field(max_length=50)
    broj_strana: int = Field(default=0, ge=0, le=10000)
    ocena: float = Field(default=0.0, ge=0.0, le=5.0)
    dostupna: bool = Field(default=True)

    autor_id: int | None = Field(default=None, foreign_key="author.id")
    autor: Author | None = Relationship(back_populates="knjige")

engine = create_engine("sqlite:///library_with_author.db")


def create_db():
    SQLModel.metadata.create_all(engine)


### CRUD - AUTHOR

def dodaj_autora(ime: str, prezime: str, godina_rodjenja: int | None = None):
    autor = Author(ime=ime, prezime=prezime, godina_rodjenja=godina_rodjenja)
    with Session(engine) as session:
        session.add(autor)
        session.commit()
        session.refresh(autor)
        return autor


def procitaj_autora(ime: str, prezime: str):
    with Session(engine) as session:
        statement = select(Author).where(
            Author.ime == ime, Author.prezime == prezime
        )
        return session.exec(statement).first()


def obrisi_autora(ime: str, prezime: str):
    with Session(engine) as session:
        statement = select(Author).where(
            Author.ime == ime, Author.prezime == prezime
        )
        autor = session.exec(statement).first()
        if autor:
            session.delete(autor)
            session.commit()
            return True
    return False


### CRUD - BOOK

def napravi_knjigu(
    naslov: str,
    zanr: str,
    broj_strana: int = 0,
    ocena: float = 0.0,
    dostupna: bool = True,
    autor_id: int | None = None,
):
    knjiga = Book(
        naslov=naslov,
        zanr=zanr,
        broj_strana=broj_strana,
        ocena=ocena,
        dostupna=dostupna,
        autor_id=autor_id,
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
        if knjiga:
            autor = knjiga.autor
    return knjiga, autor


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
    nova_dostupna: bool | None = None,
    novi_autor_id: int | None = None,
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
            if novi_autor_id is not None:
                knjiga.autor_id = novi_autor_id
            session.add(knjiga)
            session.commit()
            session.refresh(knjiga)
            return knjiga
    return None


def knjige_autora(ime: str, prezime: str):
    with Session(engine) as session:
        statement = select(Author).where(
            Author.ime == ime, Author.prezime == prezime
        )
        autor = session.exec(statement).first()
        if autor:
            return autor.knjige
    return []


### MAIN

create_db()

# autor = dodaj_autora("Lav", "Tolstoj", 1828)

# knjiga = napravi_knjigu(
#     "Rat i mir",
#     "Istorijski roman",
#     1225,
#     4.82,
#     True,
#     autor_id=autor.id,
# )

# print(procitaj_knjigu("Rat i mir"))
# update_knjigu(naslov="Rat i mir", nova_ocena=1.23)
# print(procitaj_knjigu("Rat i mir"))

# print(knjige_autora("Lav", "Tolstoj"))