class server(object):

    def __init__(self, arg):
        self.arg = arg

    def create_server(arg):
        self.Local_Server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Local_Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Local_Server.bind(arg)
        self.Local_Server.listen(5)
        
