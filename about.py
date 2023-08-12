import streamlit as st
from streamlit.components.v1 import html

def render_html_file():
    with open('about.html', 'r') as file:
        html_content = file.read()

    # Render the HTML content
    html(html_content, height=500)
