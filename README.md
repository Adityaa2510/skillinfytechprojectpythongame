# 🐍 Snake Arena — CI/CD & DevSecOps Project

A Python-based Snake Arena game extended into a practical DevOps and DevSecOps project, featuring automated testing, security scanning, Docker containerization, a Flask API, and Nginx load balancing across multiple backend replicas.

The project demonstrates how development, testing, security validation, containerization, and traffic distribution can fit into a modern software delivery workflow.

## 🚀 Project Overview

Snake Arena started as a Python game and was extended to explore real-world DevOps engineering concepts.

The project includes two main components:

- **Game application:** A Python and Pygame-based Snake Arena game with testable game logic.
- **API infrastructure:** A Flask API served through Gunicorn, containerized with Docker, and accessed through an Nginx load balancer.

GitHub Actions is used to automate testing and security checks. Docker Compose runs the API replicas and Nginx locally.

## ✨ Features

- 🎮 Python-based Snake Arena game
- 🧪 Automated unit tests using Pytest
- 🔍 Static Application Security Testing (SAST) with Bandit
- 📦 Dependency vulnerability auditing with pip-audit
- 🔐 Secret scanning with Gitleaks
- 🐳 Docker image creation and container-based smoke tests
- 🌐 Flask API served using Gunicorn
- ⚖️ Nginx reverse proxy and round-robin load balancing
- 🔄 Two API replicas running as separate containers
- ❤️ Health-check endpoint for API availability
- ⚙️ Docker Compose for multi-container orchestration
- 🚀 GitHub Actions CI/CD workflow

## 🏗️ Architecture

```text
                 Developer
                     |
                     v
                Git Push
                     |
                     v
             GitHub Repository
                     |
                     v
             GitHub Actions CI
                     |
        +------------+-------------+
        |            |             |
        v            v             v
    Unit Tests    Security      Dependency
      Pytest       Scans          Audit
        |            |             |
        +------------+-------------+
                     |
                     v
              Docker Image
                     |
                     v
              Docker Compose
                     |
                     v
                Nginx :80
                     |
               Host Port 8080
                     |
           +---------+---------+
           |                   |
           v                   v
       API Replica 1       API Replica 2
       Flask/Gunicorn      Flask/Gunicorn
       Port 5000           Port 5000
```

**Request flow:** A client sends a request to `http://localhost:8080`. Nginx forwards it to one of the configured API replicas. Both replicas run the same application but return different instance identifiers, making request distribution easy to demonstrate.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Game | Python, Pygame |
| API | Flask, Gunicorn |
| Testing | Pytest |
| CI/CD | GitHub Actions |
| Security | Bandit, pip-audit, Gitleaks |
| Containerization | Docker |
| Multi-container orchestration | Docker Compose |
| Reverse proxy and load balancing | Nginx |
| Version control | Git, GitHub |

## 📁 Project Structure

```text
snake-arena/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
│   └── test_game_logic.py
├── api.py
├── game.py
├── game_logic.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── tests/test_load_balancing.sh
└── README.md
```

The structure above represents the intended project layout. Keep the files in their actual locations in your repository, especially the load-balancing test script.

## ⚙️ Prerequisites

Install the following tools before running the project:

- Git
- Python 3.13 for the local game and test environment
- Docker Desktop with Docker Compose
- A code editor such as Visual Studio Code

The Docker image uses its own Python base image, so the Python version inside the container is independent of the local virtual environment.

