from pathlib import Path
import click
import logging

from espresso.docs.project import EspressoProject, ProjectCreator, ProjectSerializer

# Setup logging
logger = logging.getLogger('compiler.log')
logging.basicConfig(filename='compiler.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='[%(levelname)s] [%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


@click.group()
def compiler_group():
    pass
    

@compiler_group.command()
@click.option('--directory', default='.', help='The directory for the project.')
@click.option('--title', default=None, help='The title of the project.')
@click.option('--description', default=None, help='The description of the project.')
@click.option('--author', default=None, help='The first author of the project.')
def new(directory, title, description, author):
    """Create a new project."""
    logging.info(f'Creating a new project.')
    ProjectCreator.create_at_cli(Path(directory), title, description, author)


@compiler_group.command()
@click.argument('file_path')
def file(file_path: str):
    """Compiles a single Notes Doc."""
    logging.info(f'Processing compilation of single notes file {file_path}')
    path = Path(file_path)
    

if __name__ == '__main__':
    compiler_group()