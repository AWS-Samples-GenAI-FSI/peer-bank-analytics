import streamlit as st ###### Import Streamlit library
from configparser import ConfigParser ###### Import ConfigParser library for reading config file to get model, greeting message, etc.
from PIL import Image ###### Import Image library for loading images
import os ###### Import os library for environment variables
from src.utils.ui_helpers import * ###### Import custom utility functions

    # Custom column layout with increased width for col1 and col3, and moving them down by 20pt
config_object = ConfigParser()
config_object.read("bank_config.ini")
hline=Image.open(config_object["IMAGES"]["hline"]) ###### image for formatting landing screen

#st.set_page_config(page_title="My App", layout="wide")
st.set_page_config(layout="wide", page_title="BankIQ") ###### Removed the Page icon

#### Set Logo on top sidebar ####
c1,c2,c3=st.sidebar.columns([1,3,1]) ###### Create columns
##
st.markdown(
    """
    <style>
        html, body, [class*="css"] {
            font-family: Arial, sans-serif !important;
        }
        
        .main * {
            font-family: Arial, sans-serif !important;
        }
        
        [data-testid=stSidebar]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
            font-family: Arial, sans-serif !important;
        }
        
        /* Make horizontal lines span full width */
        .stImage > img {
            width: 100vw !important;
            max-width: 100vw !important;
            margin-left: calc(-50vw + 50%) !important;
            margin-right: calc(-50vw + 50%) !important;
        }
        
        /* Ensure main container allows full width */
        .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
            max-width: 100% !important;
        }
        
        /* Modern typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: Arial, sans-serif !important;
            font-weight: 600 !important;
        }
        
        p, span, div {
            font-family: Arial, sans-serif !important;
            font-weight: 400 !important;
        }
    </style>
    """, unsafe_allow_html=True
)
# Removed sidebar title

##





st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #4B91F1 0%, #1E88E5 100%); margin-left: calc(-50vw + 50%); margin-bottom: 20px;"></div>', unsafe_allow_html=True)
heads()
st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #4B91F1 0%, #1E88E5 100%); margin-left: calc(-50vw + 50%); margin-top: 20px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
col1, col2, col3=st.columns([10,1,10])
with col1:
    first_column()
with col2:
    st.write("")
with col3:
    third_column()
st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #4B91F1 0%, #1E88E5 100%); margin-left: calc(-50vw + 50%); margin-top: 20px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

# Footer note
st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; font-family: Arial, sans-serif; margin-top: 40px;'>Powered by Amazon Bedrock - BankIQ+</p>", unsafe_allow_html=True)


