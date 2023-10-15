from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dcim.forms.common import InterfaceCommonForm
from dcim.models import Device, DeviceRole, Platform, Rack, Region, Site, SiteGroup
from extras.models import ConfigTemplate
from ipam.models import IPAddress, VLAN, VLANGroup, VRF
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from utilities.forms import BootstrapMixin, ConfirmationForm
from utilities.forms.fields import (
    CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, JSONField, SlugField,
)
from utilities.forms.widgets import HTMXSelect
from virtualization.models import *

__all__ = (
    'ClusterAddDevicesForm',
    'ClusterForm',
    'ClusterGroupForm',
    'ClusterRemoveDevicesForm',
    'ClusterTypeForm',
    'VirtualMachineForm',
    'VMInterfaceForm',
)


class ClusterTypeForm(NetBoxModelForm):
    slug = SlugField()

    fieldsets = (
        (_('Cluster Type'), (
            'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = ClusterType
        fields = (
            'name', 'slug', 'description', 'tags',
        )


class ClusterGroupForm(NetBoxModelForm):
    slug = SlugField()

    fieldsets = (
        (_('Cluster Group'), (
            'name', 'slug', 'description', 'tags',
        )),
    )

    class Meta:
        model = ClusterGroup
        fields = (
            'name', 'slug', 'description', 'tags',
        )


class ClusterForm(TenancyForm, NetBoxModelForm):
    type = DynamicModelChoiceField(
        label=_('Type'),
        queryset=ClusterType.objects.all()
    )
    group = DynamicModelChoiceField(
        label=_('Group'),
        queryset=ClusterGroup.objects.all(),
        required=False
    )
    site = DynamicModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all(),
        required=False,
        selector=True
    )
    comments = CommentField()

    fieldsets = (
        (_('Cluster'), ('name', 'type', 'group', 'site', 'status', 'description', 'tags')),
        (_('Tenancy'), ('tenant_group', 'tenant')),
    )

    class Meta:
        model = Cluster
        fields = (
            'name', 'type', 'group', 'status', 'tenant', 'site', 'description', 'comments', 'tags',
        )


class ClusterAddDevicesForm(BootstrapMixin, forms.Form):
    region = DynamicModelChoiceField(
        label=_('Region'),
        queryset=Region.objects.all(),
        required=False,
        null_option='None'
    )
    site_group = DynamicModelChoiceField(
        label=_('Site group'),
        queryset=SiteGroup.objects.all(),
        required=False,
        null_option='None'
    )
    site = DynamicModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region',
            'group_id': '$site_group',
        }
    )
    rack = DynamicModelChoiceField(
        label=_('Rack'),
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site'
        }
    )
    devices = DynamicModelMultipleChoiceField(
        label=_('Devices'),
        queryset=Device.objects.all(),
        query_params={
            'site_id': '$site',
            'rack_id': '$rack',
            'cluster_id': 'null',
        }
    )

    class Meta:
        fields = [
            'region', 'site', 'rack', 'devices',
        ]

    def __init__(self, cluster, *args, **kwargs):

        self.cluster = cluster

        super().__init__(*args, **kwargs)

        self.fields['devices'].choices = []

    def clean(self):
        super().clean()

        # If the Cluster is assigned to a Site, all Devices must be assigned to that Site.
        if self.cluster.site is not None:
            for device in self.cleaned_data.get('devices', []):
                if device.site != self.cluster.site:
                    raise ValidationError({
                        'devices': _("{} belongs to a different site ({}) than the cluster ({})").format(
                            device, device.site, self.cluster.site
                        )
                    })


class ClusterRemoveDevicesForm(ConfirmationForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Device.objects.all(),
        widget=forms.MultipleHiddenInput()
    )


