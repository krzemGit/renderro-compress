import os
import uuid
import requests
import shutil


class Process_archive:
    ''' main class, expects (1) list of links to files and (2) pathmaker object (instance) as arguments '''

    def __init__(self, link_list, pathmaker):
        self.hash = str(uuid.uuid4())
        self.link_list = link_list
        self.pathmaker = pathmaker
        self.statuses = ['processing', 'success', 'failed']
        self.timeout = 30
        self.errors = 0

    def get_hash(self):
        return self.hash

    def update_status_file(self, status):
        if status == self.statuses[0]:
            pass  # function to check if there are no similar hashes - I run out of time to do it

        # check errors and include them in status
        if status == self.statuses[1]:
            if self.errors == len(self.link_list):
                status = self.statuses[2]
            elif self.errors:
                status = f'{self.statuses[1]} with {self.errors} errors'
        with open(self.pathmaker.get_hash_status_path(f'{self.hash}.txt'), 'w') as hash_status:
            hash_status.write(status)

    def create_temp_dir(self):
        os.mkdir(self.pathmaker.get_temp_path(self.hash))

    def save_file_to_temp(self, filename, filecontent, index):
        with open(self.pathmaker.get_temp_path(self.hash, filename), 'wb') as new_file:
            shutil.copyfileobj(filecontent.raw, new_file)

    def downlaod_files_from_lists(self):
        for index, url in enumerate(self.link_list):
            try:
                with requests.get(url, timeout=self.timeout, stream=True) as file_content:
                    if file_content.ok:
                        file_name = url.split('/')[-1]
                        self.save_file_to_temp(file_name, file_content, index)
                    else:
                        self.errors += 1
            # error handling
            except requests.exceptions.HTTPError as errh:
                self.errors += 1
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                self.errors += 1
                print(errc)
            except requests.exceptions.Timeout as errt:
                self.errors += 1
                print(errt)
            except requests.exceptions.RequestException as err:
                self.errors += 1
                print(err)

    def create_archive(self):
        hash_temp_folder = self.pathmaker.get_temp_path(self.hash)
        hash_archive = self.pathmaker.get_archive_path(self.hash)
        shutil.make_archive(hash_archive, 'zip', hash_temp_folder)

    def delete_temp_dir(self):
        if os.path.isdir(self.pathmaker.get_temp_path(self.hash)):
            shutil.rmtree(self.pathmaker.get_temp_path(self.hash), self.hash)

    def execute(self):
        ''' the main method, calls other methods in desired order '''

        # print('creating status file')
        self.update_status_file(self.statuses[0])
        # print('creating temp directory')
        self.create_temp_dir()
        # print('downloading files')
        self.downlaod_files_from_lists()
        # print('creating archive')
        self.create_archive()
        # print('updating status file')
        self.update_status_file(self.statuses[1])
        # print('deleting temp folder')
        self.delete_temp_dir()
        # print('done')
