from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from multiprocessing import Queue
from WsClientDrone import WsClientDrone

q = Queue()
app = FastAPI()
ws_client = WsClientDrone(q)
ws_client.start()
origins = ['*']
templates = Jinja2Templates(directory="./")


@app.get("/")
def read_main(request: Request,response_class=HTMLResponse):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/set-current-direction")
async def set_current_direction(request: Request):
    data = await request.body()
    print(data)
    q.put(data)
    return {"msg": data}
