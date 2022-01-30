from flask import Flask

app = Flask(__name__)
 
from flask import render_template, request, redirect    
import pickle

import json
currency = '''{"table": [{"currency":"dolar amerykański","code":"USD","bid":4.0396,"ask":4.1212},{"currency":"dolar australijski","code":"AUD","bid":2.8613,"ask":2.9191},{"currency":"dolar kanadyjski","code":"CAD","bid":3.1871,"ask":3.2515},{"currency":"euro","code":"EUR","bid":4.5084,"ask":4.5994},{"currency":"forint (Węgry)","code":"HUF","bid":0.012645,"ask":0.012901},{"currency":"frank szwajcarski","code":"CHF","bid":4.3411,"ask":4.4287},{"currency":"funt szterling","code":"GBP","bid":5.4135,"ask":5.5229},{"currency":"jen (Japonia)","code":"JPY","bid":0.035034,"ask":0.035742},{"currency":"korona czeska","code":"CZK","bid":0.1847,"ask":0.1885},{"currency":"korona duńska","code":"DKK","bid":0.6057,"ask":0.6179},{"currency":"korona norweska","code":"NOK","bid":0.4521,"ask":0.4613},{"currency":"korona szwedzka","code":"SEK","bid":0.4327,"ask":0.4415},{"currency":"SDR (MFW)","code":"XDR","bid":5.5959,"ask":5.7089}]}'''

data_code = json.loads(currency)

przelicznik = dict()

for i in data_code['table']:
    name = i['code']
    cena = i['ask']
    przelicznik[name] = cena

from werkzeug.datastructures import MultiDict

@app.route('/kalkulator', methods=['GET', 'POST'])
def wybor_waluty():
    przeli = {'USD': 4.1212, 'AUD': 2.9191, 'CAD': 3.2515, 'EUR': 4.5994, 'HUF': 0.012901, 'CHF': 4.4287, 'GBP': 5.5229, 'JPY': 0.035742, 'CZK': 0.1885, 'DKK': 0.6179, 'NOK': 0.4613, 'SEK': 0.4415, 'XDR': 5.7089}
    
    if request.method == "GET":
        return render_template("wybor_waluty.html", przeli=przeli)
    elif request.method == "POST":
        data = MultiDict(request.form)
        symbol = data['waluta_name'] 
        data_ilosc = data.get('ilosc_waluty')
        koszt = przeli[symbol]
        wartosc = float(koszt) * float(data_ilosc)
        with open("waluty.pickle", 'wb') as f:
            pickle.dump(wartosc, f)
        
        return redirect("/kalkulator/ilosc")
        


@app.route('/kalkulator/ilosc', methods=['GET', 'POST'])
def jaka_ilosc():
  with open("waluty.pickle", "rb") as f:
    wartosc = pickle.load(f)
    wartosc_dobra = round(wartosc, 2)
    
  return render_template("jaka_ilosc.html", wartosc_dobra=wartosc_dobra)
    


        
    

