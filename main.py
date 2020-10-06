# -*- coding: utf-8 -*-
import json
import requests
from datetime import date
import schedule
import time
import re

url = "https://sistemas.df.gov.br/MTeste/screenservices/MTeste/Common/Inicio/ScreenDataSetGetAgendaByIsAtivo"
payload = {'versionInfo':{'moduleVersion':'KClf+PqAhZp2NPaFNjMdMw','apiVersion':'2mxpqQCjfxphi4QihXYSxQ'},'viewName':'Common.Inicio','screenData':{'variables':{'FilterData':'10/06/2020','TableSort':'','StartIndex':0,'MaxRecords':20}},'inputParameters':{'StartIndex':0,'MaxRecords':20}}
headers = {'content-type':'application/json; charset=utf-8', 'X-CSRFToken':'T6C+9iB49TLra4jEsMeSckDMNhQ='}

running = False

def sendRequest(data):
  payload['screenData']['variables']['FilterData'] = data
  r = requests.post(url, data=json.dumps(payload), headers=headers)
  return r

def verifyEmpty(jsonText):
  if not jsonText['data']['List']['List']:
    return True
  else:
    return False

def checkVagas(data):
  hasVaga = False
  r = sendRequest(data)
  print(r)
  j = json.loads(r.text)

  if not verifyEmpty(j):
    lista = j['data']['List']['List']
    for obj in lista:
      if obj['TotalVagasDisponiveis'] != '0':
        #sendText("HA VAGAS NA DATA:" + obj["Data"],True)
        #local = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]', '', obj['Nome'].decode('utf-8'))
        texto = "VAGA DATA: "+obj['Data']+" LOCAL: "+obj['Nome']+" QTD: "+obj['TotalVagasDisponiveis']
        sendText(texto, True)
        hasVaga = True
  else:
    hasVaga = True
    sendText("DATA: "+data+" NAO DIVULGADA", False)

  if not hasVaga:
    sendText("DATA: "+data+" SEM VAGAS", False)

def sendText(bot_message, check):
  print(bot_message)
  bot_token = "<put your token here>"
  bots_chatID = ["<number example>"]
  if check:
    for bot_chatID in bots_chatID:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text)
  #return response.json()

def run():
#  try:
  print("Executando")
  data = date.today()
  for i in range(3):
    fut = date.fromordinal(data.toordinal()+i)
    checkVagas(fut.strftime("%d/%m/%Y"))
  print("Finalizou")
#  except:
#    print("Erro na execucao")

run()

schedule.every().hour.do(run)
#schedule.every().minutes.do(run)

while True: 
  # Checks whether a scheduled task  
  # is pending to run or not 
  schedule.run_pending() 
  time.sleep(1) 
