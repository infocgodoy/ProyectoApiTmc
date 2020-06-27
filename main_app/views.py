import requests
import json
import datetime
from django.shortcuts import render
from datetime import date
import re

def home(request):

   fecha_actual=datetime.datetime.now()
   mensaje= 'Rellene todo los campos'
   return render(request, "main_app/home.html", {"mensaje": mensaje,"fecha": fecha_actual})

def resultado(request):   

   


   fecha_actual=datetime.datetime.now()
   
   if request.POST["tmc"] == '' or request.POST["dateIni"] == '' or request.POST["dateFin"] == '' or request.POST["uf"] == '':
      mensaje= 'Faltaron campos que rellenar'
      return render(request, "main_app/home.html", {"mensaje": mensaje,"fecha": fecha_actual})

   tmc = request.POST["tmc"]
   tmcArr = tmc.split('-')
   tmcMes = int(tmcArr[0])
   tmcAni = int(tmcArr[1])
   apikey = '9c84db4d447c80c74961a72245371245cb7ac15f'
   formato = 'json'
   response = requests.get('https://api.sbif.cl/api-sbifv3/recursos_api/tmc/%s/%s?apikey=%s&formato=%s' % (tmcMes,tmcAni,apikey,formato))      
   todos = response.json()
   arreglo = todos['TMCs']
   

   fecha_ini = request.POST["dateIni"]
   fecha_ini = fecha_ini.split('-')
   fecha_ini = date(int(fecha_ini[0]), int(fecha_ini[1]), int(fecha_ini[2]))

   fecha_fin = request.POST["dateFin"]
   fecha_fin = fecha_fin.split('-')
   fecha_fin = date(int(fecha_fin[0]), int(fecha_fin[1]), int(fecha_fin[2]))

   dias = fecha_fin - fecha_ini
   dias = dias + datetime.timedelta(days=1)

   uf = request.POST["uf"]
   OperacionesNacionales = '^Operaciones no reajustables en moneda nacional'   

   if dias.days > 90:
      DiasMasOMenos = '90 días o más$'

      if (int(uf) <= 50):
         ufStr = '^Inferiores o iguales al equivalente de 50'
      elif int(uf) <= 200:
         ufStr = '^Inferiores o iguales al equivalente de 200'
      elif int(uf) <= 5000:
         ufStr = '^Inferiores o iguales al equivalente de 5.000'
      else:
         ufStr = '^Superiores al equivalente de 5.000'
   else:
      DiasMasOMenos = 'menos de 90 días$'

      if int(uf) <= 5000:
         ufStr = '^Inferiores o iguales al equivalente de 5.000'
      else:
         ufStr = '^Superiores al equivalente de 5.000'

   valorEncontrado = ''

   for lista in arreglo: 
      tituloStr = str(lista["Titulo"])      
      subTituloStr = str(lista["SubTitulo"]) 

      if re.findall(OperacionesNacionales, tituloStr):
         if re.findall(DiasMasOMenos, tituloStr):
            if re.findall(ufStr, subTituloStr):
               valorEncontrado = lista["Valor"]          
               
   return render(request, "main_app/resultado.html", {"valorTmc":valorEncontrado,"fecha": fecha_actual})
