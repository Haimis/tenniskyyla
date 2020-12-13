import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta


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
    for day in days:
        print('Vapaat vuorot {}:'.format(day))
        print('Meikku')
        res = requests.get(baseUrl+str(day))
        body = res.text

        soup = BeautifulSoup(body, 'html.parser')

        cells = soup.find_all(class_='s-avail')
        for cell in cells:
            link = str(cell.a).split('\"')[1]
            link = 'https://meilahti.slsystems.fi/'+link
            print(cell.a.text, link)

        print('Taivallahti')
        res = requests.get(baseUrl2+str(day))
        body = res.text

        soup = BeautifulSoup(body, 'html.parser')

        cells = soup.find_all(class_='s-avail')
        for cell in cells:
            hour = str(cell.a.text).replace(' ', ':').split(':')
            if int(hour[1]) < 22 and int(hour[1]) >= 7:
                link = str(cell.a).split('\"')[1]
                link = 'https://meilahti.slsystems.fi/'+link
                print(cell.a.text, link)

days = createDates()
findFreeTimes(days)
