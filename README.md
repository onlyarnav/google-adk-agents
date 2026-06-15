# Google ADK Agents

A professional collection of automation agents built using the Google API Python Client. This project demonstrates how to integrate LLM capabilities with Google services (starting with Gmail) to automate communication and information retrieval.

## 🚀 Features

- **Gmail Automation**: Send, read, search, and manage emails programmatically.
- **Advanced Emailing**: Support for CC, BCC, multiple recipients, HTML bodies (links), and file attachments.
- **Email Summarization**: Integrated logic for summarizing long email threads (placeholder ready for LLM integration).
- **Agent Hub Architecture**: Centralized management for all agents, making it easy to scale the project with new Google service agents.

## 📁 Project Structure

```text
google-adk-agents/
├── src/
│   ├── hub.py               # Central Agent Hub for accessing all agents
│   └── agents/
│       ├── __init__.py
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

You can use the `AgentHub` to manage all your agents from a single place.

```python
from src.hub import AgentHub

# Initialize the Hub
hub = AgentHub()

# Get the Gmail Agent
gmail = hub.get_agent('gmail')

# Send a professional email with CC, BCC, and Attachments
gmail.send_email(
    to=["recipient1@example.com", "recipient2@example.com"],
    subject="Quarterly Report",
    body="<h1 style='color:blue;'>Hello Team</h1><p>Please find the report attached and check the <a href='https://google.com'>link</a>.</p>",
    cc="manager@example.com",
    bcc="archive@example.com",
    attachments=["report.pdf"],
    is_html=True
)

# Read and summarize latest emails
emails = gmail.read_latest_emails(max_results=5)
for email in emails:
    print(f"From: {email['from']}")
    print(f"Summary: {gmail.summarize_email(email['body'])}")
```

## 🛡️ Security Note

**Never** commit your `credentials.json` or `token.json` files to version control. This project includes a `.gitignore` file to protect these files by default.
