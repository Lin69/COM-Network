# from PIL import Image, ImageTk
from tkinter import Tk, Frame, BOTH, Button, Label, Menu, Text, StringVar, VERTICAL, Message, TOP, Y, Listbox, \
    Scrollbar, Toplevel, END
from tkinter import ttk
from tkinter.ttk import Style
from tkinter import filedialog
# from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter.messagebox import showerror
import time

# from tes import Manager


FONT_BIG = ('Sans', '14', 'bold')
FONT = ('Sans', '10', 'bold')
FONT_DOP = ('Sans', '12', 'bold')
COLOR = 'lightblue'
ACTIVE_BUTTON_COLOR = 'lime'
BUTTON_COLOR = 'lightgrey'
DOP_COLOR = 'lightyellow'


class MainWindow(Frame):
    def __init__(self,manager):
        # super().__init__()
        self.window = Tk()
        self.window.geometry('900x600')
        Frame.__init__(self, self.window, background=COLOR)
        # app1 = Settings(window)
        # self.window = window
        self.manager = manager
        self.init_ui()

        self.window.mainloop()

    def init_ui(self):
        self.window.title("Курсовая работа")
        self.style = Style()
        self.style.theme_use("default")
        self.window.resizable(False, False)
        self.pack(fill=BOTH, expand=1)
        self.center_window(900, 600, self.window)

        self.is_port_opened = False
        self.are_threads_going = False
        self.is_connected = False

        

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.quit_button = Button(self.window, text="Выход", height=2, width=15, command=self.on_exit, font=FONT,
                             activebackground=ACTIVE_BUTTON_COLOR, bg=BUTTON_COLOR)
        self.quit_button.place(x=750, y=550)
        self.send_label = Label(self.window, text="Файл", width=13, background=COLOR, font=FONT_BIG)
        self.send_label.place(x=600, y=10)

        self.send_label = Label(self.window, text="Отправка файла", width=13, background=COLOR, font=FONT_DOP)
        self.send_label.place(x=530, y=65)

        self.path_file_change = Text(self.window, width=25, height=1, state='disabled')
        self.path_file_change.place(x=530, y=110)

        self.send_button = Button(self.window, text="Выбрать файл", height=1, width=15, font=FONT,
                             activebackground=ACTIVE_BUTTON_COLOR, bg=BUTTON_COLOR, command=self.on_open)
        self.send_button.place(x=750, y=108)

        self.way_label = Label(self.window, text="Содержимое файла", width=20, background=COLOR, font=FONT)
        self.way_label.place(x=520, y=145)

        self.manager.view_file = Text(self.window, width=40, height=9, state='disabled')  # показывает содержимое файла
        self.manager.view_file.place(x=529, y=170)

        self.save_label = Label(self.window, text="Сохранение файла", width=20, background=COLOR, font=FONT_DOP)
        self.save_label.place(x=505, y=410)

        self.manager.params_button = Button(self.window, text="Отправить файл", height=2, width=20, font=FONT,
                               activebackground=ACTIVE_BUTTON_COLOR, bg=BUTTON_COLOR, state = 'disabled',command=self.send_file)
        self.manager.params_button.place(x=530, y=350)

        self.path_file_save = Text(self.window, width=25, height=1, state='disabled')
        self.path_file_save.place(x=530, y=452)

        self.manager.save_button = Button(self.window, text="Сохранить файл", height=1, width=15, font=FONT,
                             activebackground=ACTIVE_BUTTON_COLOR, bg=BUTTON_COLOR, command=self.save_file,state = 'disabled')
        self.manager.save_button.place(x=750, y=450)

        self.connection_label = Label(self.window, text="Соединение", width=10, background=COLOR, font=FONT_BIG)
        self.connection_label.place(x=140, y=10)

        self.status_label = Label(self.window, text="Статус соединения:", width=20, background=COLOR, font=FONT_DOP)
        self.status_label.place(x=20, y=65)

        self.manager.change_status_label = Label(self.window, text="не установлено", width=15, background=COLOR,
                                         font=FONT_DOP, fg='red')
        self.manager.change_status_label.place(x=210, y=65)

        self.parametrs = Label(self.window, text="Параметры соединения:", width=25, background=COLOR, font=FONT_DOP)
        self.parametrs.place(x=12, y=120)

        self.speed_label = Label(self.window, text="Скорость", width=15, background=COLOR, font=FONT_DOP, fg='green')
        self.speed_label.place(x=10, y=160)

        self.speed_var = StringVar()

        self.speed = ttk.Combobox(self.window, state='readonly', height=5, width=10, textvariable=self.speed_var)
        # self.speed['values'] = ('50', '75', '110', '134', '150', '200', '300', '600', '1200', '1800', '2400', '4800', '9600',
        #    '19200', '38400', '57600', '115200')
        self.speed['values'] = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                                19200, 38400, 57600, 115200)
        self.speed.set(9600)
        self.speed.place(x=260, y=162)
        self.speed.bind("<<ComboboxSelected>>", self.callback)

        self.sender_port_label = Label(self.window, text="COM-порт", width=20, background=COLOR, font=FONT_DOP,
                                  fg='green')
        self.sender_port_label.place(x=-14, y=200)

        self.sender_port_var = StringVar()

        self.sender_port = ttk.Combobox(self.window, state='readonly', height=5, width=10,
                                        textvariable=self.sender_port_var)
        self.sender_port['values'] = ('COM1', 'COM2')
        self.sender_port.set('COM1')
        self.sender_port.place(x=260, y=202)
        self.sender_port.bind("<<ComboboxSelected>>", self.callback)

        # recipient_port_label = Label(self.window, text="COM-порт получателя", width=20,  background=COLOR, font=FONT_DOP,
        #                              fg='green')
        # recipient_port_label.place(x=35, y=240)

        # self.recipient_port_var = StringVar()

        # self.recipient_port = ttk.Combobox(self.window, state='readonly', height=5, width=10, textvariable=self.recipient_port_var)
        # self.recipient_port['values'] = ('/dev/ttys1', '/dev/ttys2', '/dev/ttys3', '/dev/ttys4', '/dev/ttys5', '/dev/ttys6', '/dev/ttys7', '/dev/ttys8', '/dev/ttys9')
        # self.recipient_port.set("/dev/ttys2")
        # self.recipient_port.place(x=260, y=242)
        # self.recipient_port.bind("<<ComboboxSelected>>", self.callback)

        self.timeout_label = Label(self.window, text="Таймаут", width=10, background=COLOR, font=FONT_DOP, fg='green')
        self.timeout_label.place(x=28, y=240)

        self.timeout_var = StringVar()

        self.timeout = ttk.Combobox(self.window, state='readonly', height=5, width=10, textvariable=self.timeout_var)
        # self.timeout['values'] = ('None', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60')
        self.timeout['values'] = ('None', 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
        self.timeout.set(15)
        self.timeout.place(x=260, y=242)
        self.timeout.bind("<<ComboboxSelected>>", self.callback)

        self.stop_bits_label = Label(self.window, text="Стоп-биты", width=10, background=COLOR, font=FONT_DOP, fg='green')
        self.stop_bits_label.place(x=40, y=280)

        self.stop_bits_var = StringVar()

        self.stop_bits = ttk.Combobox(self.window, state='readonly', height=5, width=10,
                                      textvariable=self.stop_bits_var)
        self.stop_bits['values'] = (1, 1.5, 2)
        self.stop_bits.set(1)
        self.stop_bits.place(x=260, y=282)
        self.stop_bits.bind("<<ComboboxSelected>>", self.callback)

        self.set_button = Button(self.window, text="Установить соединение", height=2, width=20, font=FONT,
                                 activebackground='red', bg=BUTTON_COLOR, command=self.conn)
        self.set_button.place(x=48, y=380)

        pace = Label(self.window, text="Темп отправки", width=15, background=COLOR, font=FONT_DOP, fg='green')
        pace.place(x=30, y=320)
        self.pace_var = StringVar()
        self.pace = ttk.Combobox(self.window, state='readonly', height=5, width=10, textvariable=self.pace_var)
        self.pace['values'] = ('Приостановить', 'Быстро', 'Средне', 'Медленно')
        self.pace.set('Быстро')
        self.pace.place(x=260, y=322)
        self.pace.bind("<<ComboboxSelected>>", self.pace_callback)

        # TODO***********************************************************
        # if соединение установлено
        # set_button.configure(text='Прервать соединение')
        # ***************************************************************
        #  можно создавать кнопки только если соединение установлено

        # break_off_button = Button(self, text="Разорвать соединение", height=2, width=20, font=FONT,
        #                           activebackground='red', bg=BUTTON_COLOR, command=self.conn)
        # break_off_button.place(x=48, y=430)

        # *****************************************************************************************************
        # шаблон для изменения статуса соединения по флагу
        # if  какое-то событие
        # change_status_label['text'] = 'установлено'
        # *****************************************************************************************************

        # ******************************************************************
        # шаблон для оповещения пользователя об ошибках
        # if какое-то событие
        # messagebox.showerror('Ошибка!', 'Сообщение не доставлено')
        # ******************************************************************
        # self.manager.is_connected.bind("")
        self.menubar = Menu(self.window)
        self.window.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label="Справка", command=self.show_info)
        self.menubar.add_cascade(label="Меню", menu=self.file_menu)

        self.menu = Menu(self.window, tearoff=False)
        # self.menu.add_command(label="Соединение", command=self.show_info)
        self.menu.add_command(label="Справка", command=self.show_info)

        self.window.bind("<Double-Button-1>", self.show_menu)  # обработчик двойного левого клика мыши
        self.pack()

        self.window.config(menu=self.menubar)
        self.pack()

    def on_open(self):  # открытие файла
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename) as file:
                for i in range(len(filename)):
                    if filename[len(filename) - i - 1] == '/':
                        # print(filename[len(filename)-i:])
                        self.filename = filename[len(filename) - i:]
                        break
                print(self.filename)
                self.text = file.read()
                self.path_file_change.configure(state='normal')
                self.path_file_change.insert(END, file.name)
                self.path_file_change.configure(state='disabled')
                self.manager.view_file.configure(state='normal')
                self.manager.view_file.delete(1.0, END)  # не работает
                self.manager.view_file.update()
                self.manager.view_file.insert(1.0, self.text)
                self.manager.view_file.configure(state='disabled')
                self.manager.is_file_opened = True
                print(self.manager.is_file_opened,self.manager.is_connected)
        if self.manager.is_file_opened and self.manager.is_connected:
            self.manager.params_button['state']='normal'

    def save_file(self):
        filename = filedialog.asksaveasfilename(initialfile=self.manager.headername)
        letter = self.manager.view_file.get(1.0, END)
        file = open(filename, 'w')  # посмотреть какой режим записи файла выбрать
        file.write(letter)
        file.close()

    def send_file(self):

        self.manager.making_list(self.filename,self.text)

        self.manager.is_file_opened = False
        self.manager.params_button['state'] = 'disabled'
        self.manager.sending()

    def show_menu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def on_exit(self):

        if self.are_threads_going:
            self.manager.exit()
        self.quit()

    def center_window(self, w, h, par):  # центрирование окна

        sw = par.winfo_screenwidth()  # ширина экрана
        sh = par.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        par.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # class Settings(Frame):
    def show_info(self):
        self.top = Toplevel(master=self.window, background=DOP_COLOR)
        self.top.title('О программе')
        self.top.resizable(False, False)
        self.top.geometry('600x300')
        self.center_window(600, 300, self.top)
        self.kurs_label = Label(self.top, text="Курсовая работа", background=DOP_COLOR, font=FONT_BIG)
        self.kurs_label.place(x=200, y=10)
        self.predmet_label = Label(self.top, text="По курсу: Сетевые технологии в АСОИУ", background=DOP_COLOR, font=FONT_DOP)
        self.predmet_label.place(x=120, y=50)
        self.galkin_label = Label(self.top, text="Преподаватель: Галкин В.А.", background=DOP_COLOR, font=FONT_DOP)
        self.galkin_label.place(x=170, y=80)
        self.about_us_label = Label(self.top, text="Выполнили:", background=DOP_COLOR, font=FONT_DOP)
        self.about_us_label.place(x=230, y=120)
        self.lina_label = Label(self.top, text="Костян Алина, ИУ5-63", background=DOP_COLOR, font=FONT)
        self.lina_label.place(x=210, y=150)
        self.andrew_label = Label(self.top, text="Болотин Андрей, ИУ5-62", background=DOP_COLOR, font=FONT)
        self.andrew_label.place(x=210, y=180)
        self.nata_label = Label(self.top, text="Брысина Наталия, ИУ5-64", background=DOP_COLOR, font=FONT)
        self.nata_label.place(x=210, y=210)
        self.kafedra_label = Label(self.top, text="Кафедра ИУ5 2019г.", background=DOP_COLOR, font=FONT)
        self.kafedra_label.place(x=210, y=260)

    def callback(self, event_object):  # обработка события выпадающего списка
        var = event_object.widget.get()
        # print(var)
        return var

    def pace_callback(self, event_object):  # обработка события выпадающего списка
        var = event_object.widget.get()
        if var == 'Быстро':
            self.manager.SendingThread.sleep_time=0
            self.manager.SendingThread.is_paused = False
        elif var == 'Средне':
            self.manager.SendingThread.sleep_time=5
            self.manager.SendingThread.is_paused = False
        elif var == 'Медленно':
            self.manager.SendingThread.sleep_time=10
            self.manager.SendingThread.is_paused = False
        else:
            self.manager.SendingThread.sleep_time=0
            self.manager.SendingThread.is_paused = True
        # print(var)
        return var

    def conn(self):

        self.set_button.configure(text='Разорвать соединение')
        self.manager.change_status_label['text'] = 'установлено'
        self.manager.change_status_label['fg'] = 'green'
        # self.manager.test()


        if not self.is_port_opened:
            dport = self.sender_port.get()
            speed = int(self.speed.get())
            if self.timeout.get() != 'None':
                timeout = int(self.timeout.get())
            else:
                timeout=0
            stopbits = self.stop_bits.get()


            self.manager.connect(dev_port=dport,
                                    speed=speed,
                                    timeout = timeout,
                                    stopbits=stopbits)
            if self.manager.COMport.status():
                messagebox.showinfo("Порт",'Порт работает')
                self.sender_port['state']='disabled'
                self.speed['state']='disabled'
                self.timeout['state']='disabled'
                self.stop_bits['state']='disabled'
                self.is_port_opened = True
                self.set_button.configure(text='Разорвать соединение')
                time.sleep(5)
                self.manager.framelist.append('L')
                self.manager.sending()
            else:
                messagebox.showinfo("Порт",'Порт не работает')

        else:
            if self.manager.is_connected:
                self.manager.framelist.append('U')
                self.manager.sending()
            self.manager.change_port()
            if not self.manager.COMport.status():
                messagebox.showinfo("Порт",'Порт отключен')
                self.sender_port['state']='normal'
                self.speed['state']='normal'
                self.timeout['state']='normal'
                self.stop_bits['state']='normal'
                self.is_port_opened = False
                self.set_button.configure(text='Установить соединение')
                self.manager.is_connected=False
            else:
                messagebox.showinfo("Порт",'Не удалось разорвать соединение')
        self.are_threads_going=True


# if __name__ == '__main__':
#     main()

# app = MainWindow()
