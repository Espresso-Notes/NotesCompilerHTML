import json
import random
from faker import Faker
import uuid
from mdgen import MarkdownPostProvider

from src.docs.notes_doc import NotesDocument, NotesDocJsonEncoder

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

notes_doc.save_to_file('test/test_data.json')
with ('test/test_data.json', 'r') as source:
    data = NotesDocument(**json.loads(source))