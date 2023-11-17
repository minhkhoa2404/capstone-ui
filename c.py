import streamlit as st
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

return_value = st_javascript(
    """
    return body.css("background-color")
    """
)

print(return_value)
