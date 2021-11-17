import socket
import json
import pickle
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0',1024)) # establishing the connectio at port 1024
s.listen(5)
host='192.168.1.120'
while True:
    s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1.connect((host,1030)) # connecting to publisher
    s1.sendall(bytes('astronomy_picture','utf-8'))
    astronomy_data=s1.recv(1024).decode('utf-8') # getting the information from publisher
    clt,adr=s.accept()
    api_results={}
    data = clt.recv(200).decode('utf-8') # receiving the subscription information
    data=data.split(',')

    if data[0]!='server':
        for topic in data :
            if(topic=='astronomy_picture'):
                api_results['astronomy_picture']=astronomy_data
            if(topic=='earth_image'):
                s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # establishing the connection with other broker
                s2.connect((host,1025))
                s2.sendall(bytes('server','utf-8'))
                msg=s2.recv(1024) # receiving information from the broker 
                #s2.close()
                api_results['earth_image']=msg.decode('utf-8')  
            if(topic=='rover_image'):
                s3=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # establishing the connection with other broker
                s3.connect((host,1026))
                s3.sendall(bytes('server','utf-8'))
                msg=s3.recv(4096) # receiving information from the broker 
                #s3.close()
                api_results['rover_image']=msg.decode('utf-8') 
            #print(api_results)
            api_pickle=pickle.dumps(api_results)
            clt.sendall(api_pickle)
    else:
        clt.sendall(bytes(astronomy_data,'utf-8'))
