import streamlit as st

st.title('CODE:')
st.subheader('Created by Pramit Acharjya')
st.subheader('We are providing our Source code so if anyone one else wants to learn about chatbot creation can use our code for inspiration')

c='''# All Modules
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
from pathlib import Path
import time


# Configure Gemini API
load_dotenv()
safety_settings = [
    {
        "category": 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        "threshold":'BLOCK_NONE'
    },
    {
        "category": 'HARM_CATEGORY_HATE_SPEECH',
        "threshold":'BLOCK_NONE'
    },
    {
        "category": 'HARM_CATEGORY_HARASSMENT',
        "threshold": 'BLOCK_NONE'
    },
    {
        "category": 'HARM_CATEGORY_DANGEROUS_CONTENT',
        "threshold":'BLOCK_NONE'
    }
]
API_KEY=os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro',safety_settings=safety_settings)
chat = model.start_chat(history=[])



# Chat response function
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Gif Function
def gif(url: str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

def gif2(link:str):
  k=requests.get(link)
  if k.status_code!=200:
    return None
  return k.json()

# image to byte array
def image_to_byte_array(image: Image):
  imgbytear=io.BytesIO()
  image.save(imgbytear,format=image.format)
  imgbytear=imgbytear.getvalue()
  return imgbytear

   
# Header Section of Webpage

gif_code=gif('https://lottie.host/7ee14ed1-6657-403e-9473-17740461cfbb/I1mf32pHPq.json')
gif_2=gif2('https://lottie.host/f6cff35b-d653-4c9d-b487-f5cadeb54e1e/z8UNfy8G61.json')
img_path='ADD IMAGE PATH'
st.set_page_config(page_title='Ask Any Query',page_icon=':upside_down_face:',layout='wide')
st.sidebar.success('Select a page above.')


# Center the image in the middle column
co1,co2,co3=st.columns([0.2,0.09,0.2])

with co2:
    
    st.image(img_path,
             use_column_width=True,
             caption='TECHNO INDIA GROUP PUBLIC SCHOOL'
             )
st.write('---')
# Tabs
selected_page  = option_menu(
    menu_title='Main Menu',
    options=['Chat Bot',  'Chat Image Recognition'],
    orientation='horizontal',
    icons=['cast','image'],
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
if selected_page == "Chat Bot":
    col1, col2= st.columns(2)
    with col1:
        st.title('Hello I\'m Carbon. A Chat Bot Application :sunglasses:')
        print('\n')
        print('\n')
        st.header('This Applications of Artificial Intelligence based on Computer Language.')
        print('\n')
        st.subheader('How can I help you?')
    with col2:
        st_lottie(gif_code,
                  height=300,
                  speed=120,
                  key='AI')
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    input_text = st.text_input('**_Give Your Input:_**', key="input")
    submit_button = st.button(':orange[Ask Question]')
    st.write('---')
    if submit_button and input_text:
        response = get_gemini_response(input_text)
        st.session_state['chat_history'].append(('You', input_text))
        st.subheader('**:red[The Response is]** :nerd_face:')
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(('Carbon',chunk.text))
        st.write('---')
        st.subheader(":blue[Chat History]")
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
elif selected_page =="Chat Image Recognition":
    c1,c2=st.columns(2)
    with c2:
        st_lottie(gif_2,
                  height=300,
                  speed=120,
                  key='cv')
    with c1:
        st.header("Interact with Computer Vision :grinning:")
        st.write("")
        image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("Choose and Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])
        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)
            st.markdown("""<style>img {border-radius: 10px;}</style>""", unsafe_allow_html=True)
            if st.button(":orange[GET RESPONSE]", use_container_width=True):
                model = genai.GenerativeModel("gemini-pro-vision")
                if uploaded_file is not None:
                    if image_prompt != "":
                        image = Image.open(uploaded_file)
                        progress_bar=st.progress(0)
                        st.markdown("""<style>.stProgress > div > div > div > div {background-color: #00FF00;}</style>""", unsafe_allow_html=True)
                        response = model.generate_content(
                            glm.Content(
                                parts = [
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
                            progress_bar.progress(i+1)
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

'''
m='''

pip install streamlit

pip install streamlit-lottie

pip install streamlit-option-menu

pip install python-dotenv

pip install google-generativeai

pip install pillow

pip install requests

pip install pathlib


'''
select_code=st.sidebar.selectbox('Select an option',['SOURCE CODE','MODULES'])
if select_code=='SOURCE CODE':
    st.code(c,language="python")
elif select_code=='MODULES':
    st.code(m,language='python')
