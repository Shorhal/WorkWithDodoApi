import requests
import gspread
import logging


def getJsonRequests(url):
    try:
        request = requests.get(url).json()
    except ConnectionError:
        raise ConnectionError("Can't connect")
        logging.exception("Can't get")
    return request

belarus = getJsonRequests('https://globalapi.dodopizza.com/api/v1/pizzerias/all/112')
nigeria = getJsonRequests('https://globalapi.dodopizza.com/api/v1/pizzerias/all/566')


def uploadToGTable(serviceAccount, tableName, data):
    gc = gspread.service_account(filename=serviceAccount)

    sh = gc.open(tableName)
    sh.sheet1.clear()
    sh.sheet1.update(data)


def getPizzeriasList(json) -> list:
    pizzerias = []
    pizzerias.append(['Country', 'City', 'Name'])
    pizzeria = []
    for country in json['countries']:
        for pizzas in country['pizzerias']:
            pizzeria = [country['countryName'], pizzas['name'], pizzas['alias']]
            pizzerias.append(pizzeria)
    return pizzerias


belarusPizzerias = getPizzeriasList(belarus)
nigeriaPezzerias = getPizzeriasList(nigeria)
allPizzerias = belarusPizzerias+nigeriaPezzerias
print(allPizzerias)

uploadToGTable('ringed-trail-360313-722fa45f047d.json', "DodosPizzas", allPizzerias)