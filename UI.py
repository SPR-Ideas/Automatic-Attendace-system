import os
import threading
import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
from api import main as m
import yaml
import pandas as pd
from blue import start , attendance

SERVER_PID = 0
customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# app = customtkinter.CTk()
# app.geometry("400x580")



class App(customtkinter.CTk):
    # name ,email ,c_name= tk.StringVar(),tk.StringVar(),tk.StringVar()

    def __init__(self):
        super().__init__()
        self.title("CustomTkinter complex_example.py")
        self.geometry("480x320")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(0,minsize=int(0.2*480),weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = Options()
        self.frame_right = QRcode()

        self.frame_left.grid(row=0, column=0, sticky="nswe")
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
        self.frame_right=Start()
        self.frame_right.update_course()
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)


    def on_closing(self, event=0):
        kill_server()
        self.destroy()


class Report(customtkinter.CTkFrame):
    def __init__(self):
        super().__init__()

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.frame = customtkinter.CTkFrame(master=self)

        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=1)
        self.frame.rowconfigure(0,weight=1)

        self.listbox = customtkinter.CTkOptionMenu(
            master= self.frame,values=['--select--',]
        )
        self.label = customtkinter.CTkLabel(master=self.frame,text="Course Code",fg_color="#2A2D2E")
        self.label.grid(row=0,column=0,)
        self.listbox.grid(row=0,column=1)

        self.frame.place(rely=0.1)

        self.button1 = customtkinter.CTkButton(master = self,
                                            #   width = 120,
                                                height = 32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Send Report",
                                                command = self.send_report
                                                )

        self.button1.grid(row=0,column=0,padx=10,pady=5)
        self.update_course()


    def make_csv_report(self,course):
        df = pd.read_csv("Records/{}.csv".format(course))
        l = df.mean()*100
        l.to_csv("Records/{}-.csv".format(course))


    def send_report(self):
        import GoogleApi.gmail_api as GP
        course = self.listbox.get()
        if course !="--select--":

            with open("Records/{}.yaml".format(course)) as l:
                data = yaml.safe_load(l)

            self.make_csv_report(course)
            content = "Hi {} hear I have attached the Attendance Report for {} ".format(
                data["A_NAME"],
                data["CODE"]
            )

            GP.send_mail(data["EMAIL"], "ATTENDACE SYSTEM",
                content, "Records/{}-.csv".format(course)
            )
            os.remove("Records/{}-.csv".format(course))


    def update_course(self):
        import os
        l = os.listdir("Records/")
        values = []
        for i in l :
            if i.endswith(".yaml"):
                values.append(i.split(".yaml")[0])
        values.insert(0,"ALL")
        self.listbox.configure(values=values)



class CreateClass2(customtkinter.CTkFrame):


    def __init__(self):
        super().__init__()
        self.CONFIG_YAML = {}
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3,weight=1)

        Label1 = customtkinter.CTkLabel(master = self, text = "Name")
        Label2 = customtkinter.CTkLabel(master = self, text = "Mac_address")
        Label3 = customtkinter.CTkLabel(master = self, text = "Register No")

        Label1.grid(row = 0, column = 0, padx = 5, pady = 5)
        Label2.grid(row = 1, column = 0, padx = 5, pady = 5)
        Label3.grid(row = 2, column = 0, padx = 5, pady = 5)


        # option1==============================

        self.combobox1 = customtkinter.CTkComboBox(master = self,
                                            values=["--Select--"],)
        self.combobox1.grid(row = 0, column = 1, padx=5,pady=5)

        # option2==============================

        self.combobox2 = customtkinter.CTkComboBox(master = self,
                                            values=["--Select--"],)
        self.combobox2.grid(row = 1, column = 1, padx=5,pady=5)

        # option3==============================

        self.combobox3 = customtkinter.CTkComboBox(master = self,
                                            values=["--Select--"],)
        self.combobox3.grid(row = 2, column = 1, padx=5,pady=5)

    #   Submit Button
        self.button = customtkinter.CTkButton(master = self,
                                            #   width = 120,
                                                height = 32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Submit",
                                                command=self.write_configure
                                                )

        self.button.grid(row=3,column=1,padx=5,pady=5,)


    def write_configure(self):
        print("pressed")
        self.CONFIG_YAML['mapped_values'] = [self.combobox1.get(),self.combobox2.get(),self.combobox3.get()]


        with open("Class/{}.yaml".format(self.CONFIG_YAML['C_NAME']),"w") as c:
            yaml.dump(self.CONFIG_YAML,c)

        home_cb()



    def set_value_for_combo_box(self,data):

        self.CONFIG_YAML = data

        try :
            df  = pd.read_csv("Class/{}.csv".format(data["C_NAME"]))
        except:
            df  = pd.read_excel("Class/{}.csv".format(data["C_NAME"]))

        values = list(df.columns)
        print(values)

        self.combobox1.configure(values=values)
        self.combobox2.configure(values=values)
        self.combobox3.configure(values = values)



