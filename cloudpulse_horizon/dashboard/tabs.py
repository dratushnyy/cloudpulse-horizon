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

from django.utils.translation import ugettext_lazy as _
from horizon import tabs
from cloudpulse_horizon.api import cloudpulse
from .tables import TestResultsTable, TestsTable


class TestResultsTab(tabs.TableTab):
    name = _("Test results")
    slug = "results"
    table_classes = (TestResultsTable,)
    template_name = "horizon/common/_detail_table.html"

    def get_test_results_data(self):
        return cloudpulse.get_tests_results(self.request)


class TestsTab(tabs.TableTab):
    name = _("Tests")
    slug = "tests"
    table_classes = (TestsTable,)
    template_name = "horizon/common/_detail_table.html"
    preload = False

    def get_tests_data(self):
        return cloudpulse.get_tests_list(self.request)


class CloudpulseTabs(tabs.TabGroup):
    slug = "cloudpulse_tabs"
    tabs = (TestResultsTab, TestsTab, )
    sticky = True
