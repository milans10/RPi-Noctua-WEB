#  Vytvořil Milan Švarc v roce 2022.

from sqlalchemy import Column, Integer, String

from databaze import Base


class polozka_db(Base):
    __tablename__ = "noctua_rpi"

    id = Column(Integer, primary_key=True, index=True)
    cas = Column(String, unique=True, index=True)
    teplota = Column(String)
    noctua = Column(String, default=True)
