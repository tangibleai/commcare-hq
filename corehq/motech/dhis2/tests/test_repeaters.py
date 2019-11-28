from distutils.version import LooseVersion

from django.test import SimpleTestCase, TestCase

from mock import Mock, patch

from corehq.motech.dhis2.const import DHIS2_MAX_VERSION
from corehq.motech.dhis2.repeaters import Dhis2Repeater


class ApiVersionTests(SimpleTestCase):

    def test_major_minor_patch(self):
        repeater = Dhis2Repeater.wrap({"dhis2_version": "2.31.6"})
        self.assertEqual(repeater.api_version, 31)

    def test_major_minor(self):
        repeater = Dhis2Repeater.wrap({"dhis2_version": "2.31"})
        self.assertEqual(repeater.api_version, 31)

    def test_major_raises_value_error(self):
        repeater = Dhis2Repeater.wrap({"dhis2_version": "2"})
        with self.assertRaises(ValueError):
            repeater.api_version

    def test_blank_raises_value_error(self):
        repeater = Dhis2Repeater.wrap({"dhis2_version": ""})
        with self.assertRaises(ValueError):
            repeater.api_version


class SlowApiVersionTest(TestCase):

    def setUp(self):
        self.repeater = Dhis2Repeater.wrap({
            "domain": "test-domain",
            "url": "https://dhis2.example.com/",
            "username": "admin",
            "password": "district",
        })

    def tearDown(self):
        self.repeater.delete()

    def test_none_fetches_metadata(self):
        self.assertIsNone(self.repeater.dhis2_version)
        with patch('corehq.motech.dhis2.repeaters.fetch_metadata') as mock_fetch:
            mock_fetch.return_value = {"system": {"version": "2.31.6"}}
            self.assertEqual(self.repeater.api_version, 31)
            mock_fetch.assert_called()

    def test_max_version_exceeded_notifies_admins(self):
        major_ver, max_api_ver, patch_ver = LooseVersion(DHIS2_MAX_VERSION).version
        bigly_api_version = max_api_ver + 1
        bigly_dhis2_version = f"{major_ver}.{bigly_api_version}.{patch_ver}"
        with patch('corehq.motech.dhis2.repeaters.fetch_metadata') as mock_fetch, \
                patch('corehq.motech.dhis2.repeaters.Requests') as MockRequests:
            mock_fetch.return_value = {"system": {"version": bigly_dhis2_version}}
            mock_requests = Mock()
            MockRequests.return_value = mock_requests

            self.assertEqual(self.repeater.api_version, bigly_api_version)
            mock_requests.notify_error.assert_called()
