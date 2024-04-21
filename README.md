# Espresso Notes Compiler

This is the Notes Compiler for the Espresso Notes project.

To compile the project into an executable, utilize the [PyInstaller](https://pyinstaller.org/en/stable/) lib. Then simply call it:

`pyinstaller .\compiler.py`

To invoke the Compiler, use the following:

`compiler.exe base_dir`

The input `base_dir` is the base directory for the project that you are compiling. The Espresso Project file `project.json` should be in this directory, with Notes files in the `notes` subdirectory. Templates should be located in the `templates` subdirectory.

After compilation, all output files will be in the `out` directory of the supplied base directory.


## Templating

The Compiler utilizes templating to design its output files. These are per project, and can be modified by the user to suit the project. Templating uses the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) templating engine. Refer to the Jinja docs for creating templates. 

The Compiler outputs two different types of files, Project and Notes files. Project files contain the Project metadata and a listing of the Notes Documents that are part of this project. Notes files contain all of the content blocks that make up a Notes Document. Each has its own templating format.

The required files are:

- `project.html`
- `notes.html`


### Project Templates

Project Templates require the usage of 4 pieces of data.

- `title` : *string* - the Espresso Project title
- `authors` : *string* - a formatted string of Project Authors
- `description` : *string* - the Espresso Project description
- `notes_docs` : *list[dict]* - The list of Notes Documents generated as part of this project, and their file name.


### Notes Templates

Notes Templates require the usage of 5 pieces of data.

- `title` : *string* - the Notes Document title
- `author` : *string* - the Notes Document author
- `docID` : *string* - the Document Identifier
- `docmodified` : *string* - the date of the last modification
- `contentBlocks` : *list[string]* - the list of pre-formatted block strings


### Default HTML Templates 

Default HTML templates can be found at the Espresso Notes website.

- [Project Template](https://espresso-notes.github.io/templates/project.html)
- [Notes Template](https://espresso-notes.github.io/templates/notes.html)