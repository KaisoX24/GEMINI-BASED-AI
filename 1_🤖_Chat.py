import os
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import google.generativeai as genai
import google.ai.generativelanguage as glm 
import io
from PIL import Image
import requests
import time
import fitz  # PyMuPDF
import tempfile  # To handle temporary files

# Set page configuration
st.set_page_config(page_title='Ask Any Query', page_icon=':upside_down_face:', layout='wide')

# Configure Gemini API
load_dotenv()
safety_settings = [
    {"category": 'HARM_CATEGORY_SEXUALLY_EXPLICIT', "threshold": 'BLOCK_NONE'},
    {"category": 'HARM_CATEGORY_HATE_SPEECH', "threshold": 'BLOCK_NONE'},
    {"category": 'HARM_CATEGORY_HARASSMENT', "threshold": 'BLOCK_NONE'},
    {"category": 'HARM_CATEGORY_DANGEROUS_CONTENT', "threshold": 'BLOCK_NONE'}
]
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
chat = model.start_chat(history=[])

# Chat response function
def get_gemini_response(question):
    """Get a response from the Gemini AI model."""
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return None

# Gif Functions with Caching
@st.cache_data
def load_gif(url: str):
    """Load a GIF from a URL."""
    r = requests.get(url)
    if r.status_code != 200:
        st.error(f"Error loading GIF: {r.status_code}")
        return None
    return r.json()

# Image to byte array function
def image_to_byte_array(image: Image):
    """Convert an image to a byte array."""
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format=image.format)
    return img_byte_array.getvalue()

# Extract text from PDF function
def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Header Section of Webpage
gif_code = load_gif('https://lottie.host/7ee14ed1-6657-403e-9473-17740461cfbb/I1mf32pHPq.json')
gif_2 = load_gif('https://lottie.host/f6cff35b-d653-4c9d-b487-f5cadeb54e1e/z8UNfy8G61.json')

st.sidebar.success('Select a page above.')

# Center the image in the middle column
co1, co2, co3 = st.columns([0.2, 0.09, 0.2])

# Tabs
selected_page  = option_menu(
    menu_title='Main Menu',
    options=['Chat Bot', 'Chat Image Recognition', 'PDF Analysis'],  # Added PDF Analysis tab
    orientation='horizontal',
    icons=['cast', 'image', 'file-earmark-text'],  # Added icon for PDF Analysis
    styles={
        "container": {"padding": "0px", "font-size": "16px", "height": "50px"},
        "nav": {"flex-direction": "row"},
        "nav-link": {
            "padding": "0.5rem 1rem",
            "background-color": "#f0f2f5",
            "margin-right": "1rem",
            "color": "#343a40",
            "text-align": "center",
            "text-decoration": "none",
            "border": "0",
            "font-weight": "bold"
        },
        "nav-link[selected]": {"background-color": "#a8a9ab"},
    }
)
st.write('---')

# Function to display chat history
def display_chat_history():
    """Display the chat history."""
    st.write('---')
    st.subheader(":blue[Chat History]")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

if selected_page == "Chat Bot":
    col1, col2 = st.columns(2)
    with col1:
        st.title('Hello I\'m Carbon. A Chat Bot Application :sunglasses:')
        st.header('This is an Application of Artificial Intelligence based on Computer Language.')
        st.subheader('How can I help you?')
    with col2:
        st_lottie(gif_code, height=300, speed=1.2, key='AI')
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    input_text = st.text_input('**_Give Your Input:_**', key="input")
    submit_button = st.button(':orange[Ask Question]')
    st.write('---')

    if submit_button and input_text:
        with st.spinner('Fetching response...'):
            response = get_gemini_response(input_text)
            if response:
                st.session_state['chat_history'].append(('You', input_text))
                st.subheader('**:red[The Response is]** :nerd_face:')
                
                for chunk in response:
                    st.write(chunk.text)
                    st.session_state['chat_history'].append(('Carbon', chunk.text))

                display_chat_history()

elif selected_page == "Chat Image Recognition":
    c1, c2 = st.columns(2)
    with c2:
        st_lottie(gif_2, height=300, speed=1.2, key='cv')
    with c1:
        st.header("Interact with Computer Vision :grinning:")
        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)
            st.markdown("""<style>img {border-radius: 10px;}</style>""", unsafe_allow_html=True)
            
            if st.button(":orange[GET RESPONSE]", use_container_width=True):
                model = genai.GenerativeModel('gemini-1.5-flash')

                if image_prompt:
                    image = Image.open(uploaded_file)
                    progress_bar = st.progress(0)
                    st.markdown("""<style>.stProgress > div > div > div > div {background-color: #00FF00;}</style>""", unsafe_allow_html=True)

                    response = model.generate_content(
                        glm.Content(
                            parts=[
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )
                    
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.01)
                    
                    response.resolve()
                    st.write("")
                    st.subheader(":blue[_Response_]")
                    st.write("")
                    st.markdown(response.text)
                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")
        else:
            st.write("")
            st.header(":red[Please Provide an image]")

elif selected_page == "PDF Analysis":  # New tab for PDF Analysis
    st.header("Upload a PDF and Get Insights :page_facing_up:")
    uploaded_pdf = st.file_uploader("Choose a PDF file", accept_multiple_files=False, type=["pdf"])

    if uploaded_pdf is not None:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Extracted Text from PDF:", pdf_text, height=300)

        if st.button(":orange[Analyze PDF]"):
            with st.spinner('Analyzing PDF...'):
                response = get_gemini_response(pdf_text)
                st.subheader(":blue[PDF Analysis Response]")
                
                if response:
                    full_response = ""
                    for chunk in response:
                        full_response += chunk.text
                        st.write(chunk.text)
                    
                    if st.button(":orange[Save Analysis]"):
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                            tmp_file.write(full_response.encode('utf-8'))
                            st.success(f"Analysis saved to {tmp_file.name}")