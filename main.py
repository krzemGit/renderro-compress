import uvicorn

if __name__ == '__main__':
    uvicorn.run('file_compress.app:app',
                host='0.0.0.0',
                port=8009,
                reload=False)
