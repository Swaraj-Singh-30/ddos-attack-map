# Live DDoS Attack Map
> **Note:** This project is currently under active development and not yet ready for production use.

### 🌐 About the Project

This is a real-time DDoS attack visualization project that monitors and displays cyber-attacks on a global map. The backend collects data on malicious IP activity from various sources, uses a machine learning model to classify attacks, and provides this data to a frontend globe for visualization.

---

### 🚀 Features

* **Real-time Monitoring:** Collects and processes data on attack spikes and malicious IPs from third-party APIs.
* **Intelligent Classification:** Uses a machine learning model to assign a confidence score to potential DDoS attacks.
* **Interactive Globe Visualization:** Displays the geographic location of attacks on a dynamic, 3D globe.
* **API-driven Backend:** A high-performance FastAPI backend serves the attack data to the frontend.

---

### 💻 Tech Stack

**Backend:**
* **Framework:** FastAPI
* **Data Sources:** Cloudflare Radar, AbuseIPDB
* **Machine Learning:** Scikit-learn
* **Dependencies:** Python, Pandas, Requests, Pydantic

**Frontend:**
* **Visualization:** Three.js
* **Core:** HTML, CSS, JavaScript

**Containerization:**
* Docker
* Docker Compose

---

### ✅ Prerequisites

Before you begin, ensure you have the following installed:
* **Git**
* **Docker**
* **Docker Compose**

You will also need to obtain API keys for the following services:
* **AbuseIPDB:** [https://www.abuseipdb.com/](https://www.abuseipdb.com/)
* **Cloudflare Radar:** [https://radar.cloudflare.com/](https://radar.cloudflare.com/)

---

### ⚙️ Getting Started

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd ddos-attack-map
    ```
2.  **Configure environment variables:**
    Create a `.env` file in the root directory and add your API keys.
    ```
    ABUSEIPDB_API_KEY=your_abuseipdb_key_here
    CLOUDFLARE_API_TOKEN=your_cloudflare_token_here
    ```
3.  **Build and run with Docker Compose:**
    This command will build the Docker image for the backend and start the container.
    ```bash
    docker-compose up --build
    ```
    Your FastAPI backend will be available at `http://localhost:8000`.

---

### 📂 Folder Structure
```
ddos-attack-map/
├── .dockerignore          # Docker ignore file
├── .env                   # Environment variables
├── docker-compose.yml     # Docker compose configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── backend/              # Backend service directory
│   ├── app/             # FastAPI application
│   │   └── ...         # Backend source files
│   └── Dockerfile      # Backend container configuration
│
└── frontend/            # Frontend service directory
    ├── index.html      # Main HTML file
    └── ...             # Frontend assets and source files
```


---

### 🔜 Next Steps

* **Implement data fetching logic** from AbuseIPDB and Cloudflare Radar.
* **Build the machine learning model** to classify attack confidence.
* **Develop the frontend visualization** to display the data on the globe.

I have ignored the warning of InconsistentVersionWarning for scikit-learn in the requirements.txt file for now, as it does not affect the functionality of the project. This could taken as a good first issue for someone looking to contribute(after the project is complete).
