FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY studio/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY studio /app/studio
COPY lewice.exe /app/lewice.exe
RUN chmod 755 /app/lewice.exe

EXPOSE 8501

CMD ["streamlit", "run", "/app/studio/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
