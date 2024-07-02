FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip3 install poetry
RUN poetry install

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["poetry", "run", "streamlit", "run", "wub_hub/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
