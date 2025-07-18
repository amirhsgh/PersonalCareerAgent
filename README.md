# Personal Career Agent

Personal Career Agent is a backend project designed to help users manage and develop their personal career paths. This project is built with Python and leverages FastAPI, SQLAlchemy, and Alembic for API development and database migrations.

## Features

- User authentication and management
- Chat and agent services
- File upload functionality
- Modular and scalable code structure

## Requirements

- Python 3.12+
- pip (Python package manager)
- (Recommended) Virtual environment tool such as venv or virtualenv

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amirhsgh/PersonalCareerAgent.git
   cd PersonalCareerAgent
   ```

2.1 **Install virtual environment and dependencies if you use uv package manager:**
   ```bash
   uv sync
   ```


2.2 **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Unix or MacOS:
   source .venv/bin/activate
   ```

3. **Install dependencies if you use your env:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.sample` to `.env` and fill in the required values.

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the application using uv:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Or, if you have [uv](https://github.com/encode/uv) installed (recommended for better performance):
   ```bash
   uv app.main:app --reload
   ```

7. **Access the API:**
   - Open your browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

## Project Structure
