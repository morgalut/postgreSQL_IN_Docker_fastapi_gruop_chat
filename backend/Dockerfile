FROM ubuntu:20.04  
RUN apt-get update && apt-get install -y python3 python3-pip ping curl
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
