#  Vytvořil Milan Švarc v roce 2022.
from sqlalchemy.orm import Session

import model_db


def posledni_polozka(db: Session):
    return db.query(model_db.polozka_db).all()[-1]


def vsechny_polozky(db: Session, skip: int = 0, limit: int = -1):
    return db.execute(f"SELECT id,cas,teplota,noctua FROM noctua_rpi ORDER BY id DESC LIMIT {limit} OFFSET {skip}")
