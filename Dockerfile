FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py server.py ./
COPY quiz_bank ./quiz_bank
COPY templates ./templates
COPY static ./static
ENV PORT=4173
EXPOSE 4173
CMD ["python", "server.py"]
