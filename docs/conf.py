from datetime import datetime

import tomllib

with open("../pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject["project"]["name"]
release = pyproject["project"]["version"]
version = ".".join(release.split(".")[:2])
author = ", ".join(author["name"] for author in pyproject["project"]["authors"])
year = datetime.now().year
copyright = f"{year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "myst_parser",
]

htmlhelp_basename = f"{project}-doc"
html_theme = "furo"
pygments_style = "sphinx"
