from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class NotesDocument:
    documentID : str
    title : str
    author : str
    lastModified : str
    content : list

@dataclass
class ContentBlock:
    contentID : int
    index : int
    blockType : str

@dataclass
class MarkdownBlock(ContentBlock):
    text : str

@dataclass
class CodeBlock(ContentBlock):
    code : str
    language : str

@dataclass
class LaTeXBlock(ContentBlock):
    text : str


class NotesSerializer:

    @staticmethod
    def load_notes_doc(file : Path) -> NotesDocument:
        raw_text = file.read_text()
        json_data = json.loads(raw_text)

        # Setup the Notes Document Meta Data
        notes_doc = NotesDocument(
            documentID = json_data['documentID'],
            title = json_data['title'],
            author = json_data['author'],
            lastModified= json_data['lastModified'],
            content = []
        )

        # Iterate through the various content blocks
        for block in json_data['content']:
            # Markdown Content Blocks
            if block['blockType'] == 'markdown':
                new_block = MarkdownBlock(
                    contentID = len(notes_doc.content),
                    index = block['index'],
                    text = block['content'],
                    blockType='markdown'
                )
            
            # Code Content Blocks
            elif block['blockType'] == 'code':
                new_block = CodeBlock(
                    contentID = len(notes_doc.content),
                    index = block['index'],
                    code = block['code'],
                    language = block['language'],
                    blockType='code'
                )
            
            # LaTeX Content Blocks
            elif block['blockType'] == 'latex':
                new_block = LaTeXBlock(
                    contentID = len(notes_doc.content),
                    index = block['index'],
                    text = block['text'],
                    blockType='latex'
                )

            notes_doc.content.append(new_block)
        return notes_doc
    

    @staticmethod
    def save_notes_doc(notes: NotesDocument, file_path: Path) -> None:
        data = {}
        data['documentID'] = notes.documentID
        data['title'] = notes.title
        data['author'] = notes.author
        data['lastModified'] = notes.lastModified
        data['content'] = []
        for block in notes.content:
            block_data = {}
            block_data['index'] = block.index
            block_data['blockType'] = block.blockType
            if block.blockType == 'markdown':
                block_data['content'] = block.text
            elif block.blockType == 'code':
                block_data['language'] = block.language
                block_data['code'] = block.code
            elif block.blockType == 'latex':
                block_data['text'] = block.text
            data['content'].append(block_data)
        file_path.write_text(json.dumps(data, indent=4))

