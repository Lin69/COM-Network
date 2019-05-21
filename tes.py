import serial
import threading
import time
import frames
from tkinter import messagebox, END




class SendingThread(threading.Thread):

    def __init__(self, manager):

        threading.Thread.__init__(self,target=self.sending)
        self.manager = manager
        self.alive = True
        self.is_sending = False
        self.message = None
        self.is_paused = False
        self.sleep_time = 0
        self.i=0

    def sending(self):

        while self.alive:
            if self.is_sending:
                print('started sending from manager')
                self.i=0
                is_sended=False
                while self.i < len(self.manager.framelist):
                    if not self.is_paused:
                        if is_sended:
                            if self.manager.answer:
                                if self.manager.issucc:
                                    self.i+=1
                                    self.manager.answer = False
                                    is_sended = False
                                else: 
                                    is_sended = False
                        else:
                            is_sended = True
                            if self.manager.framelist[self.i]=='U' or self.manager.framelist[self.i]=='A' or self.manager.framelist[self.i]=='L' or  self.manager.framelist[self.i]=='N':
                                self.manager.answer=True
                                self.manager.issucc=True
                            else:
                                self.manager.answer = False
                            time.sleep(self.sleep_time)
                            self.manager.COMport.write(self.manager.framelist[self.i])
                self.is_sending=False
                self.manager.framelist = []
            pass

    
        
class ReadingThread(threading.Thread):

    def __init__(self, manager):
        threading.Thread.__init__(self, target=self.reading)
        self.manager = manager
        self.alive = True
        self.is_reading = False
        self.message = None

    def reading(self):
        while self.alive:
            if self.is_reading:
                self.message = self.manager.COMport.read()
                if len(self.message) > 0:
                    print('msg:', self.message, len(self.message))
                    self.manager.making_answer(self.message)
                time.sleep(1)
        print('thread is not alive')

class CheckConnection(threading.Thread):

    def __init__(self,manager):
        threading.Thread.__init__(self,target=self.checking)
        self.manager = manager
        self.alive = True
        # self.is_connected=False

    def checking(self):

        while self.alive:
            time.sleep(10)
            if self.manager.is_connected:
                dsr = self.manager.COMport.ser.dsr
                if not dsr:
                    messagebox.showinfo('','Подключение потеряно')
                    self.manager.change_port()
                    self.manager.is_connected = False

