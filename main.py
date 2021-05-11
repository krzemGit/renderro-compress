import uvicorn

if __name__ == '__main__':
    uvicorn.run('file_compress.app:app',
                host='localhost',
                port=80,
                reload=False)
