from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse
import os

from .process_archive import Process_archive
from .pathmaker import Pathmaker

app = FastAPI()


class ItemList(BaseModel):
    urls: list


# object for path creation
pathmaker = Pathmaker()


@app.get('/', tags=['main'])
def welcome() -> dict:
    return {'message': 'Welcome to the file compressor! (by Lech Krzemiński)'}


@app.post('/api/archive/create', tags=['archive'])
async def create_archive(urls: ItemList, background_tasks: BackgroundTasks) -> dict:

    link_list = urls.urls

    # check urls for https:// at the start
    for index, link in enumerate(link_list):
        if not link.startswith('https://'):
            link_list[index] = ''.join(['https://', link])

    process_archive = Process_archive(link_list, pathmaker)

    hash = process_archive.get_hash()

    background_tasks.add_task(process_archive.execute)

    return {'hash': hash}


@app.get('/api/archive/status/{hash}', tags=['archive'])
def check_hash_status(hash: str) -> dict:

    status = 'error'
    info_path = pathmaker.get_hash_status_path(f'{hash}.txt')

    # error if path/hash is incorrect
    if not os.path.isfile(info_path):
        return {'error': 'Incorrect hash, no such archive'}

    with open(info_path, 'r') as hash_status:
        status = hash_status.read()

    return {'status': status, 'url': f'http://0.0.0.0:8009/api/archive/get/{hash}'}


@app.get('/api/archive/get/{hash}', tags=['archive'])
def get_archive(hash: str):

    status = 'unknown'
    file_path = pathmaker.get_archive_path(f'{hash}.zip')

    # check if archive exists
    if not os.path.isfile(file_path):
        return {'error': 'Incorrect hash, no such archive'}

    # check if the archive creation is done
    with open(pathmaker.get_hash_status_path(f'{hash}.txt'), 'r') as status_file:
        status = str(status_file.read())

    if not status.startswith('success'):
        return {'error': 'The processing of your file is not done, please wait a while'}

    # return
    return FileResponse(file_path)
