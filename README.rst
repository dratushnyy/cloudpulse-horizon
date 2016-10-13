OpenStack Dashboard plugin for CloudPulse - OpenStack Health Service

Installation prerequisites

1. Installed Horizon
2. Installed CloudPulse

To install plugin:
git clone https://github.com/dratushnyy/cloudpulse-horizon.git 
cd cloudpulse-horizon
cp -rv cloudpulse_horizon/enabled/ </path/to/horizon>/openstack_dashboard/local/enabled
horizon/tools/with_venv.sh python setup.py install

You can use https://github.com/dratushnyy/ansible-cloudpulse to deploy cloudpulse client, server and panel
