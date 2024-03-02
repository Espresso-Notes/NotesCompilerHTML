import json
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader
from espresso.docs.notes_doc import NotesDocument
import markdown


class NotesCompiler:

    def __init__(self, base_path : Path):
        self.notes_path : Path = base_path / 'notes'
        self.templates_path : Path = base_path / 'static' / 'html' / 'templates'
        self.out_path = base_path / 'out' / 'html'
        self.notes_files = [x for x in self.notes_path.iterdir() if x.is_file()]
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_path))

    def compile(self):
        logging.info('Starting compilation of notes files.')
        for file in self.notes_files:
            # Load the Notes Data
            out_file = self.out_path / f'{file.name.split(".")[0]}.html'
            notes_json = json.loads(file.read_text())
            notes_data = NotesDocument(notes_json)

            # Format the Notes Content
            data = {}
            data['title'] = markdown.markdown(f'# {notes_data.title}')
            data['documentID'] = markdown.markdown(f'`ID: {notes_data.documentID}`')
            data['author'] = markdown.markdown(f'Author: {notes_data.author}')
            data['lastModified'] = markdown.markdown(f'Last Modified: {notes_data.lastModified}')
            data['blocks'] = []
            for block in notes_data.content:
                data['blocks'].append(markdown.markdown(block.content))
            
            # Render the Notes Content
            template = self.jinja_env.get_template('notes.html')
            content = template.render(content=data)
            out_file.write_text(content)

