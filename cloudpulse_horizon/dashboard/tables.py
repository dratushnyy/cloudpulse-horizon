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

from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from horizon import messages
from horizon import tables
from cloudpulse_horizon.api import cloudpulse


class DeleteResultAction(tables.DeleteAction):
    verbose_name = _("Delete result")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete test result",
            u"Delete test results",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted test result",
            u"Deleted test results",
            count
        )

    def delete(self, request, object_id):
        cloudpulse.delete_test_result(request, object_id)


class TestResultsTable(tables.DataTable):
    STATE_CHOICES = (
        ("success", True),
        ("scheduled", None),
        ("failed", False)
    )
    id = tables.Column('id', verbose_name=_("ID"),
                       link="horizon:admin:cloudpulse:result_details")
    uuid = tables.Column('uuid', hidden=True)
    name = tables.Column('name', verbose_name=_("Name"),
                         link="horizon:admin:cloudpulse:result_details")
    type = tables.Column('testtype', verbose_name=_("Test type"),
                         link="horizon:admin:cloudpulse:result_details")
    state = tables.Column('state', verbose_name=_("State"),
                          status=True, status_choices=STATE_CHOICES,
                          link="horizon:admin:cloudpulse:result_details")

    class Meta:
        name = "test_results"
        verbose_name = _("Test results")
        status_columns = ("state", )
        # TODO (dratushnyy) update rows like in instances
        # TODO (dratushnyy) batch delete rows
        row_actions = (DeleteResultAction, )

    def get_row_status_class(self, status):
        if status is True:
            return "success"
        elif status is False:
            return "danger"
        else:
            return "warning"

    def get_object_id(self, datum):
        return datum.uuid


class TestResultDetailedTable(TestResultsTable):
    created_at = tables.Column('created_at', verbose_name=_("Created"))
    updated_at = tables.Column('updated_at', verbose_name=_("Updated"))
    result = tables.Column('result', verbose_name=_("Result"))


class RunTestAction(tables.Action):
    name = "runtest"
    verbose_name = _("Run test")

    def single(self, data_table, request, object_id):
        result = cloudpulse.run_test(request, object_id)
        if result:
            message = _('Test %s scheduled with ID %s' % (result['name'],
                                                          result['id']))
            messages.success(request, message)
        else:
            messages.error(request, _("Failed to schedule test %s"
                                      % object_id))


class TestsTable(tables.DataTable):
    scenario = tables.Column('scenario', verbose_name=_("Scenario"))
    name = tables.Column('name', verbose_name=_("Name"))

    class Meta:
        name = "tests"
        verbose_name = _("Tests")
        row_actions = (RunTestAction,)

    def get_object_id(self, datum):
        return datum.name
