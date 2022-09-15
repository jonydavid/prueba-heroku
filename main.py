from random import SystemRandom
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

class Item(BaseModel):
    ranking: int
    puesto_ant: int
    nombre: str
    puntos: int

@app.get("/api/v1/ranking_onlive")
def get_ranking():
    url = 'https://live-tennis.eu/en/atp-live-ranking'
    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html.parser")

    table = soup.find('table', attrs={'id': 'u868'})

    list = []   

    for i in table.find_all('tr', attrs={'class': 'dn'}):
        # combertir a json
        ranking = i.find('td', attrs={'class': 'rk'}).text
        puesto_ant = i.find('td', attrs={'class': 'chtd'}).text
        nombre = i.find('td', attrs={'class': 'pn'}).text
        puntos = i.find('td', attrs={'class': 'rdf'})
        if puntos:
            puntos = puntos.text

        list.append({'ranking': ranking, 'puesto_ant': puesto_ant, 'nombre': nombre, 'puntos': puntos})

    return list
    



