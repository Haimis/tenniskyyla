from flask import Flask
from flask import render_template
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta

app = Flask(__name__)

baseUrl = 'https://meilahti.slsystems.fi/booking/booking-calendar?BookingCalForm%5Bp_laji%5D=1&BookingCalForm%5Bp_pvm%5D='
baseUrl2 = 'https://varaukset.talintenniskeskus.fi/booking/booking-calendar?BookingCalForm%5Bp_laji%5D=5=1&BookingCalForm%5Bp_pvm%5D='

def createDates():
    days = []
    for i in range(3):
        today = date.today()
        day = today + timedelta(days=i)
        days.append(day)
    return days

def findFreeTimes(days):
    freeTimes = {}
    freeTimes['Meikku'] = {}
    freeTimes['Taivis'] = {}
        
    #iterate Meikku
    for day in days:
        free = {}
        res = requests.get(baseUrl+str(day))
        body = res.text

        soup = BeautifulSoup(body, 'html.parser')

        cells = soup.find_all(class_='s-avail')
        for cell in cells:
            link = str(cell.a).split('\"')[1]
            link = 'https://meilahti.slsystems.fi/'+link
            free[str(cell.a.text).replace('Varaa', '')] = link

        freeTimes['Meikku'][day] = free



    #iterate Taivis
    for day in days:
        free = {}
        res = requests.get(baseUrl2+str(day))
        body = res.text

        soup = BeautifulSoup(body, 'html.parser')

        cells = soup.find_all(class_='s-avail')
        for cell in cells:
            link = str(cell.a).split('\"')[1]
            link = 'https://varaukset.talintenniskeskus.fi/'+link
            free[str(cell.a.text)] = link

        freeTimes['Taivis'][day] = free

    return freeTimes


@app.route('/')
def index():
    days = createDates()
    freeTimes = findFreeTimes(days)

    return render_template('index.html', free=freeTimes)