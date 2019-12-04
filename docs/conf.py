import os
import sys
from pkg_resources import get_distribution

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
os.environ["DJANGO_SETTINGS_MODULE"] = "tests.app.settings"

project = "django-bootstrap3"
copyright = "2014-2019, Dylan Verheul"

release = get_distribution(project).version
version = ".".join(release.split(".")[:2])

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "default"

htmlhelp_basename = "{project}-doc".format(project=project)

latex_documents = [("index", "django-bootstrap3.tex", "django-bootstrap3 Documentation", "Dylan Verheul", "manual")]

man_pages = [("index", "django-bootstrap3", "django-bootstrap3 Documentation", ["Dylan Verheul"], 1)]

texinfo_documents = [
    (
        "index",
        "django-bootstrap3",
        "django-bootstrap3 Documentation",
        "Dylan Verheul",
        "django-bootstrap3",
        "One line description of project.",
        "Miscellaneous",
    )
]

on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
