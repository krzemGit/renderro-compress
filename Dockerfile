FROM python:3.7

RUN pip install fastapi uvicorn starlette requests aiofiles

EXPOSE 80

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]