import os

try:
    from importlib.metadata import metadata
except ImportError:
    from importlib_metadata import metadata

PROJECT_NAME = "django-bootstrap3"

on_rtd = os.environ.get("READTHEDOCS", None) == "True"
project_metadata = metadata(PROJECT_NAME)

project = project_metadata["name"]
author = project_metadata["author"]
copyright = f"2020, {author}"

# The full version, including alpha/beta/rc tags, in x.y.z.misc format
release = project_metadata["version"]
# The short X.Y version.
version = ".".join(release.split(".")[:2])

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
pygments_style = "sphinx"
htmlhelp_basename = f"{PROJECT_NAME}-doc"

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
