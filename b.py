import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
import requests
import json
import io
import base64
import time

st.set_page_config(page_title="Hello World", layout="wide")

img, img_res_PIL = Image.new("RGBA", (640, 640), (255, 255, 255, 0)), Image.new(
    "RGBA", (640, 640), (255, 255, 255, 0)
)

json_res = requests.Response()
json_res._content = ""

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

button_center = """
<style>
div[class="row-widget stButton"]{
    display: grid;}
div[class="row-widget stDownloadButton"]{
    display: grid;}
button{
    margin: 0 auto;
    display: block}
</style>
"""

st.markdown(button_center, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file", ["jpg", "png", "jpeg"])


_, button_col1, _, button_col2, _ = st.columns([1, 2, 1, 2, 1])


if button_col1.button("Get result"):
    post_url = f"http://127.0.0.1:8080/upload/{uploaded_file.name}"
    get_img = f"http://127.0.0.1:8080/get_img/{uploaded_file.name}"
    get_result = f"http://127.0.0.1:8080/get_result/{uploaded_file.name}"
    get_json = f"http://127.0.0.1:8080/get_json/{uploaded_file.name}"

    upload = requests.post(
        post_url,
        files={"file": uploaded_file.getvalue()},
    )
    img_str = requests.get(get_img)
    img_res = requests.get(get_result)
    json_res = requests.get(get_json)
    img = base64.b64decode(img_str.text)
    imgPIL = Image.open(io.BytesIO(img))
    img_res = base64.b64decode(img_res.text)
    img_res_PIL = Image.open(io.BytesIO(img_res))

try:
    df_temp = json.loads(json_res.text)
except:
    pass


button_col2.download_button(
    "Download csv",
    pd.DataFrame().to_csv(),
    "file.csv",
    "text/csv",
    key="download-csv",
)

col1, col2 = st.columns(2)

col1.image(img)
col2.image(img_res_PIL)


hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""

show_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: visible;}
</style>
"""

if json_res._content == "":
    st.markdown(hide_img_fs, unsafe_allow_html=True)
else:
    st.markdown(show_img_fs, unsafe_allow_html=True)
    st.dataframe(
        pd.DataFrame(
            {
                "Name": [name for name in df_temp.keys()],
                "Count": [count for count in df_temp.values()],
            }
        ),
        use_container_width=True,
        hide_index=True,
        height=455,
    )


# placeholder = st.empty()
