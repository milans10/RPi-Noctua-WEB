#  Vytvořil Milan Švarc v roce 2022.
import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import funkce_db
from databaze import SessionLocal

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def nacti_home(request: Request, db: Session = Depends(get_db)):
    polozky = funkce_db.vsechny_polozky(db, limit=25)

    def aktualni_teplota():
        vystup_mereni = os.popen('vcgencmd measure_temp').readline()
        teplota = (vystup_mereni.replace("temp=", "").replace("'C\n", ""))
        try:
            teplota = str(int(round(float(teplota), 0)))
        except ValueError:
            return "nezměřeno"

        return str(teplota)

    teplota = aktualni_teplota()
    try:
        teplota = float(teplota)
    except ValueError:
        teplota = 100

    if teplota <= 50.0:
        barva = "green"
    elif 50.0 < teplota < 65.0:
        barva = "dark_orange"
    else:
        barva = "red"

    return templates.TemplateResponse("index.html",
                                      {"request": request, "polozka_id": polozky, "teplota": aktualni_teplota(),
                                       "barva": barva})


@app.get("/polozka", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db)):
    polozka = funkce_db.posledni_polozka(db)
    polozka_id = list()
    polozka_id.append(polozka)
    return templates.TemplateResponse("polozka.html", {"request": request, "polozka_id": polozka_id})


@app.get("/polozka/vse", response_class=HTMLResponse)
async def read_item(request: Request, db: Session = Depends(get_db)):
    polozka_id = funkce_db.vsechny_polozky(db)
    return templates.TemplateResponse("polozka.html", {"request": request, "polozka_id": polozka_id})