## 💻 Run Locally on Windows

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/snake-arena.git
cd snake-arena
```

Replace `YOUR_USERNAME/snake-arena` with your actual GitHub repository path.

### 2. Create a virtual environment

```powershell
py -3.13 -m venv .venv313
.\.venv313\Scripts\Activate.ps1
```

If PowerShell blocks script execution, activate the environment using the appropriate execution policy for your machine, or run the environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the game

```powershell
python game.py
```

This launches the Pygame graphical application. The game is separate from the Flask API load-balancing demonstration.

### 5. Run unit tests

```powershell
python -m pytest -v
```

The game logic is tested independently from the graphical interface.

## 🐳 Run with Docker Compose

### 1. Build and start the services

```powershell
docker compose up --build -d
```

This starts the API replicas and Nginx.

### 2. Verify running containers

```powershell
docker compose ps
```

Expected services:

- `api1` — first API replica
- `api2` — second API replica
- `nginx` — reverse proxy and load balancer

### 3. Check the API

Open these endpoints in your browser:

- Main API: http://localhost:8080/
- Health check: http://localhost:8080/health

The root endpoint returns JSON identifying the API instance. The health endpoint returns the health status and instance identifier.

### 4. Verify Nginx configuration

```powershell
docker compose exec nginx nginx -t
```

A successful configuration test confirms that Nginx can parse its current configuration.

## ⚖️ Test Nginx Load Balancing

Send 20 requests through the same endpoint:

```powershell
1..20 | ForEach-Object {
    (Invoke-RestMethod http://localhost:8080/).instance
}
```

The output should include both:

```text
api-replica-1
api-replica-2
```

With the default round-robin configuration, requests are distributed across the configured upstream servers. The exact sequence can vary depending on request timing and server availability.

### How it works

1. The client sends a request to Nginx.
2. Nginx selects an API replica from the upstream group.
3. Gunicorn serves the request through the Flask application.
4. The API returns a JSON response containing the instance identifier.
5. Repeated requests make the distribution visible.

This is a simple demonstration of reverse proxying and load balancing. It does not, by itself, guarantee high availability or prove that every failure scenario is handled correctly.

## 🔒 DevSecOps Pipeline

The GitHub Actions workflow is designed to incorporate security checks into the development process.

| Stage | Tool | Purpose |
|---|---|---|
| Automated testing | Pytest | Validate application logic |
| Static analysis | Bandit | Identify common Python security issues |
| Dependency auditing | pip-audit | Check dependencies for known vulnerabilities |
| Secret scanning | Gitleaks | Detect potentially committed secrets |
| Image build | Docker | Package the application |
| Container smoke tests | Docker | Verify basic application imports and behavior |
| Integration testing | Docker Compose, Nginx | Validate API access through the load balancer |
| Image publishing | Docker Hub | Publish an image when the deployment job and credentials are configured |

Security tools may report findings that require investigation. A successful workflow should be confirmed from the actual GitHub Actions run; a local test does not prove that every remote pipeline job succeeds.

## 🔁 GitHub Actions Setup

Ensure the workflow exists at:

```text
.github/workflows/ci.yml
```

If your workflow publishes Docker images to Docker Hub, add these repository secrets under **GitHub → Repository → Settings → Secrets and variables → Actions**:

- `DOCKERHUB_USERNAME` — your Docker Hub username
- `DOCKERHUB_TOKEN` — a Docker Hub access token

The publishing job should run only under the intended branch and conditions, such as pushes to `main`.

After pushing a commit, open the **Actions** tab in GitHub to inspect job results and logs.

## 📋 Useful Docker Commands

Start the stack:

```powershell
docker compose up --build -d
```

View service status:

```powershell
docker compose ps
```

View application logs:

```powershell
docker compose logs -f api1 api2 nginx
```

Stop the stack:

```powershell
docker compose down
```

Rebuild the containers after configuration or source changes:

```powershell
docker compose up --build -d
```

## 🎯 What I Learned

- Structuring Python code so game logic can be tested independently
- Automating tests and security checks using GitHub Actions
- Building and running containerized applications
- Serving a Flask application using Gunicorn
- Configuring Nginx as a reverse proxy and load balancer
- Using Docker Compose to run multiple services together
- Verifying application health and observing traffic distribution
- Understanding how CI/CD and DevSecOps practices fit into a software delivery workflow

## 🔮 Future Improvements

- Add automated integration tests for API behavior
- Configure dedicated container health checks and improved failure handling
- Add HTTPS and secure production configuration
- Introduce metrics and monitoring
- Deploy the stack to a cloud environment
- Add image vulnerability scanning to the container pipeline
- Improve deployment strategies and rollback support

## 👨‍💻 Author

**Aditya Patro**

GitHub: https://github.com/Adityaa2510

Portfolio: https://adityapatro.dev

---

⭐ If you find this project useful, consider starring the repository.

*Built as a hands-on learning project to explore CI/CD, DevSecOps, containerization, and load balancing.*
