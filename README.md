# ACEest Fitness & Gym - DevOps Assignment

A containerized Flask web application for **ACEest Fitness & Gym** with a complete CI/CD pipeline using GitHub Actions, Jenkins, Docker, and Pytest.

---

## Project Overview

This project demonstrates a full DevOps workflow for a Python Flask application:

- **Flask** web application serving gym member data, fitness classes, and a BMI calculator via REST API endpoints.
- **Pytest** unit tests (18 test cases) to comprehensively validate application behavior.
- **Docker** containerization with security best practices (non-root user) for consistent, reproducible deployments.
- **GitHub Actions** CI pipeline for automated linting (py_compile + flake8), building, and testing on every push and pull request.
- **Jenkins** pipeline (Jenkinsfile) for BUILD & quality gate integration.

---

## Project Structure

```
aceest-gym-app/
├── app.py                        # Main Flask application
├── requirements.txt              # Python dependencies
├── tests/
│   └── test_app.py               # Pytest unit tests (18 tests)
├── Dockerfile                    # Docker build instructions (optimized)
├── Jenkinsfile                   # Jenkins declarative pipeline
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI pipeline
└── README.md                     # Project documentation
```

---

## Local Installation Guide

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Docker (for containerization)
- Git

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/2024tm93650/assets-gym-app.git
   cd aceest-gym-app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   # venv\Scripts\activate         # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run the Flask App

Start the application locally:

```bash
python app.py
```

The app will be available at **http://localhost:5000**.

### Available Endpoints

| Endpoint            | Method | Description                                 |
|---------------------|--------|---------------------------------------------|
| `/`                 | GET    | Welcome message for ACEest Fitness           |
| `/members`          | GET    | JSON list of all gym members                 |
| `/members/<id>`     | GET    | Get a single member by ID                    |
| `/classes`          | GET    | JSON list of available gym classes            |
| `/bmi?weight=&height=` | GET | BMI calculator (weight in kg, height in m) |
| `/health`           | GET    | Health check endpoint                        |

### Example Requests

```bash
# Home page
curl http://localhost:5000/

# List members
curl http://localhost:5000/members

# Get a single member
curl http://localhost:5000/members/1

# List gym classes
curl http://localhost:5000/classes

# Calculate BMI
curl "http://localhost:5000/bmi?weight=70&height=1.75"

# Health check
curl http://localhost:5000/health
```

---

## How to Run Tests Manually

Run the full test suite using Pytest:

```bash
python -m pytest tests/ -v
```

Expected output (18 tests):

```
tests/test_app.py::test_home_status_code PASSED
tests/test_app.py::test_home_returns_json PASSED
tests/test_app.py::test_home_has_tagline PASSED
tests/test_app.py::test_members_status_code PASSED
tests/test_app.py::test_members_returns_json PASSED
tests/test_app.py::test_members_data_structure PASSED
tests/test_app.py::test_get_single_member PASSED
tests/test_app.py::test_get_member_not_found PASSED
tests/test_app.py::test_classes_status_code PASSED
tests/test_app.py::test_classes_returns_json PASSED
tests/test_app.py::test_classes_data_structure PASSED
tests/test_app.py::test_bmi_normal_weight PASSED
tests/test_app.py::test_bmi_overweight PASSED
tests/test_app.py::test_bmi_missing_params PASSED
tests/test_app.py::test_bmi_invalid_params PASSED
tests/test_app.py::test_calculate_bmi_underweight PASSED
tests/test_app.py::test_calculate_bmi_obese PASSED
tests/test_app.py::test_calculate_bmi_invalid_input PASSED
tests/test_app.py::test_health_endpoint PASSED
```

### Run flake8 lint check manually:

```bash
flake8 app.py tests/ --max-line-length=120 --statistics
```

---

## Docker Build & Run Instructions

### Build the Docker Image

```bash
docker build -t aceest-gym-app .
```

### Run the Docker Container

```bash
docker run -d -p 5000:5000 --name aceest-gym aceest-gym-app
```

