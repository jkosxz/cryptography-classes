from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import aiofiles
from stegano import lsb

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return RedirectResponse("/docs")


@app.post("/uploadimage")
async def upload(file: UploadFile = File()):
    async with aiofiles.open("./images/file.png", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    return {"Result": "OK"}


@app.get("/downloadcipheredimage")
async def download(text_to_hide: str):
    modified_image_path = "./images/modified_image.png"
    modified_image = lsb.hide("./images/file.png", text_to_hide)
    modified_image.save(modified_image_path)

    return FileResponse(path=modified_image_path, filename="image_with_hidden_text.png", media_type="image/png")


@app.post("/read_hidden_message")
async def read(image_to_read: UploadFile = File()):
    path = "./images/file_to_read.png"
    async with aiofiles.open(path, 'wb') as out_file:
        content = await image_to_read.read()  # async read
        await out_file.write(content)  # async write
        return {"hidden_message": lsb.reveal(path)}
