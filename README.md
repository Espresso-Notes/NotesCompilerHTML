# NotesCompilerHTML
A compiler implementation to generate HTML content files from Espresso Notes Documents.


## Program Flow
1. Validate the input Notes JSON file(s) as valid Notes File.
2. Ensure valid directory structure for output.
3. Copy static files to output directory.
4. Compile Notes JSON file to HTML content file.


## Command Line Interface (CLI)

This is a list of the commands and options available for usage. 
By default, the Compiler will search in the base directory for the project files.

- `--directory` or `-d`: The directory location of the Project files.
- `--project` or `-p`: Compile a full Project.
- `--file` or `-f`: Compile a standalone Notes File.
- `--addmd <input> <doc>`: Add an `input` markdown file to the `doc` Notes Document as a new Markdown Block at the end.
- `--latex` or `-l`: Compile to LaTeX instead of HTML
- `--template` or `-t`: Compile using this template

