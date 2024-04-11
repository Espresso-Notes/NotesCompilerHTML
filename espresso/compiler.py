import json
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader
from espresso.docs.notes import NotesSerializer, CodeBlock, ContentBlock, MarkdownBlock, NotesDocument
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


class NotesCompiler:

    def __init__(self, base_dir : Path):
        self.notes_dir = base_dir / 'notes'
        self.out_dir = base_dir / 'out'
        self.templates = Environment(loader=FileSystemLoader(base_dir / 'templates'))


    def list_notes_files(self) -> list:
        return [
            doc for doc in self.notes_dir.iterdir()
                if doc.is_file()
        ]
    

    def load_notes_docs(self) -> list:
        files = self.list_notes_files()
        docs = []
        for file in files:
            doc = NotesSerializer.load_notes_doc(file)
            docs.append(doc)
        return docs

    def compile_doc(self, notes_doc : NotesDocument) -> None:
        # Get the template being used
        template = self.templates.get_template('notes.html')

        # Get the Notes File

        # Ensure the Content Blocks are sorted by Index
        notes_doc.content.sort(key=lambda x: x.index)

        # Render Each Content Block
        content_blocks = []
        for block in notes_doc.content:
            if block.blockType == 'markdown':
                content_blocks.append(markdown.markdown(block.text))
            elif block.blockType == 'code':
                lexer = get_lexer_by_name(block.language)
                formatter = HtmlFormatter(linenos='inline')
                result = highlight(block.code, lexer, formatter)
                content_blocks.append(result)
            elif block.blockType == 'latex':
                content_blocks.append(block.text)

        # Render the Content on the Template
        content = template.render(
            title = notes_doc.title,
            docID = notes_doc.documentID,
            author = notes_doc.author,
            modified = notes_doc.lastModified,
            contentBlocks = content_blocks
        )

        # Save the new Content
        out_name = notes_doc.title + '.html'
        out_file = self.out_dir / out_name
        out_file.write_text(content)


    def compile_all(self):
        docs = self.load_notes_docs()
        for doc in docs:
            self.compile_doc(doc)
        



    

