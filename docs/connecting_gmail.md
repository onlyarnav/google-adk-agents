# Connecting Your Gmail Agent to Your Account

To get the `gmail_agent.py` script working, you need to authorize it via the Google Cloud Console. Follow these steps exactly:

## Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Log in with your Gmail account.
3. Click the project dropdown (top left) and select **"New Project"**.
4. Give it a name (e.g., `My-Gmail-Agent`) and click **Create**.

## Step 2: Enable the Gmail API
1. In the search bar at the top, type **"Gmail API"**.
2. Click on the Gmail API result and click the **"Enable"** button.

## Step 3: Configure the OAuth Consent Screen
1. In the left sidebar, go to **APIs & Services** $\rightarrow$ **OAuth consent screen**.
2. Choose **"External"** (or "Internal" if you are using a Google Workspace account) and click **Create**.
3. Fill in the required App information:
   - **App name**: `Gmail Agent`
   - **User support email**: Your email address.
   - **Developer contact info**: Your email address.
4. Click **Save and Continue** through the "Scopes" and "Test Users" sections.
5. **Crucial**: In the "Test Users" section, add your own Gmail address as a test user. If you don't do this, you will get an "Access Blocked" error.

## Step 4: Create OAuth 2.0 Credentials
1. In the left sidebar, go to **APIs & Services** $\rightarrow$ **Credentials**.
2. Click **"+ Create Credentials"** $\rightarrow$ **"OAuth client ID"**.
3. For "Application type", select **"Desktop App"**.
4. Name it (e.g., `Gmail-Agent-Client`) and click **Create**.
5. You will see a "Download JSON" button for your client ID. **Download the JSON file**.

## Step 5: Setup the Project Folder
1. Rename the downloaded JSON file to `credentials.json`.
2. Move `credentials.json` into the same folder as your `gmail_agent.py` file (in this case, `D:\agents\`).

## Step 6: Running the Agent
1. Open your terminal.
2. Activate the virtual environment:
   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`
3. Run the script: `python gmail_agent.py`
4. A browser window will open asking you to log in to your Gmail account and authorize the app. 
5. After you authorize, a `token.json` file will be created automatically in your folder. This file allows the agent to stay logged in without asking you every time.
