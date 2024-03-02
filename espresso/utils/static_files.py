import requests
from pathlib import Path

class StaticFilesUtil:

    STATIC_FILES_URL = 'https://espresso-notes.github.io/static/'
    MANIFEST_URL = STATIC_FILES_URL + 'manifest.csv'

    def __init__(self):
        self.manifest = []


    def get_manifest(self) -> list:
        r = requests.get(self.MANIFEST_URL)
        content = r.content.decode()
        self.manifest = [x for x in content.split('\n') if x]
        return self.manifest
    

    def download_files(self, write_path: Path) -> list:
        downloaded_files = []
        for file in self.manifest:
            # Setup the Directory Structure and get the file's write path
            file_path = file.split('\\')
            new_path = write_path
            for subdir in file_path[:-1]:
                new_path = new_path / subdir
                if not new_path.is_dir():
                    new_path.mkdir()
            
            # Download the file contents
            file_name = file_path[-1]
            with requests.Session() as s:
                url = self.STATIC_FILES_URL + file
                url = url.replace('\\', '/')
                data = s.get(url)
                data = data.content.decode('utf-8')
                with open(new_path / file_name, 'w') as new_file:
                    new_file.write(data)

            downloaded_files.append(file)

        return downloaded_files