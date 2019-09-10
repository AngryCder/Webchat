import socket
import cv2
from PIL import Image,ImageTk
import pickle
import sounddevice as sd
import numpy as np
import multiprocessing as mp
import tkinter as tk

#create the local server

Local_Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Local_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Local_Server.listen(5)

#

#global values
global user_picture = None
global client_picture = None

global user_voice = None
global client_voice = None

global current_connection = None
#

# arrays for handling incoming requests

Incoming_request_socket_array = []
Incoming_request_address_array = []

#

#appplication window fit to the screen
Application_Window = tk.Tk()

width, height = Application_Window.winfo_screenwidth(), Application_Window.winfo_screenheight()

Application_Window.geometry('%dx%d+0+0' % (width,height))

#

#drop down menu listing the incoming requests

menu = Menu(Application_Window)
Application_Window.config(menu=menu)
Incoming = Menu(menu)
menu.add_cascade(label='Incoming requests', menu=Incoming)

#
#
error_indicator = ''
error_label = Label(Application_Window,error_indicator)
#
# Entry for address required to make an outgoing requests


ip_enter = Entry(Application_Window)
port_enter = Entry(Application_Window)
make_call_button =  Button(Application_Window,text = 'make call' ,command = make_call)

#


#function to handel the serialization and deserialization of transmitted and recived data

def recive_serialized_data_and_deserialize(sock):
    serialized_data = b""

    serialized_len = sock.recv(128)
    length = pickle.loads(serialized_len)

    while length > 0:
        if length < 1024:
            packet = sock.recv(length)
        else:
            packet = sock.recv(1024)

        if not packet:
            break

        serialized_data += packet
        length -= len(packet)


    data = pickle.loads(serialized_data)
    client_picture = data['image_array']
    client_voice = data['audio_array']


def send_serialized_data(sock,image,audio):
      data = {'image_array':image,'audio_array':audio}
      try:
        serialized_img = pickle.dumps(data)
        serialized_len = pickle.dumps(len(data))
        sock.sendall(serialized_len)
        sock.sendall(serialized_img)

      except:
        error_indicator = ""

#

# a function to reply too incoming requests


def lift_call(sock,img,audio):
    while True :
        try:
           recive_serialized_data_and_deserialize = Process(recive_serialized_data_and_deserialize,(sock,))
           send_serialized_data = Process(send_serialized_data, ((sock,img,audio),))
           recive_serialized_data_and_deserialize.start()
           send_serialized_data.start()
           recive_serialized_data_and_deserialize.join()
           send_serialized_data.join()

        except socket.timeout :
            error_indicator = "call timed out"

def ear():
    Incoming_request_socket,Incoming_request_address = Local_server.accept()
    Incoming_request_socket_array.append(Incoming_request_socket)
    Incoming_request_address_array.append(Incoming_request_address)
    Incoming.add_command(label= Incoming_request_address, command= lift_call(Incoming_request_address))

def make_call():
   ip_address = ip_enter.get()
   port =int(port_enter.get()
   ip = (ip_address,port)
   def caller(address):
       Local_server.connect(address)

   try:
       calling_thread = Process(caller(),ip)
       calling_thread.start()
       calling_thread.join()


   except ConnectionRefusedError :
           error_indicator = 'outgoing request denied'


   except socket.gaierror :
       error_indicator = 'address error'


def show_picture(cv2image):
    if cv2image == None :
        img = Image.fromarray([1,0,1])
        imgtk = ImageTk.PhotoImage(image=img)
    else:
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

def End_call(sock):
        ind = Incoming_request_socket_array.index()
        Incoming_request_socket_array.pop(ind)
        Incoming_request_address_array.pop(ind)
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

def mouth(recived_audio):
         audio_to_be_sent = sd.playrec(recived_audio,cv2.CAP_PROP_FPS,channels = 2)
         user_voice = audio_to_be_sent

if __name__ == '__main__':
    while 1:
        ear_thread = Process(ear(),)
        ear_thread.start()
        ear_thread.join()
        ear_thread
