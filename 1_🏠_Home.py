import streamlit as st ###### Import Streamlit library
from configparser import ConfigParser ###### Import ConfigParser library for reading config file to get model, greeting message, etc.
from PIL import Image ###### Import Image library for loading images
import os ###### Import os library for environment variables
from src.utils.ui_helpers import * ###### Import custom utility functions

# Authentication check - reset on refresh
def check_auth():
    # Clear authentication on page refresh/reload
    if "page_loaded" not in st.session_state:
        st.session_state.clear()
        st.session_state.page_loaded = True
        st.session_state.authenticated = False
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Elegant login container with glassmorphism effect
        st.markdown("""
        <div style="
            max-width: 400px;
            margin: 5rem auto;
            padding: 3rem 2rem;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(160, 32, 240, 0.1);
            border: 1px solid rgba(160, 32, 240, 0.1);
        ">
            <div style="text-align: center; margin-bottom: 2.5rem;">
                <div style="
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(135deg, #A020F0, #8B1A9B);
                    border-radius: 50%;
                    margin: 0 auto 1rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2rem;
                ">
                    🏦
                </div>
                <h1 style="
                    color: #A020F0;
                    font-size: 2rem;
                    margin: 0 0 0.5rem 0;
                    font-weight: 600;
                    font-family: 'Inter', sans-serif;
                ">
                    BankIQ+
                </h1>
                <p style="
                    color: #666;
                    font-size: 1rem;
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                ">
                    Advanced Banking Analytics
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create centered columns for form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div style="margin-top: -2rem;">', unsafe_allow_html=True)
            
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                label_visibility="collapsed"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                label_visibility="collapsed"
            )
            
            st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)
            
            if st.button("Sign In", use_container_width=True):
                if username == "awsuser" and password == "Password123$":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        

        return False
    return True

# Check authentication before showing main app
if not check_auth():
    st.stop()

    # Custom column layout with increased width for col1 and col3, and moving them down by 20pt
config_object = ConfigParser()
config_object.read("src/utils/bank_config.ini")
hline=Image.open(config_object["IMAGES"]["hline"]) ###### image for formatting landing screen

#st.set_page_config(page_title="My App", layout="wide")
st.set_page_config(
    layout="wide", 
    page_title="BankIQ",
    menu_items=None,
    initial_sidebar_state="expanded"
)

#### Set Logo on top sidebar ####
c1,c2,c3=st.sidebar.columns([1,3,1]) ###### Create columns
##
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }
        
        .main * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
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
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }
        
        p, span, div {
            font-family: 'Inter', sans-serif !important;
            font-weight: 400 !important;
        }
        
        /* Style login input boxes */
        .stTextInput > div > div > input {
            border: 2px solid #E5E7EB !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            font-family: 'Inter', sans-serif !important;
            background-color: #ffffff !important;
            outline: none !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #A020F0 !important;
            box-shadow: 0 0 0 3px rgba(160, 32, 240, 0.1) !important;
            transform: translateY(-1px) !important;
        }
        
        .stDeployButton {
            display: none !important;
        }
        
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        .stActionButton {
            display: none !important;
        }
        
        /* Hide all tooltips and hover elements */
        [role="tooltip"],
        .stTooltipHoverTarget,
        [data-testid="stTooltipHoverTarget"],
        [data-baseweb="tooltip"],
        .st-emotion-cache-tooltip,
        [class*="tooltip"],
        [id*="tooltip"],
        [title*="keyword"],
        [title*="double_arrow"],
        [aria-label*="keyword"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Hide sidebar resizer handle */
        .css-1d391kg,
        .css-1lcbmhc,
        .css-1y4p8pa,
        [data-testid="stSidebarNav"] + div,
        .stApp > div > div > div > div:first-child::after,
        .sidebar .element-container::after,
        .css-1lcbmhc .css-1d391kg,
        [class*="css-"][class*="sidebar"]::after,
        [class*="css-"][class*="resize"],
        .stSidebar::after,
        .stSidebar + div::before {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        
        /* Hide any resizer or splitter */
        [role="separator"],
        [class*="resizer"],
        [class*="splitter"],
        [style*="cursor: col-resize"],
        [style*="cursor: ew-resize"],
        .stApp [data-testid="stSidebar"] + div::before,
        .stApp [data-testid="stSidebar"] + div::after,
        .stApp > div:first-child > div:first-child::after {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Make sidebar static size - no resizing */
        [data-testid="stSidebar"] {
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            resize: none !important;
        }
        
        /* Disable all resize handles and cursors */
        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"]::before,
        [data-testid="stSidebar"]::after,
        [data-testid="stSidebar"] + *::before,
        [data-testid="stSidebar"] + *::after {
            cursor: default !important;
            resize: none !important;
            pointer-events: none !important;
        }
        
        /* Hide any tooltip elements */
        [data-baseweb="tooltip"],
        [role="tooltip"],
        .stTooltipHoverTarget,
        [data-testid="stTooltipHoverTarget"],
        [class*="css-tooltip"],
        [title*="keyword"],
        [aria-label*="keyword"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Disable pointer events for tooltip triggers */
        *[title] {
            pointer-events: none !important;
        }
        
        /* Show sidebar normally */
        [data-testid="stSidebar"] {
            display: block !important;
        }
        
        /* Enhanced button styling */
        .stButton > button {
            background: linear-gradient(135deg, #A020F0 0%, #8B1A9B 100%) !important;
            color: white !important;
            border: none !important;
            padding: 16px 32px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 30px rgba(160, 32, 240, 0.4) !important;
            background: linear-gradient(135deg, #8B1A9B 0%, #6A1B9A 100%) !important;
        }
        
        /* Re-enable pointer events for sidebar content */
        [data-testid="stSidebar"] .element-container,
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] [data-testid="stSidebarNav"],
        [data-testid="stSidebar"] [data-testid="stSidebarNavItems"],
        [data-testid="stSidebar"] [role="button"],
        [data-testid="stSidebar"] .css-1544g2n {
            pointer-events: auto !important;
        }
    </style>

    <style>
        /* Global rule to hide any text containing keyword */
        * {
            font-size: 0 !important;
        }
        
        * {
            font-size: initial !important;
        }
        
        *:contains("keyword") {
            display: none !important;
        }
        
        /* Hide the specific keyword text */
        .stApp *::before,
        .stApp *::after {
            content: "" !important;
        }
        
        .stApp * {
            text-indent: -9999px !important;
        }
        
        .stApp * {
            text-indent: 0 !important;
        }
        
        /* Target the specific problematic element */
        [class*="css"] *:not(h1):not(h2):not(h3):not(p):not(span):not(div):not(button):not(input) {
            font-size: 0 !important;
            line-height: 0 !important;
            color: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True
)
# Removed sidebar title

##





st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #2C5F41 0%, #1B4332 100%); margin-left: calc(-50vw + 50%); margin-bottom: 20px;"></div>', unsafe_allow_html=True)
heads()
st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #2C5F41 0%, #1B4332 100%); margin-left: calc(-50vw + 50%); margin-top: 20px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
col1, col2, col3=st.columns([10,1,10])
with col1:
    first_column()
with col2:
    st.write("")
with col3:
    third_column()
st.markdown('<div style="width: 100vw; height: 4px; background: linear-gradient(90deg, #2C5F41 0%, #1B4332 100%); margin-left: calc(-50vw + 50%); margin-top: 20px; margin-bottom: 20px;"></div>', unsafe_allow_html=True)

# Logout button in sidebar
with st.sidebar:
    if st.button("🚪 Logout", key="logout_button_unique"):
        st.session_state.authenticated = False
        st.rerun()

# Footer note
        st.markdown('</div>', unsafe_allow_html=True)  # Close login container
        
        # Modern footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; color: rgba(255, 255, 255, 0.8);">
            <p style="font-size: 0.9rem; margin: 0;">
                ✨ Powered by Amazon Bedrock & Claude AI ✨
            </p>
        </div>
        """, unsafe_allow_html=True)


