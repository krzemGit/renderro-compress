FROM python:3.7

RUN pip install fastapi uvicorn starlette requests aiofiles

WORKDIR /app

COPY . /app

EXPOSE 8000

CMD ["python", "main.py"]
