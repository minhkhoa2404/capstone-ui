# import os
# import torch
# from tqdm import tqdm
import cv2
import numpy as np
import time
import torch
import io
import base64
from PIL import Image
import json


t1 = time.time()
model = torch.hub.load("yolov5", "custom", path="best.pt", source="local")
model.hide_conf = True
# model.half = True
t2 = time.time()

print(t2 - t1)

img = r"test.jpg"

t3 = time.time()
results = model(img)  # inference
t4 = time.time()

# results.show()
print(t4 - t3)

a = results.pandas().xyxy[0].to_json(orient="records")
ys = json.loads(a)

for y in ys:
    print(y["name"])

counts = dict()
for y in ys:
    counts[y["name"]] = counts.get(y["name"], 0) + 1

print(counts)
# results.ims
# results.render()  # updates results.ims with boxes and labels
# buffered = io.BytesIO()
# im_base64 = Image.fromarray(results.ims[0])
# im_base64.save(buffered, format="JPEG")
# print(base64.b64encode(buffered.getvalue()))
# t3 = time.time()
# with torch.no_grad():
#     results1 = model(img)
# t4 = time.time()

# results = model(img)
# t5 = time.time()

# print(f"{t4 - t3} - {t5 - t3}")
# # Results
# cv2.imshow("Test", np.array(results.render()[0]))

# cv2.waitKey(0)
# cv2.destroyAllWindows()
