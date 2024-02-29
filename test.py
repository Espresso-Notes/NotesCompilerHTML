import os
import json
import time
from pathlib import Path
from espresso.utils.directory_utils import setup_output_directory
from espresso.docs.notes_doc import NotesDocument
from espresso.compiler import NotesCompiler
import logging

def main():
    # Set the current working directory to the notebook
    test_dir = Path('.') / 'tests'
    if not test_dir.is_dir():
        test_dir.mkdir()
    os.chdir(test_dir)
    base_path = Path('.')

    # Setup logging
    log_dir : Path = base_path / 'logs'
    if not log_dir.is_dir():
        log_dir.mkdir()
    log_file = log_dir / 'notes.log'
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logging.info(f'Starting new test run. {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')

    # Setup the Environment
    setup_environment(base_path)
    
    # Generate Test Documents
    generate_test_documents(base_path / 'notes', 3)

    # Compile Test Documents
    c = NotesCompiler(base_path)
    c.compile()


def setup_environment(base_path = Path('.')) -> None:
    logging.info('Setting up the test environment directory structure.')
    
    # Setup the Notes Directory
    notes_dir : Path = base_path / 'notes'
    if not notes_dir.is_dir():
        notes_dir.mkdir()
    
    # Setup the Static Directory
    static_dir = base_path / 'static'
    if not static_dir.is_dir():
        static_dir.mkdir()
    
    # Setup the CSS Directory
    css_dir = static_dir / 'css'
    if not css_dir.is_dir():
        css_dir.mkdir()

    # Setup the Templates Directory
    templates_dir = static_dir / 'templates'
    if not templates_dir.is_dir():
        templates_dir.mkdir()

    # TODO: Download Default Files from the Website

    # Setup the Output Directories
    setup_output_directory(base_path)


def generate_test_documents( notes_path : Path, num_docs = 1) -> None:
    for i in range(num_docs):
        logging.info(f'Generating test document #{i+1}.')
        test_file = notes_path / f'test_notes{i+1}.json'
        test_data = NotesDocument.gen_random_data()
        test_file.write_text(json.dumps(test_data, indent=4, default=lambda o: o.__dict__))


if __name__ == '__main__':
    main()