from fastapi import FastAPI , File , Request
from fastapi.responses import HTMLResponse
# from typing import List
from fastapi.templating import Jinja2Templates
import uvicorn
import yaml

templates = Jinja2Templates(directory="api/templates")

app = FastAPI()


@app.post("/files")
async def create_files(
    # file: bytes = File(...)
    request:Request
    ):


    form = await request.form()
    file = form['file']
    A_NAME = form['a_name']
    C_NAME = form['c_name']
    E_MAIL = form['email']
    content = await file.read()
    print(file.filename.split('.')[::-1])


    with open("api/temp.yaml","w") as y:
        d = {"A_NAME" : A_NAME,"C_NAME":C_NAME,"E_MAIL":E_MAIL,"CHANGE":True,"C":True}
        yaml.dump(d,y)

    with open("Class/{}.csv".format(C_NAME),"wb+") as f:
        f.write(content)

    return {"Please Close your browser "}


def get_class_list():
    import os
    files = os.listdir('Class')
    temp = []
    for i in files:
        if i.endswith(".yaml"):
            temp.append(i.split(".yaml")[0])
    return temp


@app.get("/" ,response_class=HTMLResponse)
def main(request : Request,):
    return templates.TemplateResponse("home.html",{"request":request,})


@app.get("/course")
def course(request: Request):

    class_list = get_class_list()
    return templates.TemplateResponse("create_course.html",{"request":request,"class":class_list})


@app.post("/course")
async def course(request: Request):
    l = await request.form()
    print(l)
    code = l['c_code']
    course = l['c_name']
    incharge = l['a_name']
    email = l['email']
    c_name = l["c_name"]
    change = True
    with open("api/temp.yaml","w") as y:
        d = {"CODE":code,"C_NAME":c_name,"CC_NAME":course,"A_NAME":incharge,"EMAIL":email,"CHANGE":change,"C":False}
        yaml.dump(d,y)



    return {"Please Close your browser "}

def run():
    uvicorn.run(app,host="0.0.0.0")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0")