import socket
import json
import pickle
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0',1026))
s.listen(5)
host='192.168.1.120'
while True:
    s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1.connect((host,1030)) # connecting to publisher
    s1.sendall(bytes('rover_image','utf-8'))
    rover_data=s1.recv(8192).decode('utf-8') # getting the information from publisher
    clt,adr=s.accept()
    api_results={}
    data = clt.recv(200).decode('utf-8') # receiving the subscription information
    data=data.split(',')
    if data[0]!='server':
        for topic in data :
            if(topic=='rover_image'):
                api_results['rover_image']=rover_data
            if(topic=='earth_image'):
                s2=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # establishing the connection with other broker
                s2.connect((host,1025))
                s2.sendall(bytes('server','utf-8'))
                msg=s2.recv(1024) # receiving information from the broker 
                api_results['earth_image']=msg.decode('utf-8')
            if(topic=='astronomy_picture'):
                s3=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # establishing the connection with other broker
                s3.connect((host,1024))
                s3.sendall(bytes('server','utf-8'))
                msg=s3.recv(1024) # receiving information from the broker 
                api_results['astronomy_picture']=msg.decode('utf-8')
            api_pickle=pickle.dumps(api_results)
            clt.sendall(api_pickle)
    else:
        clt.sendall(bytes(rover_data,"utf-8"))
