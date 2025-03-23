# Legal Advisor Bot

A Dockerized application providing legal advisory services through a FastAPI backend with LangChain (some LangGraph too,for memory node) OpenAI integration, and a frontend for user interaction.

## Project Structure

```
legal-advisor-bot/
├── backend/                # Backend directory
│   ├── chat_service.py     # Chat service logic
│   ├── database.py         # Database configuration
│   ├── Dockerfile          # Docker configuration for backend
│   ├── main.py             # FastAPI application
│   └── requirements.txt    # Backend dependencies
├── frontend/               # Frontend directory
│   ├── app.py              # Frontend application
│   ├── Dockerfile          # Docker configuration for frontend
│   ├── requirements.txt    # Frontend dependencies
│   └── style.css           # Frontend styling
├── .env                    # Environment variables (not tracked)
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
```

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/adelheid2357894357846/legal-advisor-bot
   cd legal-advisor-bot
   ```

2. **Configure Environment Variables**
   - Copy the `.env.example` file to `.env` in the project root:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` to include your specific environment variables (e.g., API keys, database credentials, endpoints). Refer to `.env.example` for the required variables.
   - Don't forget to create a db in PostgreSQL (pgadmin4.exe) and have it running for this to work.

3. **Build and Run the Project**
   - From the project root, run the following command to build and start the services:
     ```bash
     docker-compose up --build
     ```
   - This will build the Docker images for the backend (FastAPI + LLM) and frontend, then start the containers.

4. **Access the Application**
   - Once running, the frontend should be accessible at `http://localhost:8000` (port specified in `docker-compose.yml`), by default 8000.
   - The backend API endpoints will be available at `http://localhost:8501` (port specified in `docker-compose.yml`), by default 8501.

## Environment Variables

All environment variables and API endpoints **must** be defined in the `.env` file in the project root( YOU CAN CHANGE where .env can be by changing docker-compose.yml setup). An example configuration is provided in `.env.example`. Common variables include:

- OpenAI API keys
- Database connection strings
- Service-specific endpoints

Ensure `.env` is properly configured before building the project.

## Services

- **Backend**: A FastAPI application with LangChain and OpenAI integration for legal advisory logic.
- **Frontend**: A simple interface styled with `style.css` and powered by `app.py`.

## Stopping the Application

To stop the running containers, press `Ctrl+C` in the terminal where `docker-compose up` is running, or use:
```bash
docker-compose down ( open split,second terminal in root project for this)
```

## Troubleshooting

- Ensure all ports specified in `docker-compose.yml` are free.
- Verify that the `.env` file contains all required variables.
- Check Docker logs for errors:
  ```bash
  docker-compose logs
  ```
