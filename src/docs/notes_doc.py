import json
from typing import List
from faker import Faker
from mdgen import MarkdownPostProvider
import uuid
import random

class NotesDocument:
    class Content(list):
        class Items:
            def __init__(self, values: dict = None):
                values = values if values is not None else {}
                self.blockType: str = values.get("blockType", None)
                self.content: str = values.get("content", None)
            
            def reprJson(self):
                return self.__dict__

        def __init__(self, values: list = None):
            super().__init__()
            values = values if values is not None else []
            self[:] = [self.Items(value) for value in values]

        def reprJson(self):
            return self.__dict__

    def __init__(self, values: dict = None):
        values = values if values is not None else {}
        self.documentID: str = values.get("documentID", None)
        self.title: str = values.get("title", None)
        self.author: str = values.get("author", None)
        self.lastModified: int = values.get("lastModified", None)
        self.content: List[Items] = self.Content(values=values.get("content"))

    def reprJson(self):
        return dict(title=self.title, lastModified=self.lastModified, author=self.author,
                    documentID=self.documentID, content=[d.__dict__ for d in self.content])
    
    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(json.dumps(self, indent=4, default=lambda o: o.__dict__))

    def load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            source = json.loads(file)

    @staticmethod
    def gen_random_data():
        fake = Faker()
        fake.add_provider(MarkdownPostProvider)

        notes_doc = NotesDocument()
        notes_doc.author = fake.name()
        notes_doc.documentID = str(uuid.uuid4())
        notes_doc.title = "Test Document"
        notes_doc.lastModified = fake.time()
        for x in range(5):
            post = NotesDocument.Content.Items()
            post.blockType = 'markdown'
            post.content = fake.post(size=random.choice(['small', 'medium', 'large']))
            notes_doc.content.append(post)
        
        return notes_doc

class NotesDocJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