class Options(customtkinter.CTkFrame):
    # # ============ frame_left ============
    def __init__(self):
        super().__init__()
        # top bar ==============================
        self.Label = customtkinter.CTkLabel(self,
                                        text= "Menus",
                                        # width=int(480*0.2)
                                    )
        self.Label.grid(padx=10,pady=10)

        # Options ===============================
        # 1

        self.home = customtkinter.CTkButton(self,
                                            text = "Home",
                                            fg_color="#2A2D2E",
                                            command=home_cb
            )
        self.home.grid(padx=5,pady=5)

        # 2

        self.create_class = customtkinter.CTkButton(self,
                                            text = "Create Class",
                                            fg_color="#2A2D2E",
                                            command=cc1_cb
            )
        self.create_class.grid(padx=5,pady=5)

        # 3

        self.create_course = customtkinter.CTkButton(self,
                                            text = "Create Course",
                                            fg_color="#2A2D2E",
                                            command=cc4_cb
            )
        self.create_course.grid(padx=5,pady=5)

        self.create_course = customtkinter.CTkButton(self,
                                            text = "Report",
                                            fg_color="#2A2D2E",
                                            command= report_cb
            )
        self.create_course.grid(padx=5,pady=5)


# QR code frame
class QRcode(customtkinter.CTkFrame):
    def __init__(self):
        super().__init__()
        # my_image = customtkinter.CTkImage(dark_image=Image.open("C:/Users/shivs/OneDrive/Desktop/tkinter/Screenshot (4).png"),
        #                                   size=(30, 30))

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        image1 = Image.open("api/qrcode.png")
        test = ImageTk.PhotoImage(image1)

        label = customtkinter.CTkLabel(master=self,text="Scan the QR Code")
        label.grid(row=0,column=0,padx=5,pady=5)

        label1 = customtkinter.CTkLabel(master=self,image=test, anchor= tk.CENTER)
        # label1 = tkinter.Label(image=test)
        label1.image = test
        label1.grid(row=1,column =0 ,padx=10,pady=5)

# to scane and test

class Progression(customtkinter.CTkFrame):
    def __init__(self,):
        super().__init__()
        global app
        self.val = tk.IntVar()
        self.progressbar = customtkinter.CTkProgressBar(master=self)
        self.progressbar.place(rely=0.5,relx=0.1)
        self.label = customtkinter.CTkLabel(master=self,text="Scanning for Devices")
        self.label.place(rely=0.4 , relx=0.25)
        self.progressbar.set(0)
        self.update()

        # self.progressbar.configure()

    def start_(self,course):
        th = threading.Thread(target=start,args=(course,self))
        th.start()



    def progression(self,val):
        global app
        self.progressbar.set(val)
        self.update()
        app.update()


    def move(self,en_data):
        global app
        app.frame_right = list_ab(en_data)
        app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
        app.update()
        # self.course = course
        # attendance(course)



