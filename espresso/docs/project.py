import json
from pathlib import Path
from dataclasses import dataclass

@dataclass
class EspressoProject:
    title: str
    description: str
    authors: list


class ProjectSerializer:

    def __init__(self) -> None:
        pass


    def project_exists(self, file_path: Path) -> bool:
        return file_path.exists()


    def load_from_file(self, file_path: Path) -> EspressoProject:
        json_data = json.loads(file_path.read_text())
        project = EspressoProject()
        project.title = json_data['title']
        project.description = json_data['description']
        project.authors = json_data['authors']
        return project
    

    def save_to_file(self, project: EspressoProject, file_path: Path = None, file_name: str = None) -> None:
        if file_name is None:
            file_name = 'project.json'
        if file_path is None:
            file_path = Path('.') 
        file_path = file_path / file_name
        proj_json = {
            'title' : project.title,
            'description' : project.description,
            'authors' : project.authors
        }
        file_path.write_text(json.dumps(proj_json, indent=4))


class ProjectCreator:
    
    @staticmethod
    def new_project(title: str, description: str, authors: list = [], dir_path: Path = None ) -> EspressoProject:
        project = EspressoProject(
            title = title,
            description = description,
            authors = authors
        )
        ProjectSerializer().save_to_file(project, file_path=dir_path)
        return project
    
    @staticmethod
    def random_project() -> EspressoProject:
        return ProjectCreator.new_project('Random Project', 'A randomly created project.', ['Bob'])
    
    @staticmethod
    def create_at_cli(dir_path: Path, title: str, description: str, author: str) -> EspressoProject:
        project = ProjectCreator.new_project(
            title= title if title else input('Project Title: '),
            description= description if description else input('Project Description: '),
            authors=[ author if author else input('First Author: ')],
            dir_path=dir_path
        )
        return project
