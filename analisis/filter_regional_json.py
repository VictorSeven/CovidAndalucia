import numpy as np 
import pandas as pd
import json
from urllib.request import urlopen
import ssl
from datetime import date 

#Unsafe, but my network knowledge is so limited I don't know how to properly get a SSL certificate at the local level :(
unverfiedssl = ssl._create_unverified_context()

#Where the data is
#url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/39464"

url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/38667"
output_data = "../data/daily/granada-day-{0}".format(date.today().strftime("%d-%m-%Y"))


#Download it...
with urlopen(url, context=unverfiedssl) as url_json:
    json_data = json.load(url_json)

#...and save it for the future...
with open(output_data + ".json", 'w') as f:
    print(json_data, file=f)

#Note: the JSON format is the following. There is 4 keys, metainfo, measures, hierarchies, and data.
#metainfo contains some commentary about the data, such as missing days, links or any problems.
#measures include the column headers
#hierarchies include the level of the place (is it a big city or a small region?)
#data contains all the data...
#The value of each key is an array, where each element is itself a dictionary with information to be displayed on
#the webpage. We will just take the raw values and save them to a pandas dataframe, generating a CSV as always.

#Get the column names, which are stored in the measures dict...
ncols = len(json_data["measures"])
header_names = [json_data["measures"][k]["des"].replace(" ", "_") for k in range(ncols)]
header_names = ["Territorio"] + header_names


#...and prepare a dictionary to store all the data
data = []

#Then read the data
nplaces = len(json_data["data"]) #Number of regions

for place in json_data["data"]:
    place_name = place[0]["des"]

    #place[1] is just the year, 2020; we can dismiss it.

    poblacion = place[2]["val"]
    if poblacion != "":
        poblacion = int(float(poblacion))
        confirmados_pdia = place[3]["val"]
        if confirmados_pdia != "":
            confirmados_pdia = int(float(confirmados_pdia))
            confirmados_14 = int(float(place[4]["val"]))
            tasa_14 = float(place[5]["val"])
            confirmados_7 = int(float(place[6]["val"]))
            total_conf = int(float(place[7]["val"]))
            curados = int(float(place[8]["val"]))
            fallecidos = int(float(place[9]["val"]))
    else:
        poblacion = 0
        confirmados_pdia = int(float(place[3]["val"]))
        confirmados_14 = int(float(place[4]["val"]))
        tasa_14 = 0
        confirmados_7 = int(float(place[6]["val"]))
        total_conf = int(float(place[7]["val"]))
        curados = int(float(place[8]["val"]))
        fallecidos = int(float(place[9]["val"]))

    data.append([place_name, poblacion, confirmados_pdia, confirmados_14, tasa_14, confirmados_7, total_conf, curados, fallecidos])

#Writhe the data to a file
df = pd.DataFrame(data=data, columns=header_names)
df.set_index("Territorio", inplace=True)
df.to_csv(output_data + ".csv")

