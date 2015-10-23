from django.test import TestCase
from casexml.apps.case.tests import delete_all_cases
from corehq.apps.callcenter.utils import sync_call_center_user_case
from corehq.apps.domain.models import CallCenterProperties
from corehq.apps.domain.shortcuts import create_domain
from corehq.apps.hqcase.utils import get_case_by_domain_hq_user_id
from corehq.apps.locations.models import LocationType
from corehq.apps.locations.tests import make_loc
from corehq.apps.users.models import CommCareUser

TEST_DOMAIN = "cc-location-owner-test-domain"
CASE_TYPE = "cc-case-type"
LOCATION_TYPE = "my-location"


class CallCenterLocationOwnerTest(TestCase):

    @classmethod
    def get_call_center_config(cls):
        return CallCenterProperties(
            enabled=True,
            use_user_location_as_owner=True,
            case_owner_id=None,
            case_type=CASE_TYPE
        )

    @classmethod
    def setUpClass(cls):
        # Create domain
        cls.domain = create_domain(TEST_DOMAIN)
        cls.domain.call_center_config = cls.get_call_center_config()
        cls.domain.save()

        # Create user
        cls.user = CommCareUser.create(TEST_DOMAIN, 'user1', '***')

        # Create locations
        LocationType.objects.get_or_create(
            domain=cls.domain.name,
            name=LOCATION_TYPE,
        )
        cls.root_location = make_loc(
            'root_loc', type=LOCATION_TYPE, domain=TEST_DOMAIN
        )
        cls.child_location = make_loc(
            'child_loc', type=LOCATION_TYPE, domain=TEST_DOMAIN, parent=cls.root_location
        )
        cls.grandchild_location = make_loc(
            'grandchild_loc', type=LOCATION_TYPE, domain=TEST_DOMAIN, parent=cls.child_location
        )

    @classmethod
    def tearDownClass(cls):
        cls.domain.delete()

    def tearDown(self):
        delete_all_cases()

    def test_no_location_sync(self):
        self.user.unset_location()
        self.user.save()
        sync_call_center_user_case(self.user)
        self.assertCallCenterCaseOwner("")

    def test_location_sync(self):
        self.user.set_location(self.root_location)
        self.user.save()
        self.assertCallCenterCaseOwner(self.root_location._id)

    def test_location_change_sync(self):
        self.user.set_location(self.root_location)
        self.user.save()
        self.user.set_location(self.child_location)
        self.user.save()
        self.assertCallCenterCaseOwner(self.child_location._id)

    def assertCallCenterCaseOwner(self, owner_id):
        case = get_case_by_domain_hq_user_id(TEST_DOMAIN, self.user._id, CASE_TYPE)
        self.assertEqual(case.owner_id, owner_id)
