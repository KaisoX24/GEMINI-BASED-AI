# 🤖 Carbon ChatBot – AI Chat, Image Recognition & PDF Analysis

Welcome to **Carbon**, your multi-functional AI assistant built using **Streamlit** and powered by **Google Gemini** (Generative AI). Carbon isn't just a chatbot—it's a full-fledged assistant that can recognize images, read PDFs, and respond intelligently to your queries.

---

## 🚀 Features

- 🔹 **Chat Bot** – Ask anything and get real-time responses powered by Gemini 1.5 Flash.
- 🖼️ **Image Recognition (Coming Soon)** – Upload an image and let AI describe or analyze it. *(Module loaded, logic can be extended)*
- 📄 **PDF Analyzer** – Upload a PDF and extract its textual content with a single click.
- ✨ Lottie animations – Smooth, animated UI elements for a delightful experience.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Streamlit** | Frontend Web App framework |
| **Google Gemini API** | AI model for chatbot responses |
| **PyMuPDF (fitz)** | PDF parsing and text extraction |
| **Lottie Animations** | Animated visuals |
| **dotenv** | Securely manage API keys |
| **Pillow (PIL)** | Image handling |
| **Requests** | API interaction for Lottie |

---

## 📂 Project Structure

```
carbon-chatbot/
│
├── 1_🤖_Chat.py           # Main Streamlit app
├── .env                   # Environment file with API key
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🔑 Environment Setup

Before running the app, make sure to set up your environment:

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Setup .env**

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

This will launch your app in the browser at `http://localhost:8501`.

---


## 💡 Inspiration

This project was created to explore the powerful capabilities of Google’s Generative AI (Gemini) and demonstrate real-world applications of AI in communication and file analysis.

---

## 🧠 Credits

Developed by Pramit Acharjya and Indudip Biswas.

---

## 📃 License

This project is licensed under the MIT License. Feel free to use, modify, and share!
