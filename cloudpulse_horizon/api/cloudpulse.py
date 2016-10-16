# Copyright 2016, Dmitry Ratushnyy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cloudpulseclient.v1 import client
from django.conf import settings


class CloudPulseTest(object):
    def __init__(self, name, scenario):
        self.name = name
        self.scenario = scenario


class CloudPulseTestResult(object):
    def __init__(self, id, uuid, name, testtype, state):
        self.id = id
        self.uuid = uuid
        self.name = name
        self.testtype = testtype
        self.state = state


class CloudPulseTestResultDetailed(CloudPulseTestResult):

    def __init__(self, id, uuid, name, testtype, state,
                 created_at, updated_at, result):
        super(CloudPulseTestResultDetailed, self).__init__(id, uuid, name,
                                                           testtype, state)

        self.created_at = created_at
        self.updated_at = updated_at
        self.result = result


def get_auth_params_from_request(request):
    return(
        request.user.username,
        request.user.project_name,
        request.user.token.id,
        request.user.tenant_id,
        getattr(settings, 'OPENSTACK_KEYSTONE_URL'),
        "health"
    )


def _cloudpulse_client(request):
    username, project_name, token_id, tenant_id, auth_url, service_type \
        = get_auth_params_from_request(request)
    return client.Client(username=username, project_id=tenant_id,
                         project_name=project_name, input_auth_token=token_id,
                         auth_url=auth_url, service_type=service_type)


def get_tests_list(request):
    resp, data = _cloudpulse_client(request).http_client \
        .json_request("GET", "/v1/cpulse/list_tests")
    test_list = []
    if resp.status == 200:
        for scenario in data:
            for test in data[scenario].split("\n"):
                test_list.append(CloudPulseTest(name=test, scenario=scenario))
    return test_list


def run_test(request, test):
    resp, data = _cloudpulse_client(request).http_client.\
        json_request('POST', "/v1/cpulse", body={"name": test})
    if resp.status == 201:
        return data


def get_tests_results(request):
    resp, data = _cloudpulse_client(request).http_client \
        .json_request("GET", "/cpulse")
    test_results = []
    if resp.status == 200:
        for result in data['cpulses']:
            test_results.append(CloudPulseTestResult(
                id=result['id'], uuid=result['uuid'], name=result['name'],
                testtype=result['testtype'], state=result['state']
            ))
    return test_results


def get_result_details(request, result_id):
    resp, data = _cloudpulse_client(request).http_client.\
        json_request("GET", "/v1/cpulse/%s" % result_id)
    if resp.status == 200:
        return data


def delete_test_result(request, result_id):
    try:
        resp, data = _cloudpulse_client(request).http_client.\
            json_request("DELETE", "/v1/cpulse/%s" % result_id)
        if resp.status == 204:
            return True, None
    except Exception, e:
        return False, e
