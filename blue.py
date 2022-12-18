from threading import Thread
from bluetooth import lookup_name
import pandas as pd
import yaml
import datetime as dt

DEVICES = []
REG = []

DIC = dict()
COUNT = 0

PRESENT = []
ABSENT = []
TOTAL = []
VAL = 0
FLAG = True

class EnData:
    def __init__(self,c,t,p,a) :
        self.course  =  c
        self.total   =  t
        self.present =  p
        self.absent  =  a


def scan_is_there(mac,reg):

    if lookup_name(mac):
        PRESENT.append(reg)
        print(reg)


def run(instance):
    global COUNT,VAL
    import time
    for key , value in DIC.items():
        VAL = COUNT /len(TOTAL)
        # time.sleep(0.2)
        # print(val)
        instance.progression(VAL)
        scan_is_there(key,value)
        COUNT+=1
    # instance.move()
    VAL = -1


def configure(course_code):
    """
        Input file = File location
        Mapped Values = Dictionary
            eg : {
                'name':"Student Name",
                'reg_no':"Reg No",
                'mac_address' : "Mac ID"
            }
    """
    global TOTAL ,DIC

    with open("Records/{}.yaml".format(course_code),"r") as f:
        rec_yaml = yaml.safe_load(f)

    with open("Class/{}.yaml".format(rec_yaml["C_NAME"]),"r") as f:
        mapped_values = yaml.safe_load(f)['mapped_values']

    df = pd.read_csv("Class/{}.csv".format(rec_yaml["C_NAME"]))

    TOTAL = list(df[mapped_values[2]].values)
    TOTAL.sort()

    for i in df.iloc:
        DIC[i[mapped_values[1]].upper()] = i[mapped_values[2]]
    DIC = dict(sorted(DIC.items(), key=lambda x:x[1]))


def attendance(en_data):
    """
        It gonna take append the result to the concernt db.
    """
    date  = dt.datetime.today()
    time = date.strftime("%H:%M:%S")
    date = date.strftime("%d.%m.%Y")
    tem ={"DATE":[date],"Time":[time] }
    for i in en_data.total:
        if i in en_data.present:
            tem[i] = 1
        else:
            tem[i] = 0

    # print(tem)
    df = pd.DataFrame(tem)
    df.to_csv("Records/{}.csv".format(en_data.course),header=False,index=False,mode='a')


# def progression_count(v):
#     global COUNT, VAL
#     while(COUNT!=-1):
#         # VAL = COUNT /len(TOTAL)
#         # v.set(val)
#         # print(val)
#     print("escaped")

def start(course,instance):
    global ABSENT
    configure(course)
    # th = Thread(target=progression_count,args=(val,))
    # th.start()
    run(instance)
    ABSENT =list( set(TOTAL).difference(PRESENT))
    ABSENT.sort()
    PRESENT.sort()
    en_data = EnData(course,TOTAL,PRESENT,ABSENT)
    # print(ABSENT)
    instance.move(en_data)
    # attendance(course)
