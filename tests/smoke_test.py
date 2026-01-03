"""
Minimal smoke test.

This test verifies that the package can be installed and that
its most basic public API is usable. It intentionally avoids
test frameworks and any optional dependencies.
"""


def main():
    import django

    import bootstrap3

    # Basic imports work
    assert django.get_version()
    assert hasattr(bootstrap3, "__version__")

    # One minimal functional call
    from bootstrap3.text import text_concat

    combined = text_concat("alpha", "beta", separator="-")
    assert combined == "alpha-beta"


if __name__ == "__main__":
    main()
