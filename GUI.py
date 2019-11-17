class GUI(server):

    def __init__(self, arg):
        self.server = arg
        self.Application_Window = tk.Tk()
        self.width = Application_Window.winfo_screenwidth()
        self.height = Application_Window.winfo_screenheight()
        self.Application_Window.geometry('%dx%d+0+0' % (self.width,self.height))
        self.m3nu = tk.Menu(self.Application_Window)
        self.Application_Window.config(menu=self.m3nu)
        self.Incoming = tk.Menu(self.m3nu)
        self.menu.add_cascade(label='Incoming requests', menu=self.Incoming)
        self.error_indicator = ''
        self.error_label = tk.Label(self.Application_Window,self.error_indicator)
        self.ImageMain = self.show_picture()
        self.ip_enter = tk.Entry(Application_Window)
        self.port_enter = tk.Entry(Application_Window)
        self.make_call_button =  tk.Button(Application_Window,text = 'make call' ,command = self.make_call)

    def show_picture(cv2image):
        if cv2image == None :
            img = Image.fromarray([1,0,1])
            imgtk = ImageTk.PhotoImage(image=img)
        else:
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

    def ear():
        self.Incoming_request_socket,self.Incoming_request_address = server.accept()
        self.Incoming_request_socket_array.append(Incoming_request_socket)
        self.Incoming_request_address_array.append(Incoming_request_address)
        self.Incoming.add_command(label= Incoming_request_address, command= lift_call(Incoming_request_address))

    def make_call(self):
       ip_address = ip_enter.get()
       port =int(port_enter.get())
       ip = (ip_address,port)
       self.server.connect(address)

    def End_call(sock):
            ind = Incoming_request_socket_array.index()
            Incoming_request_socket_array.pop(ind)
            Incoming_request_address_array.pop(ind)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

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
