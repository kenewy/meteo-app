

import requests

from datetime import datetime , timedelta # pour travailler avec les dates et les durées

from datetime import datetime , timedelta 

import json
from statistics import mean # pour calculer la moyenne 
from PIL import Image, ImageDraw, ImageFont, ImageColor # pour manipuler des images avec pillow 




 # Cette fonction parcourt la liste de données et remplace les valeurs nulles (None) par la valeur précédente non nulle



def dataclean(dataliste):
    for i in range(len(dataliste)):
        if(dataliste[i]==None):
            dataliste[i]=dataliste[i-1]
    return dataliste


presentday=datetime.today() # pour obtenir la date actuelle 
start_date=presentday.strftime("%Y-%m-%d") # pour convertir la date en format de chaine "%Y-%m-%d"
end_date = presentday + timedelta(4)
end_date=end_date.strftime("%Y-%m-%d")
j=[]
nj=[]
j.append(presentday)
nj.append(j[0].strftime("%A"))
for i in range(4):
  j.append(presentday + timedelta(i+1))
  nj.append(j[i+1].strftime("%A"))
print(nj)

n_start_date=presentday.strftime("%A")


print(start_date)
print(end_date)
# Construire l'URL de l'API météo en utilisant les dates de début et de fin ainsi que les paramètres requis
url="https://api.open-meteo.com/v1/meteofrance?latitude=43.61&longitude=3.87&hourly=cloud_cover&hourly=relativehumidity_2m&hourly=precipitation&hourly=temperature_2m&hourly=windspeed_10m&start_date="+start_date+"&end_date="+end_date

# Effectuer une requête GET à l'URL de l'API et récupérer le contenu de la réponse

response=requests.get(url).content.decode('utf-8')

data = json.loads(response) # Convertir les données de réponse JSON en un objet Python (dictionnaire)

# Extraire les différentes listes de données à partir de la réponse de l'API

temperatureliste=data["hourly"]["temperature_2m"] #  Liste des températures
windsliste=data["hourly"]["windspeed_10m"]   # Liste des vitesses du vent
precipitationliste=data["hourly"]["precipitation"]  # Liste des précipitations
relativehumidity=data["hourly"]["temperature_2m"] # Liste de l'humidité relative
cloud_cover=data["hourly"]["cloud_cover"] # Liste de la couverture nuageuse


temperatureliste=dataclean(temperatureliste)
windsliste=dataclean(windsliste)
precipitationliste=dataclean(precipitationliste)
relativehumidity=dataclean(relativehumidity)
cloud_cover=dataclean(cloud_cover)


maxtemp=[0,0,0,0,0]
mintemp=[0,0,0,0,0]
winds=[0,0,0,0,0]
precipitation=[0,0,0,0,0]
maxhumi=[0,0,0,0,0]
cloudj=[0,0,0,0,0]

# Boucle pour parcourir les données par tranche de 24 heures

for i in range(len(maxtemp)):
  maxtemp[i]=max(temperatureliste[24*i:24*(i+1)-1])
  mintemp[i]=min(temperatureliste[24*i:24*(i+1)-1])
  winds[i]=mean(windsliste[24*i:24*(i+1)-1])
  precipitation[i]=sum(precipitationliste[24*i +6:24*(i+1)-1 -6])
  maxhumi[0]=max(relativehumidity[24*i:24*(i+1)-1])
  cloudj[0]=mean(cloud_cover[24*i +6:24*(i+1)-1 -6])
  
# Affichage des résultats
print(mintemp)
print(maxtemp)
print(winds)
print(precipitation)
print(maxhumi)

precipitationn=[0,0,0,0]
cloudn=[0,0,0,0]
for i in range(len(cloudn)):
  cloudn[i]=mean(cloud_cover[18+24*i:18+12+24*i])
  precipitationn[i]=sum(precipitationliste[18+24*i:18+12+24*i])


# Définition des constantes C et L

C=70
L=310
# Ouverture des différentes images à utiliser dans le programme

img = Image.open("meteoback.jpg")
img_cloud=Image.open("cloud_p.jpg")
img_cloud2=Image.open("cloud2.jpg")
img_cloud3=Image.open("cloud3.jpg")
img_sun=Image.open("sun.jpg")

img_hum=Image.open("hum.jpg")
img_pres_nuit=Image.open("pluit_nuit.jpg")
img_croissant=Image.open("croissant.jpg")
img_cr_nua=Image.open("cr_nua.jpg")
img_nua_nuit=Image.open("nua_nuit.jpg")

draw = ImageDraw.Draw(img) # Crée un objet ImageDraw à partir de l'image img


# Chargement des polices à utiliser pour le texte
font = ImageFont.truetype("Gidole-Regular.ttf", size=50)
font1 = ImageFont.truetype("Gidole-Regular.ttf", size=30)
font2 = ImageFont.truetype("Gidole-Regular.ttf", size=20)
font3 = ImageFont.truetype("Gidole-Regular.ttf", size=34)


draw.text((C+20, 120), nj[0],font=font3, fill='black') # Ajout du texte correspondant aux jours de la semaine
for i in range(len(nj)-1):
    draw.text((C+20+170*(i+1), 140), nj[i+1],font=font1, fill='black')


for i  in range(len(maxtemp)):
  # Ajout des données météorologiques pour chaque jour
  draw.text((C+170*i, L), str(round(maxtemp[i],2))+"°C",font=font, fill='black')
  draw.text((C+10+170*i, L+50), str(round(mintemp[i],2))+"°C",font=font1, fill='black')
  draw.text((C+170*i, L+100), str(round(maxhumi[i],2))+"%",font=font1, fill='black')
  draw.text((C+10+170*i, L+140), str(round(precipitation[i], 2))+"mm",font=font1, fill='black')
  draw.text((C+10+170*i, L+180), str(round(winds[i], 2))+"Km/h",font=font2, fill='black')
  img.paste(img_hum.resize((30, 30)),(C+90+170*i, L+100),)
  if(precipitation[i]>2):
    img.paste(img_cloud.resize((100, 100)),(C+20+170*i, 190),)
  elif (25>cloudj[i]):
    img.paste(img_sun.resize((100, 100)),(C+20+170*i, 190),)
  elif (60>cloudj[i]):
    img.paste(img_cloud2.resize((100, 100)),(C+20+170*i, 190),)
  else:
    img.paste(img_cloud3.resize((100, 100)),(C+20+170*i, 190),)
for i in range(len(cloudn)) :# Ajout des icônes pour représenter les conditions météorologiques de nuit
  if(precipitationn[i]>2):
    img.paste(img_pres_nuit.resize((50, 50)),(C+125+170*i, 250),)
  elif (25>cloudn[i]):
    img.paste(img_croissant.resize((50, 50)),(C+125+170*i, 250),)
  elif (60>cloudn[i]):
    img.paste(img_cr_nua.resize((50, 50)),(C+125+170*i, 250),)
  else:
    img.paste(img_nua_nuit.resize((50, 50)),(C+125+170*i, 250),)

img = img.save("julteo.jpg") # Enregistre l'image modifiée avec les données météorologiques

