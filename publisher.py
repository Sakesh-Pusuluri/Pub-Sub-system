import socket
import time
import requests
from urllib.request import urlretrieve
import datetime
import json
import _thread 
from _thread import start_new_thread # for multi-threading
api = '3oUyHmeenW3WXHSVN004bu4qkHC6PvKU43GfykTJ' # api key to get the data

x = datetime.datetime.now() # function to get the today's date
d=x.strftime('%Y-%m-%d') # formatting date
today = datetime.date.today()
x = today - datetime.timedelta(days=0)
d=x.strftime('%Y-%m-%d')
yesterday = today - datetime.timedelta(days=3) # function to get yesterday's date

m = d.split('-')
y_t = yesterday.strftime('%Y-%m-%d').split('-')

mars_today = today - datetime.timedelta(days=1)
mars_yesterday = mars_today - datetime.timedelta(days=2)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # establishing connection
s.bind(('0.0.0.0',1030)) # binding to a specified port
s.listen(5)
def astronomyPicture(): 
  '''This function returns astronomy picture for that day'''
  url = "https://api.nasa.gov/planetary/apod"
  parameters = {
      'api_key':api,
      'date':d,
      'hd':'True'
  }
  resp = requests.get(url,params=parameters).json() 
  return resp['url']

def epicData():
  url = "https://api.nasa.gov/EPIC/api/natural/"
  parameters = {
      'api_key':api,
  }
  response = requests.get(url,params=parameters).json()
  return (response[0]['image'])

def epicImage():
  '''This function returns earth image'''
  y,m,d = y_t[0],y_t[1],y_t[2]
  img_id = epicData()
  url = "https://epic.gsfc.nasa.gov/archive/natural/"
  url = url + y +'/' + m + '/'+d
  url = url + '/png'
  url = url + '/' + img_id + '.png' 
  return (url)
def roverImages():
    '''This function will return rover images'''
    parameters = {"earth_date":mars_yesterday, "api_key":api}
    f = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"
    data_retrieved = requests.get(f, params = parameters)
    data_retrieved = json.loads(data_retrieved.text)
    for i in data_retrieved["photos"][0]:
        data_retrieved = data_retrieved["photos"][3]["img_src"]
        return data_retrieved

def multi_thread(conn,data,astronomy_data,earth_image,rover_image):
    if data =='astronomy_picture':
        #(f"Connection to {adr} established")
        clt.send(bytes(astronomy_data,'utf-8'))
        #print('data sent :',astronomy_data)
    if data =='earth_image':
        #print(f"Connection to {adr} established")
        clt.send(bytes(earth_image,'utf-8'))
        #print('data sent :',earth_image)
    if data =='rover_image':
        #print(f"Connection to {adr} established")
        clt.send(bytes(rover_image,'utf-8'))
        #print('data sent :',rover_image)
    time.sleep(10000)
    conn.close()

while True:
    astronomy_data = astronomyPicture() 
    earth_image=epicImage()
    rover_image=roverImages()
    clt,adr=s.accept()
    data = clt.recv(100).decode('utf-8') # receiving the response from the clients 
    start_new_thread(multi_thread, (clt,data,astronomy_data,earth_image,rover_image)) # multi threading for each client

    