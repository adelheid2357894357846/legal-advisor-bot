FROM python:3.12-slim

WORKDIR /app

COPY frontend/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/ /app/

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]