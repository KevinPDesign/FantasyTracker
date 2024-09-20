import requests
from bs4 import BeautifulSoup as bs
import  pandas as pd

def obtener_datos_fantasy():
    url = 'https://https://fantasy.nfl.com/league/9616457/team/8'
    response = request.get(url)
    soup = bs(response.content, 'html.parser')

jugadores = soup.find_all('div', class='')