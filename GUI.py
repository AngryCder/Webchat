import socket
import ssl
import cv2
from PIL import Image,ImageTk
from moviepy.editor import *
import pickle
import wave
import pyaudio
import numpy as np
import threading as th
import tkinter as tk

class server():

    def __init__(self, arg):
        self.arg = arg
        self.Local_Server_incoming = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Local_Server_outgoing = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Incoming_request_socket_array = None
        self.Incoming_request_address_array = None



    def create_server(self,address_in):
        self.Local_Server_incoming.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Local_Server_outgoing.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Local_Server_incoming.bind(address_in)
        self.Local_Server_incoming.listen(1)

    def connector(self):
         print("wiat")
         while True:
             sock,addr = self.Local_Server_incoming.accept()
             print(addr)
             self.Incoming_request_socket = sock
             self.Incoming_request_address = addr

class Aud_Vid():

    def __init__(self, arg):
        self.video = cv2.VideoCapture(0)
        self.CHUNK = 1470
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
        self.instream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,input=True,frames_per_buffer=self.CHUNK)
        self.outstream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,output=True,frames_per_buffer=self.CHUNK)


    def sync(self):
          with concurrent.futures.ThreadPoolExecutor() as executor:
                  tv = executor.submit(self.video.read)
                  ta = executor.submit(self.instream.read,1470)
                  vid = tv.result()
                  aud = ta.result()
                  return(vid[1],aud)



class GUI(server,Aud_Vid):

    def __init__(self, networks, graphics):
        self.server = networks
        self.avi = graphics
        self.Application_Window = tk.Tk()
        self.Application_Window.title("WebChat")
        self.width = self.Application_Window.winfo_screenwidth()
        self.height = self.Application_Window.winfo_screenheight()
        self.para = self.server.Incoming_request_address_array
        self.Application_Window.geometry('%dx%d+0+0' % (self.width,self.height))
        self.m3nu = tk.Menu(self.Application_Window)
        self.Application_Window.config(menu=self.m3nu)
        self.Incoming = tk.Menu(self.m3nu)
        self.m3nu.add_cascade(label='Incoming requests', menu=self.Incoming)
        self.error_indicator = 'status'
        self.error_label = tk.Label(self.Application_Window,text=self.error_indicator)
        imgop = Image.open("pico_img.png")
        img = ImageTk.PhotoImage(imgop)
        self.ImageMain = tk.Label(self.Application_Window,image = img)
        self.ImageMain.image = img
        imgop1 = Image.open("lenna.png")
        img1 = ImageTk.PhotoImage(imgop1)
        self.ImageRecv = tk.Label(self.Application_Window,image = img1)
        self.ImageRecv.image = img1
        self.ip_enter = tk.Entry(self.Application_Window)
        self.port_enter = tk.Entry(self.Application_Window)
        self.make_call_button =  tk.Button(self.Application_Window,text = 'make call' ,command = self.make_call)
        self.end_call_button =  tk.Button(self.Application_Window,text = 'end call' ,command = self.end_call)
        self.lift_call_button =  tk.Button(self.Application_Window,text = 'lift_call' ,command = self.lift_call)
        self.ip_enter.grid(row=0, column=1)
        self.port_enter.grid(row=1, column=1)
        self.make_call_button.grid(row=3, column=1)
        self.lift_call_button.grid(row=3, column=2)
        self.error_label.grid(row=4, column=1)
        self.ImageMain.grid(row=5, column=1)
        self.ImageRecv.grid(row=5,column=3)
        self.end_call_button.grid(row = 6 , column =1)
        self.tshopic = th.Thread(target=self.show_picture)
        self.tcon = th.Thread(target=self.server.connector)
        self.tshopic.start()
        self.tcon.start()

    def show_picture(self):
        ret,frame = self.avi.video.read()
        pi = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pic =  cv2.flip(pi,1)
        img = Image.fromarray(pic)
        ima = ImageTk.PhotoImage(img)
        self.ImageMain.configure(image = ima)
        self.ImageMain.image = ima
        self.ImageMain.after(1,self.show_picture)

    def show_recv(self,frame):
        pi = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pic =  cv2.flip(pi,1)
        img = Image.fromarray(pic)
        ima = ImageTk.PhotoImage(img)
        self.ImageRecv.configure(image = ima)
        self.ImageRecv.image = ima
        self.ImageRecv.after(1,self.show_recv)


    def play_recv(self,frames,aud):
       with concurrent.futures.ThreadPoolExecutor() as executor:
               show = executor.submit(self.show_recv,frames)
               hear = executor.submit(self.avi.outstream.write,aud)
               vid = show.result()
               aud = hear.result()


    def make_call(self):
       ip_address = self.ip_enter.get()
       port =int(self.port_enter.get())
       ip = (ip_address,port)
       self.server.Local_Server_outgoing.connect(ip)
       print(ip)
       self.error_indicator =" connected"


    def padding(self,arg):
        a = len(arg)
        if a == 16:
            return arg
        elif a <16:
            arg =arg + ((b'\x00')*(16-a))
            return arg



    def end_call(self,sock):
            ind = self.server.Incoming_request_socket_array.index(sock)
            self.m3nu.delete(self.Incoming_request_address_array[ind][0])
            self.server.Incoming_request_socket_array.pop(ind)
            self.server.Incoming_request_address_array.pop(ind)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    def send(self,sock):
        while True:
           ser_data =pickle.dumps(self.avi.sync())
           length = self.padding(ser_data)
           sock.sendall(length)
           sock.sendall(ser_data)

    def recived(self,sock,buffer):
        while True:
           ser_data = b""
           ser_len = client_socket.recv(16)
           length = pickle.loads(ser_len)
           if length > 0:
               if length < 4096:
                   packet = client_socket.recv(length)
               else:
                   packet = client_socket.recv(4096)

               ser_data += packet
               length -= len(packet)

           data = pickle.loads(ser_data)
           play_recv(data)

    def comms(self,sock):
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                        send = executor.submit(sock.sendall,data)
                        rec_v = executor.submit(seck.recv,1024)
                        vid = send.result()
                        aud = rec_v.result()

            except socket.timeout :
                error_indicator = "call timed out"





if __name__ == '__main__':
             cli = server("local")
             cli.create_server(("",80))
             avi = Aud_Vid("sound and sight")
             app = GUI(cli,avi)
             app.Application_Window.mainloop()
