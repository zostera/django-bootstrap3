from django.test import TestCase


class VersionTest(TestCase):
    """Test presence of package version."""

    def test_version(self):
        import bootstrap3

        version = bootstrap3.__version__
        version_parts = version.split(".")
        self.assertTrue(len(version_parts) >= 2)