class Manager:

    def __init__(self):

        self.SendingThread = SendingThread(self)
        self.ReadingThread = ReadingThread(self)
        self.CheckingThread = CheckConnection(self)
        self.is_connected = True
        self.header = False
        self.headername =''
        self.infframes = []
        self.got_text = ''
        self.gotmessage = False


        self.change_status_label = None
        self.params_button=None
        self.is_file_opened = False
        self.view_file = None
        self.save_button = None


        self.COMport = None
        self.issucc = True
        self.answer = False
        self.framelist = []
        # self.connected = False

    def making_list(self,filename,info):

        frame_list=[]
        fr = frames.Frames()
        frame_list.append(fr.create_frame('H',filename))

        i = 0
        while i*15+14 < len(info):
            frame_list.append(fr.create_frame('I',info[i*15:i*15+15]))
            i+=1
        if len(info[i*15:])>0:
            frame_list.append(fr.create_frame('I',info[i*15:]))
        frame_list.append(fr.create_frame('H',''))

        self.framelist = frame_list

    def making_answer(self,frame):

        fr = frames.Frames()
        decoded_fr=fr.deconstract_frame(frame)

        if decoded_fr[0] == 'L':
            self.is_connected=True
            self.change_status_label['text'] = 'установлено'
            self.change_status_label['fg'] = 'green'

        elif decoded_fr[0] == 'U':
            messagebox.showinfo('Подключение','Подключение разорвано с другой стороны')
            self.is_connected=False
            self.change_port()
            self.change_status_label['text'] = 'не установлено'
            self.change_status_label['fg'] = 'red'
        elif decoded_fr[0] == 'A':
            self.issucc=True
            self.answer=True
        elif decoded_fr[0] == 'N':
            self.issucc=False
            self.answer=True
        elif decoded_fr[0] == 'I': 
            self.infframes.append(decoded_fr[1])
            self.framelist.append('A')
            self.sending()
        elif decoded_fr[0]=='H':
            if not self.header:
                self.header = True
                self.headername=decoded_fr[1]
            else:
                self.header = False
                self.got_text=fr.tosingle_string(self.infframes)
                self.gotmessage = True
                self.save_button['state'] = 'normal'
                self.view_file.configure(state='normal')
                self.view_file.delete(1.0, END)
                self.view_file.insert(END, self.got_text)
                self.view_file.configure(state='disabled')
            self.framelist.append('A')
            self.sending()
        else:
            self.framelist.append('N')
            self.sending()




    def connect(self,dev_port='COM1',speed=50,timeout = None, stopbits=1):
        self.COMport = COMConnection(self,dev_port=dev_port,speed=speed, timeout=timeout,stopbits=stopbits)
        self.COMport.open()
        self.start_threads()

    
    def start_threads(self): 

        try:
            self.SendingThread.start()
            self.ReadingThread.start()
            self.CheckingThread.start()
        except:
            pass
        self.ReadingThread.is_reading=True
        print('set is_reading')

    def quit_threads(self):

        self.SendingThread.alive=False
        self.ReadingThread.alive=False
        self.CheckingThread.alive=False


    def sending(self):
        
        self.SendingThread.is_sending=True

        # while self.SendingThread.alive:
        #     if self.SendingThread.is_sending:
        #         self.SendingThread.i=0
        #         is_sended=False
        #         while self.SendingThread.i < len(self.framelist):
        #             if not self.SendingThread.is_paused:
        #                 if is_sended:
        #                     if self.answer:
        #                         if self.issucc:
        #                             self.i+=1
        #                             self.answer = False
        #                             is_sended = False
        #                         else: 
        #                             is_sended = False
        #                 else:
        #                     is_sended = True
        #                     if self.framelist[self.SendingThread.i]=='U' or self.framelist[self.SendingThread.i]=='A' or self.framelist[self.SendingThread.i]=='L' or  self.framelist[self.SendingThread.i]=='N':
        #                         self.answer=True
        #                         self.issucc=True
        #                     else:
        #                         self.answer = False
        #                     time.sleep(self.SendingThread.sleep_time)
        #                     self.COMport.write(self.framelist[self.SendingThread.i])
        #         self.SendingThread.is_sending=False
        #         manager.framelist = []               
                
    def exit(self):
        self.quit_threads()
        self.COMport.disconnect()
    
    def change_port(self):
        self.COMport.disconnect()
        self.change_status_label['text'] = 'не установлено'
        self.change_status_label['fg'] = 'red'

class COMConnection:

    def __init__(self, manager,dev_port='COM1',speed=9600, timeout = None,stopbits = 1):

        self.ser=serial.Serial()
        self.ser.baudrate=speed
        self.ser.port=dev_port
        self.ser.write_timeout=timeout+5
        self.ser.timeout=timeout
        if stopbits == 1:
            self.ser.stopbits = serial.STOPBITS_ONE
        elif stopbits == 1.5:
            self.ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else: 
            self.ser.stopbits = serial.STOPBITS_TWO
        self.ser.dsrdtr = True

    def open(self):

            self.ser.open()

    def disconnect(self):

        self.ser.close()

    def read(self):

        line=bytes()
        while self.ser.inWaiting() > 0:
            line += bytes(self.ser.read())  # let's read
        line = line.decode("utf-8")
        print('line after', line)
        return line

    def write(self,message):
        print('starting write msg:', message)
        self.ser.write(message.encode("utf-8"))

    def status(self):

        if self.ser.is_open:
            return True
        else: 
            return False

