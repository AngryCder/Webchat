class Vid_and_Aud(object):

    def __init__(self, arg):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.arg = arg
    def vid_frame(arg):
        if self.vid.isOpened():
            ret,frame = ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return(ret,None)
        else:
            return(ret,None)

    def mouth(recived_audio):
             audio_to_be_sent = sd.playrec(recived_audio,cv2.CAP_PROP_FPS,channels = 2)
             user_voice = audio_to_be_sent

     def __del__(self):
           if self.vid.isOpened():
               self.vid.release()
