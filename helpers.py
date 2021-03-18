import streamlit as st
import os
import base64


# from https://discuss.streamlit.io/t/href-on-image/9693/3
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url, text=""):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        {text}
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" width=20/>
        </a>'''
    return html_code


def roll_page_layout():
    st.text("\n")
    st.text("\n")
    st.text("\n")
    st.sidebar.title("Settings")