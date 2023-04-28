import importlib
import os
from configparser import ConfigParser
from datetime import datetime

on_rtd = os.environ.get("READTHEDOCS", None) == "True"

config_parser = ConfigParser()
config_parser.read("../setup.cfg")
metadata = config_parser["metadata"]

project = "bootstrap3"
project_with_underscores = project.replace("-", "_")

module = importlib.import_module(f"{project_with_underscores}")
# The full version, including alpha/beta/rc tags, in x.y.z.misc format
release = module.__version__
# The short X.Y version.
version = ".".join(release.split(".")[:2])

author = metadata["author"]
year = datetime.now().year
copyright = f"{year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]
pygments_style = "sphinx"
htmlhelp_basename = f"{project}-doc"

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
