try:
    from ._version import version
except ImportError:
    try:
        from setuptools_scm import get_version

        version = get_version()
    except ImportError:
        version = "???"
__version__ = version
