# Google ADK Agents

A professional collection of automation agents built using the Google API Python Client. This project demonstrates how to integrate LLM capabilities with Google services (starting with Gmail) to automate communication and information retrieval.

## 🚀 Features

- **Gmail Automation**: Send, read, search, and manage emails programmatically.
- **Email Summarization**: Integrated logic for summarizing long email threads (placeholder ready for LLM integration).
- **Modular Architecture**: Clean separation between the agent logic, documentation, and configuration.

## 📁 Project Structure

```text
google-adk-agents/
├── src/
│   └── agents/
│       └── gmail_agent.py   # Core Gmail Agent implementation
├── docs/
│   └── connecting_gmail.md # Detailed setup guide for Google Cloud Console
├── tests/                  # Unit and integration tests
├── .gitignore              # Prevents leakage of sensitive credentials
└── requirements.txt        # Project dependencies
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/google-adk-agents.git
   cd google-adk-agents
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Setup & Configuration

To use the agents, you need to authorize the application through the Google Cloud Console. 

Please follow the detailed step-by-step guide in [docs/connecting_gmail.md](docs/connecting_gmail.md).

## 💻 Usage Example

```python
from src.agents.gmail_agent import GmailAgent

agent = GmailAgent()

# Send an email
agent.send_email("someone@example.com", "Hello from Agent", "This is a test body")

# Read and summarize latest emails
emails = agent.read_latest_emails(max_results=5)
for email in emails:
    print(f"From: {email['from']}")
    print(f"Summary: {agent.summarize_email(email['body'])}")
```

## 🛡️ Security Note

**Never** commit your `credentials.json` or `token.json` files to version control. This project includes a `.gitignore` file to protect these files by default.
