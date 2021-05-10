import os


class Pathmaker:
    ''' Class for sorting the paths in the application, allows modification and nesting '''

    def __init__(self):
        self.cwd = os.getcwd()
        self.temp_dir = ['temp']
        self.movies = ['data', 'movies']
        self.hashes = ['data', 'hash_status']

    def get_temp_path(self, hash=None, filename=None):
        if filename:
            return os.path.join(self.cwd, *self.temp_dir, hash, filename)
        if hash:
            return os.path.join(self.cwd, *self.temp_dir, hash)
        return os.path.join(self.cwd, *self.temp_dir)

    def get_archive_path(self, hash=None):
        if hash:
            return os.path.join(self.cwd, *self.movies, hash)
        return os.path.join(self.cwd, *self.movies)

    def get_hash_status_path(self, hash=None):
        if hash:
            return os.path.join(self.cwd, *self.hashes, hash)
        return os.path.join(self.cwd, *self.hashes)
