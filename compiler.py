from pathlib import Path
import logging
import argparse

from espresso.compiler import NotesCompiler

# Setup logging
logger = logging.getLogger('compiler.log')
logging.basicConfig(filename='compiler.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='[%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def main():
    logging.info('Starting EspressoNotesCompiler')

    # Setup Command Line Args
    parser = argparse.ArgumentParser(
        prog='EspressoNotesCompiler',
        description='Compiles Espresso Notes Documents into target format.'
    )

    parser.add_argument('base_dir')
    parser.add_argument('-l','--latex', action='store_true')

    # Get the Command Line Arguments
    args = parser.parse_args()
    base_dir = Path(args.base_dir)
    use_latex = args.latex

    logging.info('Retrieving command line arguments.')
    logging.info(f'Notes Directory: {args.base_dir}')
    logging.info(f'Target Format: {"LaTeX" if use_latex else "HTML"}')
    
    # Get the Template Files
    logging.info('Checking for template files.')
    template_dir = base_dir / 'templates'

    for file in template_dir.iterdir():
        if file.is_file():
            logging.info(f'Found template file: {file}')
    
    if use_latex:
        notes_template_file = template_dir / 'notes.tex'
        project_template_file = template_dir / 'project.tex'
    else:
        notes_template_file = template_dir / 'notes.html'
        project_template_file = template_dir / 'project.html'

    # Check that the Template Files exist
    if not notes_template_file.exists():
        logging.error(f'Template file {notes_template_file} not found.')
        return
    if not project_template_file.exists():
        logging.error(f'Project template file {project_template_file} not found.')
        return
    
    compiler = NotesCompiler(base_dir, project_template_file, notes_template_file)
    compiler.compile_all()


if __name__ == '__main__':
    main()