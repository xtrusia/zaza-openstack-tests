# Copyright 2026 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from unittest import mock

import zaza.openstack.charm_tests.manila_ganesha.setup as manila_setup


class TestManilaGaneshaSetup(unittest.TestCase):

    @mock.patch.object(
        manila_setup.openstack_utils, 'get_overcloud_keystone_session')
    @mock.patch.object(
        manila_setup.openstack_utils, 'get_manila_session_client')
    def test_setup_ganesha_share_type(
            self, get_manila_session_client, get_keystone_session):
        session = mock.MagicMock()
        get_keystone_session.return_value = session

        manila_setup.setup_ganesha_share_type()

        get_manila_session_client.assert_called_once_with(session)
        get_manila_session_client.return_value.share_types.create.\
            assert_called_once_with(
                name=manila_setup.MANILA_GANESHA_TYPE_NAME,
                spec_driver_handles_share_servers=False,
                extra_specs={
                    'vendor_name': 'Ceph',
                    'storage_protocol': 'NFS',
                    'snapshot_support': True,
                })
