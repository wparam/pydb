FROM pyodbc

WORKDIR /app

# Copy code to container
COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-i", "main.py"]