The app will be accessible at **http://localhost:5000**.

### Run Tests Inside the Container

```bash
docker run --rm aceest-gym-app python -m pytest tests/ -v
```

### Stop and Remove the Container

```bash
docker stop aceest-gym
docker rm aceest-gym
```

### Docker Security Note

The Dockerfile is optimized for security by:
- Using `python:3.10-slim` base image (minimal attack surface).
- Running the application as a **non-root user** (`gymuser`).
- Using `--no-cache-dir` for pip to reduce image size.

---

## GitHub Actions Pipeline Explanation

The CI pipeline is defined in `.github/workflows/main.yml` and runs automatically on every **push** and **pull request** to any branch.

### Pipeline Steps

| Step | Action | Description |
|------|--------|-------------|
| 1 | **Checkout code** | Clones the repository using `actions/checkout@v4` |
| 2 | **Setup Python 3.10** | Installs Python 3.10 using `actions/setup-python@v5` |
| 3 | **Install dependencies** | Runs `pip install -r requirements.txt` |
| 4 | **Syntax check** | Runs `python -m py_compile app.py` to check for syntax errors |
| 5 | **Lint with flake8** | Runs `flake8` to enforce code quality standards |
| 6 | **Build Docker image** | Builds the Docker image with `docker build -t aceest-gym-app .` |
| 7 | **Run tests** | Executes Pytest inside the Docker container to validate all tests pass |

### How It Works

1. A developer pushes code or opens a pull request.
2. GitHub Actions automatically triggers the workflow.
3. The pipeline checks out the code, sets up the environment, and installs dependencies.
4. The code is linted with `py_compile` (syntax) and `flake8` (code quality) to catch errors early.
5. A Docker image is built to verify the containerization works.
6. Unit tests (18 tests) run inside the Docker container to ensure the application behaves correctly.
7. If any step fails, the pipeline reports the failure and blocks the merge.

---

## Jenkins BUILD & Quality Gate

The repository includes a `Jenkinsfile` that defines a declarative pipeline for the Jenkins BUILD phase. This serves as a secondary validation layer to ensure the code compiles and integrates correctly in a controlled build environment.

### How to Configure Jenkins

1. **Install Jenkins** on your server or run it via Docker:
   ```bash
   docker run -d -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
   ```
2. **Create a new Pipeline project** in Jenkins.
3. Under **Pipeline → Definition**, select **Pipeline script from SCM**.
4. Set **SCM** to **Git** and enter the repository URL:
   ```
   https://github.com/2024tm93650/assets-gym-app.git
   ```
5. Set **Branch Specifier** to `*/main`.
6. Jenkins will automatically detect the `Jenkinsfile` and run the pipeline.

### Jenkins Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Checkout** | Jenkins pulls the latest code from the Git repository. |
| **Setup** | Install Python dependencies using `pip install -r requirements.txt`. |
| **Lint** | Run `py_compile` and `flake8` to verify code has no syntax or quality issues. |
| **Build Docker Image** | Build the Docker image using `docker build -t aceest-gym-app .` |
| **Test** | Run `docker run --rm aceest-gym-app python -m pytest tests/ -v` to execute tests inside the container. |

### Jenkins + GitHub Actions Integration Logic

- **GitHub Actions** runs on every push/PR as the **first quality gate** — fast feedback for developers.
- **Jenkins** acts as the **secondary BUILD environment** — pulls code from GitHub, performs a clean build, and runs the full test suite in an isolated server environment.
- Both pipelines execute the same stages (Lint → Build → Test) ensuring **dual validation** before code reaches production.

---

## Technologies Used

- **Python 3.10** - Programming language
- **Flask 3.0** - Lightweight web framework
- **Pytest 7.4** - Testing framework
- **flake8 7.0** - Code linting and quality checks
- **Docker** - Containerization platform
- **GitHub Actions** - CI/CD automation (primary pipeline)
- **Jenkins** - CI/CD server (secondary BUILD gate)

---

## License

This project is created for educational purposes as part of a DevOps assignment.
