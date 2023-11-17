"""
                       _oo0oo_
                      o8888888o
                      88" . "88
                      (| -_- |)
                      0\  =  /0
                    ___/`---'\___
                  .' \\|     |// '.
                 / \\|||  :  |||// \
                / _||||| -:- |||||- \
               |   | \\\  -  /// |   |
               | \_|  ''\---/''  |_/ |
               \  .-\__  '-'  ___/-. /
             ___'. .'  /--.--\  `. .'___
          ."" '<  `.___\_<|>_/___.' >' "".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `_.   \_ __\ /__ _/   .-` /  /
     =====`-.____`.___ \_____/___.-`___.-'=====
                       `=---=' 
"""


from fastapi import FastAPI, Path, UploadFile
import uvicorn
from PIL import Image, ImageOps
import io
import torch
import base64
import json

app = FastAPI()

img_list = {}

model = torch.hub.load(
    "yolov5", "custom", path="best.pt", source="local", verbose=False
)
model.hide_conf = True


def result_to_json(res: str):
    counts = dict()
    items = json.loads(res)
    for item in items:
        counts[item["name"]] = counts.get(item["name"], 0) + 1
    return counts


@app.get("/")
async def root():
    return {"message": (1, 2)}


@app.post("/upload/{file_name}")
async def upload_file(file_name: str, file: UploadFile):
    content = await file.read()
    img = io.BytesIO()
    img_arr = Image.open(io.BytesIO(content))
    img_arr = ImageOps.exif_transpose(img_arr)
    img_arr.save(img, "JPEG")

    with torch.no_grad():
        results = model(img_arr, size=640)  # inference
    results.ims
    results.render()
    buffered = io.BytesIO()
    im_base64 = Image.fromarray(results.ims[0])
    im_base64.save(buffered, format="JPEG")

    result_str = results.pandas().xyxy[0].to_json(orient="records")

    img_list[file_name] = {
        "img": base64.b64encode(img.getvalue()),
        "result": base64.b64encode(buffered.getvalue()),
        "json_result": result_to_json(result_str),
    }
    return img_list[file_name]


@app.get("/get_img/{file_name}")
async def get_img(file_name: str):
    return img_list[file_name]["img"]


@app.get("/get_result/{file_name}")
async def get_img(file_name: str):
    return img_list[file_name]["result"]


@app.get("/get_json/{file_name}")
async def get_img(file_name: str):
    return img_list[file_name]["json_result"]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
