import json
from docs.notes_doc import NotesDocument
import markdown

def compile():
    notes_doc = NotesDocument.gen_random_data()
    notes_doc.save_to_file('test/test_data.json')

    with open('test/test.html','w') as html_file:
        html_file.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
        html_file.write('<link rel="stylesheet" href="github-markdown.css">')
        html_file.write('<style>'
                    '.markdown-body {'
                        'box-sizing: border-box;'
                        'min-width: 200px;'
                        'max-width: 980px;'
                        'margin: 0 auto;'
                        'padding: 45px;'
                    '}'
                    ' '
                    '@media (max-width: 767px) {'
                        '.markdown-body {'
                            'padding: 15px;'
                        '}'
                    '}'
                '</style>')
        html_file.write('<article class="markdown-body">')
        html_file.write(markdown.markdown(f'# {notes_doc.title}'))
        html_file.write(markdown.markdown(f'`ID: {notes_doc.documentID}`'))
        html_file.write(markdown.markdown(f'Author: {notes_doc.author}'))
        html_file.write(markdown.markdown(f'Last Modified: {notes_doc.lastModified}'))
        for content in notes_doc.content:
            html_file.write(markdown.markdown(content.content))

        html_file.write('</article>')

if __name__ == '__main__':
    compile()