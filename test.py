from pathlib import Path
from espresso.compiler import NotesCompiler
from pygments.formatters import HtmlFormatter

def run_test():
    compiler = NotesCompiler(Path('./tests'))
    css_dir = Path('./tests/out/css')
    css_file = css_dir / 'pygmentize.css'
    css_file.write_text(HtmlFormatter().get_style_defs('.highlight'))
    compiler.compile_all()


if __name__ == '__main__':
    run_test()