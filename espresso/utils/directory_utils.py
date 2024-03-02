from pathlib import Path

def setup_output_directory( base_path : Path ):
    # Check if the 'out' directory exists
    out_path : Path = base_path / 'out'
    if not out_path.is_dir():
        out_path.mkdir()

    # Check if the 'html' directory exists
    html_path : Path = out_path / 'html'
    if not html_path.is_dir():
        html_path.mkdir()

    # Check if the 'css' directory exists
    out_css_path : Path = html_path / 'css'
    if not out_css_path.is_dir():
        out_css_path.mkdir()

    # Copy the HTML files into the css directory
    static_css_path : Path = base_path / 'static' / 'html' / 'css'
    for in_file in static_css_path.iterdir():
        out_file : Path = out_css_path / in_file.name
        out_file.write_text(in_file.read_text())
    