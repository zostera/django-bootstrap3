from django.test import TestCase


class UtilsTest(TestCase):
    """Test the Font Awesome Renderer."""

    def test_version(self):
        import bootstrap3

        version = bootstrap3.__version__
        version_parts = version.split(".")
        self.assertTrue(len(version_parts) >= 3)