class Start(customtkinter.CTkFrame):
    def __init__(self):
        super().__init__(width=int(480*1))

        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.frame = customtkinter.CTkFrame(master=self)

        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=1)
        self.frame.rowconfigure(0,weight=1)

        self.listbox = customtkinter.CTkOptionMenu(
            master= self.frame,values=['--select--',]
        )
        self.label = customtkinter.CTkLabel(master=self.frame,text="Course Code",fg_color="#2A2D2E")
        self.label.grid(row=0,column=0,)
        self.listbox.grid(row=0,column=1)

        self.frame.place(rely=0.1)

        self.button1 = customtkinter.CTkButton(master = self,
                                            #   width = 120,
                                                height = 32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Start Scanning",
                                                command=self.start_cb
                                                )

        self.button1.grid(row=0,column=0,padx=10,pady=5)



    def start_cb(self):
        global app
        course = self.listbox.get()
        app.frame_right = Progression()
        app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
        app.update()
        app.frame_right.start_(course)

    def update_course(self):
        import os
        l = os.listdir("Records/")
        values = []
        for i in l :
            if i.endswith(".yaml"):
                values.append(i.split(".yaml")[0])

        self.listbox.configure(values=values)


class Details(customtkinter.CTkFrame):
    def __init__(self):
        global name , c_name , email
        super().__init__()
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3,weight=1)

        Label1 = customtkinter.CTkLabel(master = self, text = "Class Advisor")
        Label2 = customtkinter.CTkLabel(master = self, text = "Class With Section")
        Label3 = customtkinter.CTkLabel(master = self, text = "Advisor Mail-id")

        Label1.grid(row = 0, column = 0, padx = 5, pady = 5)
        Label2.grid(row = 1, column = 0, padx = 5, pady = 5)
        Label3.grid(row = 2, column = 0, padx = 5, pady = 5)

        name ,email ,c_name= tk.StringVar(),tk.StringVar(),tk.StringVar()


        self.entry1 = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry1",textvariable=name)
        self.entry1.grid(row = 0, column = 1, padx=5,pady=5)

        self.entry2 = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry2",textvariable=c_name)
        self.entry2.grid(row = 1, column = 1, padx=5,pady=5)

        self.entry3 = customtkinter.CTkEntry(master=self, placeholder_text="CTkEntry3",textvariable=email)
        self.entry3.grid(row = 2, column = 1, padx=5,pady=5)



        self.button2 = customtkinter.CTkButton(master = self,
                                            #   width = 120,
                                                height = 32,
                                                border_width=0,
                                                corner_radius=8,
                                                text="Next",
                                                command=cc1_cb)

        self.button2.grid(row=3,column=1,padx=10,pady=5)


class Sub(customtkinter.CTkFrame):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        r,c = 0,0
        for i in get_availabel_class():

            self.entry = customtkinter.CTkFrame(master=self,border_width=2,

        )
            label = customtkinter.CTkLabel(master = self.entry,text = i,height=80,width=80)
            label.grid()
            self.entry.grid(row = r, column = c,pady=10,padx=5)
            c+=1
            if c>2:
                c =0
                r+=1

        self.button2 = customtkinter.CTkButton(master = self,
                                              width = 80,
                                                height = 80,
                                                border_width=0,
                                                corner_radius=8,
                                                text="+",
                                                command=cc2_cb
                                                )

        self.button2.grid(row= r, column=c,pady=10,padx=5)



class list_ab(customtkinter.CTkFrame):
    def __init__(self,en_data):
        super().__init__()

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=9)
        self.columnconfigure(0,weight=1)
        # self.course = en_data.course
        self.en_data = en_data

        label = customtkinter.CTkLabel(self,text="ABSENT",height=20)
        label.grid(row=0,column=0,padx=10,pady=10,)

        canvas = customtkinter.CTkCanvas(self,bg="#2A2D2E",)
        canvas.grid(row=1, column=0,sticky="nsew",padx=10,pady=10)
        canvasFrame = customtkinter.CTkFrame(canvas,border_color="#000000")

        canvas.create_window(0, 0, window=canvasFrame, anchor='nw')
        count = 0
        self.instance = {}
        for i in en_data.absent:
            element = customtkinter.CTkCheckBox(canvasFrame, text=i,)
            element.grid(row=count, column=0,padx=10,pady=10)
            self.instance[i] = element
            count+=1

        button = customtkinter.CTkButton(self,text="Mark",command=self.mark_attendance)
        button.grid(row=2,column=0,padx=5,pady=5)
        yscrollbar = customtkinter.CTkScrollbar(self, orientation="vertical",command=canvas.yview)
        # yscrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=yscrollbar.set)
        yscrollbar.grid(row=1, column=1, sticky="ns")

        canvasFrame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    def mark_attendance(self):
        global app
        temp=[]
        for reg, inst, in self.instance.items():
            if inst.get():
                temp.append(reg)
        for i in temp:
            self.en_data.present.append(i)
            self.en_data.absent.remove(i)
            self.en_data.present.sort()
            self.en_data.absent.sort()
        # print(self.en_data.present)
        attendance(self.en_data)
        app.frame_right = Start()
        app.frame_right.update_course()
        app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)