class VirtualMachineForm(TenancyForm, NetBoxModelForm):
    site = DynamicModelChoiceField(
        label=_('Site'),
        queryset=Site.objects.all(),
        required=False
    )
    cluster = DynamicModelChoiceField(
        label=_('Cluster'),
        queryset=Cluster.objects.all(),
        required=False,
        selector=True,
        query_params={
            'site_id': '$site',
        }
    )
    device = DynamicModelChoiceField(
        label=_('Device'),
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'cluster_id': '$cluster',
            'site_id': '$site',
        },
        help_text=_("Optionally pin this VM to a specific host device within the cluster")
    )
    role = DynamicModelChoiceField(
        label=_('Role'),
        queryset=DeviceRole.objects.all(),
        required=False,
        query_params={
            "vm_role": "True"
        }
    )
    platform = DynamicModelChoiceField(
        label=_('Platform'),
        queryset=Platform.objects.all(),
        required=False
    )
    local_context_data = JSONField(
        required=False,
        label=''
    )
    config_template = DynamicModelChoiceField(
        queryset=ConfigTemplate.objects.all(),
        required=False,
        label=_('Config template')
    )
    comments = CommentField()

    fieldsets = (
        (_('Virtual Machine'), ('name', 'role', 'status', 'description', 'tags')),
        (_('Site/Cluster'), ('site', 'cluster', 'device')),
        (_('Tenancy'), ('tenant_group', 'tenant')),
        (_('Management'), ('platform', 'primary_ip4', 'primary_ip6', 'config_template')),
        (_('Resources'), ('vcpus', 'memory', 'disk')),
        (_('Config Context'), ('local_context_data',)),
    )

    class Meta:
        model = VirtualMachine
        fields = [
            'name', 'status', 'site', 'cluster', 'device', 'role', 'tenant_group', 'tenant', 'platform', 'primary_ip4',
            'primary_ip6', 'vcpus', 'memory', 'disk', 'description', 'comments', 'tags', 'local_context_data',
            'config_template',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:

            # Compile list of choices for primary IPv4 and IPv6 addresses
            for family in [4, 6]:
                ip_choices = [(None, '---------')]

                # Gather PKs of all interfaces belonging to this VM
                interface_ids = self.instance.interfaces.values_list('pk', flat=True)

                # Collect interface IPs
                interface_ips = IPAddress.objects.filter(
                    address__family=family,
                    assigned_object_type=ContentType.objects.get_for_model(VMInterface),
                    assigned_object_id__in=interface_ids
                )
                if interface_ips:
                    ip_list = [(ip.id, f'{ip.address} ({ip.assigned_object})') for ip in interface_ips]
                    ip_choices.append(('Interface IPs', ip_list))
                # Collect NAT IPs
                nat_ips = IPAddress.objects.prefetch_related('nat_inside').filter(
                    address__family=family,
                    nat_inside__assigned_object_type=ContentType.objects.get_for_model(VMInterface),
                    nat_inside__assigned_object_id__in=interface_ids
                )
                if nat_ips:
                    ip_list = [(ip.id, f'{ip.address} (NAT)') for ip in nat_ips]
                    ip_choices.append(('NAT IPs', ip_list))
                self.fields['primary_ip{}'.format(family)].choices = ip_choices

        else:

            # An object that doesn't exist yet can't have any IPs assigned to it
            self.fields['primary_ip4'].choices = []
            self.fields['primary_ip4'].widget.attrs['readonly'] = True
            self.fields['primary_ip6'].choices = []
            self.fields['primary_ip6'].widget.attrs['readonly'] = True


class VMInterfaceForm(InterfaceCommonForm, NetBoxModelForm):
    virtual_machine = DynamicModelChoiceField(
        label=_('Virtual machine'),
        queryset=VirtualMachine.objects.all(),
        selector=True
    )
    parent = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        label=_('Parent interface'),
        query_params={
            'virtual_machine_id': '$virtual_machine',
        }
    )
    bridge = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        label=_('Bridged interface'),
        query_params={
            'virtual_machine_id': '$virtual_machine',
        }
    )
    vlan_group = DynamicModelChoiceField(
        queryset=VLANGroup.objects.all(),
        required=False,
        label=_('VLAN group')
    )
    untagged_vlan = DynamicModelChoiceField(
        queryset=VLAN.objects.all(),
        required=False,
        label=_('Untagged VLAN'),
        query_params={
            'group_id': '$vlan_group',
            'available_on_virtualmachine': '$virtual_machine',
        }
    )
    tagged_vlans = DynamicModelMultipleChoiceField(
        queryset=VLAN.objects.all(),
        required=False,
        label=_('Tagged VLANs'),
        query_params={
            'group_id': '$vlan_group',
            'available_on_virtualmachine': '$virtual_machine',
        }
    )
    vrf = DynamicModelChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=_('VRF')
    )

    fieldsets = (
        (_('Interface'), ('virtual_machine', 'name', 'description', 'tags')),
        (_('Addressing'), ('vrf', 'mac_address')),
        (_('Operation'), ('mtu', 'enabled')),
        (_('Related Interfaces'), ('parent', 'bridge')),
        (_('802.1Q Switching'), ('mode', 'vlan_group', 'untagged_vlan', 'tagged_vlans')),
    )

    class Meta:
        model = VMInterface
        fields = [
            'virtual_machine', 'name', 'parent', 'bridge', 'enabled', 'mac_address', 'mtu', 'description', 'mode',
            'vlan_group', 'untagged_vlan', 'tagged_vlans', 'vrf', 'tags',
        ]
        labels = {
            'mode': '802.1Q Mode',
        }
        widgets = {
            'mode': HTMXSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable reassignment of VirtualMachine when editing an existing instance
        if self.instance.pk:
            self.fields['virtual_machine'].disabled = True
