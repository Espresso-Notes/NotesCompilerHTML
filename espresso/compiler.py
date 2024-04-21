import json
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader
from espresso.docs.notes import NotesSerializer, CodeBlock, ContentBlock, MarkdownBlock, NotesDocument
from espresso.docs.project import EspressoProject, ProjectSerializer
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, LatexFormatter


class NotesCompiler:

    def __init__(self, base_dir : Path, proj_template_file : Path, notes_templates_file : Path):
        self.notes_dir = base_dir / 'notes'
        self.out_dir = base_dir / 'out'
        self.templates = Environment(loader=FileSystemLoader(base_dir / 'templates'))
        self.notes_template = self.templates.get_template(notes_templates_file.name)
        self.proj_template = self.templates.get_template(proj_template_file.name)
        self.use_latex = '.tex' in notes_templates_file.name
        
        # Figure out the Formatter to use based on the template extensions
        if self.use_latex:
            self.formatter = LatexFormatter()
            logging.info('Compiler Formatter set to LaTeX.')
        else:
            self.formatter = HtmlFormatter()
            logging.info('Compiler formatter set to HTML.')

        # Load the Espresso Project
        project_file = base_dir / 'project.json'
        self.project = ProjectSerializer().load_from_file(project_file)


    def compile_notes(self, notes_doc : NotesDocument) -> Path:

        # Ensure the Content Blocks are sorted by Index
        notes_doc.content.sort(key=lambda x: x.index)

        # Render Each Content Block
        content_blocks = []
        for block in notes_doc.content:
            if block.blockType == 'markdown':
                content_blocks.append(markdown.markdown(block.text))
            elif block.blockType == 'code':
                lexer = get_lexer_by_name(block.language)
                result = highlight(block.code, lexer, self.formatter)
                content_blocks.append(result)
            elif block.blockType == 'latex':
                content_blocks.append(block.text)

        # Render the Content on the Template
        content = self.notes_template.render(
            title = notes_doc.title,
            docID = notes_doc.documentID,
            author = notes_doc.author,
            modified = notes_doc.lastModified,
            contentBlocks = content_blocks
        )

        # Save the new Content
        ext = '.tex' if self.use_latex else '.html'
        out_name = notes_doc.title + ext
        out_file = self.out_dir / out_name
        out_file.write_text(content)

        # Return the Doc Title and Path of the File Written to
        return notes_doc.title, out_file
    

    def compile_project(self, compiled_notes : list):
        content = self.proj_template.render(
            title = self.project.title,
            description = self.project.description,
            authors = ', '.join(self.project.authors),
            notes_docs = compiled_notes
        )

        ext = '.tex' if self.use_latex else '.html'
        out_name = self.project.title + ext
        out_file = self.out_dir / out_name
        out_file.write_text(content)


    def compile_all(self):
        logging.info('Compiling all files in Project Directory.')
        
        compiled_notes = []

        # Iterate through each notes file
        for file in self.notes_dir.iterdir():
            
            # If this object isn't a file, skip it
            if not file.is_file():
                continue

            # Load the Notes Document from the File
            logging.info(f'Loading NotesDocument from {file.name}')
            notes_doc = NotesSerializer.load_notes_doc(file)

            # Compile the Document
            title, out_file = self.compile_notes(notes_doc)
            compiled_notes.append({'title': title, 'file': out_file.name})

        # Compile the Project
        self.compile_project(compiled_notes)