# server Manitanance
def kill_server():
    global SERVER_PID
    if SERVER_PID:
        import os , signal
        os.kill(SERVER_PID,signal.SIGTERM)
        SERVER_PID = 0

def start_server():
    global SERVER_PID
    import multiprocessing
    th = multiprocessing.Process(target=m.run)
    th.start()

    SERVER_PID = th.pid


def get_availabel_class():
    li = []
    for i in os.listdir("Class"):
        if i.endswith(".yaml"):
            li.append(i.split(".yaml")[0])
    return li


def scan_for_change():
    flag= False
    data = {}
    while not flag:
        try:
            with open("api/temp.yaml",'r') as f:
                data =yaml.load(f)
                flag = data["CHANGE"]
            # print(flag)
        except TypeError:
            pass

    with open("api/temp.yaml",'w+') as f:
        d = {"A_NAME" : "","C_NAME":"","E_MAIL":"","CHANGE":False}
        yaml.dump(d,f)

    print("change updated")
    if data["C"]:
        cc3_cb(data)
    else:
        course_code = data['CODE']
        with open("Records/{}.yaml".format(data['CODE']),'w') as f:
            yaml.dump(data,f)

        with open("Class/{}.yaml".format(data['C_NAME']),'r') as f:
            data = yaml.load(f)

        try:
            df = pd.read_csv("Class/{}.csv".format(data['C_NAME']))
        except:
            df = pd.read_excel("Class/{}.csv".format(data['C_NAME']))

        col = list(df[data['mapped_values'][2]])
        col.sort()
        col.insert(0,"Time")
        col.insert(0,"Date")

        d = {i:[] for i in col}
        df2 = pd.DataFrame(columns=d)
        df2.to_csv("Records/{}.csv".format(course_code),index=False)

        home_cb()


def make_qr(route=""):
    import netifaces ,pyqrcode
    ip = netifaces.ifaddresses('wlo1')[netifaces.AF_INET][0]['addr']
    url = pyqrcode.create(ip+":8000"+"/{}".format(route))
    url.png("api/qrcode.png",scale=5)


# Call Back Functions

def report_cb():
    global app
    kill_server()

    app.frame_right = Report()
    app.frame_right.grid(row=0,column=1,sticky="nswe",padx=10,pady=10)
    app.update()

def home_cb():
    global app
    kill_server()

    app.frame_right = Start()
    app.frame_right.update_course()
    app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
    app.update()



# def cc1_cb():
#     global app , SERVER_PID

#     kill_server()

#     app.frame_right = Details()
#     start_server()

#     app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
#     app.update()

def cc4_cb():
    global app
    import threading

    kill_server()
    make_qr("course")

    start_server()

    app.frame_right = QRcode()
    app.frame_right.grid(row=0,column=1, sticky="nswe", padx=10,pady=10)
    app.update()

    th = threading.Thread(target=scan_for_change)
    th.start()

def cc3_cb(data):
    global app
    kill_server()

    frame_instance = CreateClass2()
    frame_instance.set_value_for_combo_box(data)

    app.frame_right = frame_instance
    app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
    app.update()


def cc1_cb():
    global app

    kill_server()
    app.frame_right = Sub()
    app.frame_right.grid(row=0,column =1,sticky = "nswe",padx=10,pady=10)


def cc2_cb():
    global app
    import threading

    # if name.get() and c_name.get() and email.get():
    kill_server()
    start_server()
    make_qr()
    app.frame_right = QRcode()
    app.frame_right.grid(row=0, column=1, sticky="nswe", padx=10,pady=10)
    app.update()

    th = threading.Thread(target=scan_for_change)
    th.start()

if __name__ =="__main__":
    app = App()
    app.mainloop()