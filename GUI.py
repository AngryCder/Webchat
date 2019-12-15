import socket
import cv2
from PIL import Image,ImageTk
import pickle
import wave
import pyaudio
import numpy as np
import threading as th
import tkinter as tk

class server():

    def __init__(self, arg):
        self.arg = arg
        self.Local_Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Incoming_request_address_array = []
        self.Incoming_request_socket_array =[]


    def create_server(self,address):
        self.Local_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Local_Server.bind(address)
        self.Local_Server.listen(5)

    def connector(self):
         print("wiat")
         while True:
             addr , sock = self.Local_Server.accept()
             self.Incoming_request_socket_array.append(sock)
             self.Incoming_request_address_array.append(addr)

class Aud_Vid():

    def __init__(self, arg):
        self.video = cv2.VideoCapture(0)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()
        self.instream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,input=True,frames_per_buffer=self.CHUNK)
        self.outstream = self.audio.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,output=True,frames_per_buffer=self.CHUNK)
        self.Aud_Inframes = []
        self.Aud_Outframes = []
        self.Vid_frames = []
        self.arg = arg

    def rec(self):
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = self.instream.read(CHUNK)
            self.Aud_frames.append(data)
    def vid(self):
        rec_time = 0
        while rec_time < RECORD_SECONDS :
                     start = time.time()
                     ret,img = self.video.read()
                     end = time.time()
                     self.Vid_frames.append(img)
                     rec_time = rec_time + end -start

    def play(self,out_frames):
        for data in out_frames :
            self.outstream.write(data)

    def play_rec(self,out_frames):
        p1 = th.Thread(target=self.play,args=(out_frames,))
        p2 = th.Thread(target=self.rec)
        p3 = th.Thread(target=self.vid)
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()

class GUI(server,Aud_Vid):

    def __init__(self, networks, graphics):
        self.server = networks
        self.avi = graphics
        self.Application_Window = tk.Tk()
        self.Application_Window.title("WebChat")
        self.width = self.Application_Window.winfo_screenwidth()
        self.height = self.Application_Window.winfo_screenheight()
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
        self.ip_enter.grid(row=0, column=1)
        self.port_enter.grid(row=1, column=1)
        self.make_call_button.grid(row=3, column=1)
        self.error_label.grid(row=4, column=1)
        self.ImageMain.grid(row=5, column=1)
        self.ImageRecv.grid(row=5,column=2)
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
        self.ImageMain.after(10,self.show_picture)

    def show_recv(self,frame):
        pi = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pic =  cv2.flip(pi,1)
        img = Image.fromarray(pic)
        ima = ImageTk.PhotoImage(img)
        self.ImageRecv.configure(image = ima)
        self.ImageRecv.image = ima
        self.ImageRecv.after(10,self.show_recv)

    def make_call(self):
       ip_address = self.ip_enter.get()
       port =int(self.port_enter.get())
       ip = (ip_address,port)
       self.server.Local_Server.connect(address)
       print(port)

    def end_call(self,sock):
            ind = self.server.Incoming_request_socket_array.index(sock)
            self.server.Incoming_request_socket_array.pop(ind)
            self.server.Incoming_request_address_array.pop(ind)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    def send(sock):
          data = {'image_array':self.ImageMain.image,'audio_array':self.avi.Aud_Inframes}
          try:
            serialized_img = pickle.dumps(data)
            sock.sendall(serialized_img)
          except:
              error_indicator = ""

    def recived(self,sock):
            serialized_data = b""
            while True:
                packet = sock.recv(1024)
                if not packet:
                    break
            data = pickle.loads(serialized_data)
            self.ImageRecv.configure(image = ima)
            self.ImageRecv = data['image_array']
            self.avi.Aud_Outframes = data['audio_array']

    def lift_call(self,sock):
        while True :
            try:
               psend = th.Thread(target=send,args=sock)
               precv = th.Thread(target=recived,arg=sock)
               psend.start()
               precv.start()
               psend.join()
               precv.join()
               self.avi.play_rec(self.Aud_Outframes)

            except socket.timeout :
                error_indicator = "call timed out"



if __name__ == '__main__':
             cli = server("local")
             cli.create_server(("127.0.0.1",80))
             avi = Aud_Vid("sound and sight")
             app = GUI(cli,avi)
             app.Application_Window.mainloop()
