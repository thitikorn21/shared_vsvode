# 🚀 Broadcast Data Platform (Mockup Integration)

A comprehensive dashboard platform designed for simulating and managing LINE Broadcast data. This project demonstrates a **Full Stack** implementation connecting a **React Frontend** with a **Databricks SQL Warehouse** via a **FastAPI** middleware.

## ✨ Features

* **Interactive Dashboard:** Built with React (CDN), Tailwind CSS, and Lucide Icons.
* **Real-time Data Fetching:** Displays Daily Stats and Flex Message Performance from Databricks.
* **Secure Backend:** Python FastAPI server handling DB connections securely using Environment Variables.
* **Mockup Capability:** Visualizes campaign performance, CTR, and estimated costs.

## 🛠 Tech Stack

* **Frontend:** HTML5, React 18, Tailwind CSS, Chart.js
* **Backend:** Python 3.x, FastAPI, Uvicorn
* **Database:** Databricks SQL (via Connector)
* **Security:** `python-dotenv` for configuration management

## ⚙️ Prerequisites

* Python 3.9+ installed
* A Databricks Workspace & Access Token

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/broadcast-data-platform.git](https://github.com/YOUR_USERNAME/broadcast-data-platform.git)
    cd broadcast-data-platform
    ```

2.  **Create Virtual Environment**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration (.env)**
    Create a `.env` file in the root directory and add your Databricks credentials:
    *(Note: This file is ignored by Git for security)*
    ```env
    DATABRICKS_SERVER_HOSTNAME=your-server-hostname.gcp.databricks.com
    DATABRICKS_HTTP_PATH=sql/protocolv1/o/xxxx/xxxx
    DATABRICKS_TOKEN=dapixxxxxxxxxx
    ```

## 🚀 How to Run

1.  **Start the Backend Server**
    ```bash
    uvicorn backend_api:app --reload --port 8001
    ```
    *Server will start at `http://localhost:8001`*

2.  **Launch the Frontend**
    * Open `index.html` (or your main html file) directly in your browser.
    * Or use Live Server in VS Code.

## 📝 Project Structure

```text
├── .env                 # Secrets (Not on GitHub)
├── .venv/               # Virtual Environment (Not on GitHub)
├── backend_api.py       # Main API Server
├── index.html           # Main Frontend Dashboard
├── requirements.txt     # Python Dependencies
└── README.md            # Documentation