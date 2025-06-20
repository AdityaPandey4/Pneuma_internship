### **`README.md`**


# Pneuma WhatsApp FAQ Bot v0.1 – Prototype Pack

This project is a rapid prototype of a WhatsApp FAQ chatbot for Pneuma. It's a small FastAPI application designed to be a demo-ready stub that can answer a handful of key user questions with Pneuma's plain-English, quietly-witty brand voice.

### Features

*   Answers general questions ("What is Pneuma?")
*   Provides today's mock "sweet-spot" travel deals.
*   Explains the basics of mileage transfers.
*   Includes a graceful fallback for questions it doesn't understand.

---

## 🚀 Getting Started

Follow these instructions to get the bot running on your local machine for development and testing.

### 1. Prerequisites

*   Python 3.9+
*   Git

### 2. Clone the Repository

First, clone the repository to your local machine.

```bash
git clone https://github.com/AdityaPandey4/Pneuma_internship.git
cd <repository-folder-name>
```

### 3. Set Up the Environment

It is highly recommended to use a Python virtual environment to manage dependencies.

**Create a virtual environment:**
```bash
python -m venv venv
```

**Activate the virtual environment:**
*   On **macOS / Linux**:
    ```bash
    source venv/bin/activate
    ```
*   On **Windows**:
    ```bash
    venv\Scripts\activate
    ```

### 4. Install Dependencies

Install the required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### 5. Configure API Key

The bot requires an Gemini API key to function.

1.  Rename the example environment file `.env.example` to `.env`.
    *   On **macOS / Linux**:
        ```bash
        mv .env.example .env
        ```
    *   On **Windows**:
        ```bash
        rename .env.example .env
        ```
2.  Open the new `.env` file and replace `sk-...` with your actual Gemini API key.

    ```
    # .env
    Gemini_API_KEY="sk-YOUR_REAL_API_KEY_HERE"
    ```

---

## ▶️ Running the Application

With the setup complete, you can start the web server.

```bash
uvicorn main:app --reload
```

The `--reload` flag enables hot-reloading, so the server will automatically restart when you make code changes.

You should see output indicating the server is running:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
The bot is now live and waiting for requests on your local machine.

---

## 🧪 Testing the Bot

To test the bot, open a **new terminal window** (while the server is still running) and use the following `curl` commands to simulate incoming WhatsApp messages.

#### Test 1: Get Deals
```bash
curl -X POST -H "Content-Type: application/json" -d '{"Body": "show me the sweet spots", "From": "whatsapp:+1234567890"}' http://127.0.0.1:8000/whatsapp
```

#### Test 2: Explain Transfers
```bash
curl -X POST -H "Content-Type: application/json" -d '{"Body": "how do I transfer miles?", "From": "whatsapp:+1234567890"}' http://127.0.0.1:8000/whatsapp
```

#### Test 3: About Pneuma
```bash
curl -X POST -H "Content-Type: application/json" -d '{"Body": "What exactly is Pneuma?", "From": "whatsapp:+1234567890"}' http://127.0.0.1:8000/whatsapp
```

---

## 🧩 Extending the Bot

Adding a new FAQ is designed to be simple and take less than 10 minutes. The core logic is handled by adding a new `elif` block to the `route_intent` function in `main.py`.

For a detailed, step-by-step guide, please see the **`EXTENDING_THE_BOT.md`** file.

---

## ⚠️ Known Limitations

This is a v0.1 prototype with several known limitations:

*   **Basic Intent Routing:** The bot uses simple keyword matching, not sophisticated Natural Language Understanding (NLU). It can be confused by ambiguous phrasing.
*   **Static Knowledge Base:** The "sweet-spot deals" and other facts are hard-coded into the prompts in `main.py`. The bot is not connected to a live database.
*   **No Conversational Memory:** Each message is treated as a standalone query. The bot cannot remember previous parts of the conversation.