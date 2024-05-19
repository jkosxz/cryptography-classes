from blockchain import Blockchain, Block
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

blockchain = Blockchain()

class BlockData(BaseModel):
    data: str

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


@app.get('/chain')
def get_chain(request: Request):
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.post('/add_block')
def add_block(block_data: BlockData):
    if not block_data.data:
        raise HTTPException(status_code=400, detail="No data provided")
    new_block = Block(123, 123, 123, 123, 123)
    blockchain.add_block(block_data.data, new_block)
    return {"message": "Block added"}
