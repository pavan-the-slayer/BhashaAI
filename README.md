# BhashaAI 🌐🤖

**AI-Powered Multilingual Customer Support Assistant**

BhashaAI is a multilingual AI customer support assistant designed to help customers get product information, pricing, stock availability, membership details, and store policy answers through a conversational interface.

The project uses a locally running AI model through Ollama and provides a web-based chat interface and a Telegram bot.

## ✨ Features

- 🌍 **Multilingual conversations:** English, Telugu, Tenglish, Hindi, and Hinglish.
- 💬 **AI-powered chat:** Natural-language customer support using Ollama.
- 🛍️ **Product assistance:** Product details, prices, and availability.
- ⭐ **Membership support:** Answers about membership benefits and discounts.
- 📦 **Store information:** Shipping and return policy assistance.
- 🌐 **Web interface:** Browser-based customer support chat.
- 📱 **Telegram integration:** Chat with BhashaAI through Telegram.
- 🖥️ **Local AI inference:** Run the language model on your own machine using Ollama.

## 🛠️ Technology Stack

- **Language:** Python
- **Web framework:** Flask
- **AI runtime:** Ollama
- **Language model:** Qwen3 14B
- **Frontend:** HTML, CSS, JavaScript
- **Messaging integration:** Telegram Bot API
- **Data:** JSON and Excel-based store information

## 📁 Project Structure

```text
BhashaAI/
├── app.py
├── telegram_bot.py
├── test_ai.py
├── Modelfile
├── Store_Data.xlsx
├── store_data.json
├── static/
│   ├── script.js
│   ├── style.css
│   └── store.css
└── templates/
    ├── index.html
    ├── store.html
    ├── requirements.txt
    └── store_data.json
```

## ⚙️ Prerequisites

Before running BhashaAI, install:

- Python 3.11
- Ollama
- Git (optional, for cloning the repository)

You also need the Qwen3 model configured in Ollama.

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/BhashaAI.git
cd BhashaAI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the Python packages required by the project. If your dependency file is in the `templates` folder, run:

```powershell
pip install -r templates/requirements.txt
```

### 4. Install and start Ollama

Install Ollama from [ollama.com](https://ollama.com), then download the model:

```powershell
ollama pull qwen3:14b
```

Make sure Ollama is running before starting the application.

### 5. Start the web application

```powershell
python app.py
```

Open the local address shown in the terminal, usually:

`http://127.0.0.1:5000`

### 6. Start the Telegram bot

Configure your Telegram bot token in a local `.env` file using the variable expected by `telegram_bot.py`:

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Keep `.env` private and never commit API keys or bot tokens to GitHub.

In another terminal, activate the virtual environment and run:

```powershell
python telegram_bot.py
```

## 🔐 Security Notes

- Never upload `.env` files, bot tokens, API keys, or passwords.
- Keep local virtual environments and temporary files out of version control.
- Use a private repository if your project contains confidential information.

## 🗺️ Future Improvements

- Voice-based customer support.
- Integration with e-commerce platforms.
- Improved product and order query handling.
- Admin dashboard for managing store information.
- Production deployment with authentication and monitoring.

## 👨‍💻 Project Status

BhashaAI is an evolving project focused on multilingual AI-powered customer support.

## 📄 License

No license has been specified yet. Add a license before distributing the project for reuse.
