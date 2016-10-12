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

from horizon import tabs
from horizon import views

from cloudpulse_horizon.api import cloudpulse
from .tabs import CloudpulseTabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = CloudpulseTabs
    template_name = 'cloudpulse/index.html'


class TestResultDetailsView(views.HorizonTemplateView):
    template_name = 'cloudpulse/test_details.html'
    page_title = "{{ result.name }} test"

    def get_context_data(self, **kwargs):
        context = super(TestResultDetailsView, self).get_context_data(**kwargs)
        context["result"] = self.get_data()
        return context

    def get_data(self):
        return cloudpulse.get_result_details(
            self.request, self.kwargs["result_uuid"])
