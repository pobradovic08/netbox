from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from dcim.choices import *
from dcim.constants import *
from dcim.models import *
from extras.forms import LocalConfigContextFilterForm
from extras.models import ConfigTemplate
from ipam.models import ASN, L2VPN, VRF
from netbox.forms import NetBoxModelFilterSetForm
from tenancy.forms import ContactModelFilterForm, TenancyFilterForm
from utilities.forms import BOOLEAN_WITH_BLANK_CHOICES, FilterForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.widgets import APISelectMultiple, NumberWithOptions
from wireless.choices import *

__all__ = (
    'CableFilterForm',
    'ConsoleConnectionFilterForm',
    'ConsolePortFilterForm',
    'ConsoleServerPortFilterForm',
    'DeviceBayFilterForm',
    'DeviceFilterForm',
    'DeviceRoleFilterForm',
    'DeviceTypeFilterForm',
    'FrontPortFilterForm',
    'InterfaceConnectionFilterForm',
    'InterfaceFilterForm',
    'InventoryItemFilterForm',
    'InventoryItemRoleFilterForm',
    'LocationFilterForm',
    'ManufacturerFilterForm',
    'ModuleFilterForm',
    'ModuleFilterForm',
    'ModuleBayFilterForm',
    'ModuleTypeFilterForm',
    'PlatformFilterForm',
    'PowerConnectionFilterForm',
    'PowerFeedFilterForm',
    'PowerOutletFilterForm',
    'PowerPanelFilterForm',
    'PowerPortFilterForm',
    'RackFilterForm',
    'RackElevationFilterForm',
    'RackReservationFilterForm',
    'RackRoleFilterForm',
    'RearPortFilterForm',
    'RegionFilterForm',
    'SiteFilterForm',
    'SiteGroupFilterForm',
    'VirtualChassisFilterForm',
    'VirtualDeviceContextFilterForm'
)


class DeviceComponentFilterForm(NetBoxModelFilterSetForm):
    name = forms.CharField(
        label=_('Name'),
        required=False
    )
    label = forms.CharField(
        label=_('Label'),
        required=False
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
        },
        label=_('Location')
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        label=_('Rack')
    )
    virtual_chassis_id = DynamicModelMultipleChoiceField(
        queryset=VirtualChassis.objects.all(),
        required=False,
        label=_('Virtual Chassis')
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label=_('Device type')
    )
    device_role_id = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        label=_('Device role')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
            'virtual_chassis_id': '$virtual_chassis_id',
            'device_type_id': '$device_type_id',
            'role_id': '$role_id'
        },
        label=_('Device')
    )


class RegionFilterForm(ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = Region
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'parent_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group'))
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Parent region')
    )
    tag = TagFilterField(model)


class SiteGroupFilterForm(ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = SiteGroup
    fieldsets = (
        (None, ('q', 'filter_id', 'tag', 'parent_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group'))
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Parent group')
    )
    tag = TagFilterField(model)


class SiteFilterForm(TenancyFilterForm, ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = Site
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('status', 'region_id', 'group_id', 'asn_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=SiteStatusChoices,
        required=False
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    asn_id = DynamicModelMultipleChoiceField(
        queryset=ASN.objects.all(),
        required=False,
        label=_('ASNs')
    )
    tag = TagFilterField(model)


class LocationFilterForm(TenancyFilterForm, ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = Location
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('region_id', 'site_group_id', 'site_id', 'parent_id', 'status')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    parent_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'site_id': '$site_id',
        },
        label=_('Parent')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=LocationStatusChoices,
        required=False
    )
    tag = TagFilterField(model)


class RackRoleFilterForm(NetBoxModelFilterSetForm):
    model = RackRole
    tag = TagFilterField(model)


class RackFilterForm(TenancyFilterForm, ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = Rack
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id')),
        (_('Function'), ('status', 'role_id')),
        (_('Hardware'), ('type', 'width', 'serial', 'asset_tag')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
        (_('Weight'), ('weight', 'max_weight', 'weight_unit')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('Location')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=RackStatusChoices,
        required=False
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=RackTypeChoices,
        required=False
    )
    width = forms.MultipleChoiceField(
        label=_('Width'),
        choices=RackWidthChoices,
        required=False
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        null_option='None',
        label=_('Role')
    )
    serial = forms.CharField(
        label=_('Serial'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('Asset tag'),
        required=False
    )
    tag = TagFilterField(model)
    weight = forms.DecimalField(
        label=_('Weight'),
        required=False,
        min_value=1
    )
    max_weight = forms.IntegerField(
        label=_('Max weight'),
        required=False,
        min_value=1
    )
    weight_unit = forms.ChoiceField(
        label=_('Weight unit'),
        choices=add_blank_choice(WeightUnitChoices),
        required=False
    )


class RackElevationFilterForm(RackFilterForm):
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'id')),
        (_('Function'), ('status', 'role_id')),
        (_('Hardware'), ('type', 'width', 'serial', 'asset_tag')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
        (_('Weight'), ('weight', 'max_weight', 'weight_unit')),
    )
    id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        label=_('Rack'),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        }
    )


class RackReservationFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = RackReservation
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('User'), ('user_id',)),
        (_('Rack'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
        },
        label=_('Location'),
        null_option='None'
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        label=_('Rack')
    )
    user_id = DynamicModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_('User'),
        widget=APISelectMultiple(
            api_url='/api/users/users/',
        )
    )
    tag = TagFilterField(model)


class ManufacturerFilterForm(ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = Manufacturer
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group'))
    )
    tag = TagFilterField(model)


class DeviceTypeFilterForm(NetBoxModelFilterSetForm):
    model = DeviceType
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Hardware'), ('manufacturer_id', 'default_platform_id', 'part_number', 'subdevice_role', 'airflow')),
        (_('Images'), ('has_front_image', 'has_rear_image')),
        (_('Components'), (
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces',
            'pass_through_ports', 'device_bays', 'module_bays', 'inventory_items',
        )),
        (_('Weight'), ('weight', 'weight_unit')),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    default_platform_id = DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        label=_('Default platform')
    )
    part_number = forms.CharField(
        label=_('Part number'),
        required=False
    )
    subdevice_role = forms.MultipleChoiceField(
        label=_('Subdevice role'),
        choices=add_blank_choice(SubdeviceRoleChoices),
        required=False
    )
    airflow = forms.MultipleChoiceField(
        label=_('Airflow'),
        choices=add_blank_choice(DeviceAirflowChoices),
        required=False
    )
    has_front_image = forms.NullBooleanField(
        required=False,
        label=_('Has a front image'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    has_rear_image = forms.NullBooleanField(
        required=False,
        label=_('Has a rear image'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_server_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console server ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_ports = forms.NullBooleanField(
        required=False,
        label=_('Has power ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_outlets = forms.NullBooleanField(
        required=False,
        label=_('Has power outlets'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    interfaces = forms.NullBooleanField(
        required=False,
        label=_('Has interfaces'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    pass_through_ports = forms.NullBooleanField(
        required=False,
        label=_('Has pass-through ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    device_bays = forms.NullBooleanField(
        required=False,
        label=_('Has device bays'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    module_bays = forms.NullBooleanField(
        required=False,
        label=_('Has module bays'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    inventory_items = forms.NullBooleanField(
        required=False,
        label=_('Has inventory items'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)
    weight = forms.DecimalField(
        label=_('Weight'),
        required=False
    )
    weight_unit = forms.ChoiceField(
        label=_('Weight unit'),
        choices=add_blank_choice(WeightUnitChoices),
        required=False
    )


class ModuleTypeFilterForm(NetBoxModelFilterSetForm):
    model = ModuleType
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Hardware'), ('manufacturer_id', 'part_number')),
        (_('Components'), (
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces',
            'pass_through_ports',
        )),
        (_('Weight'), ('weight', 'weight_unit')),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer'),
        fetch_trigger='open'
    )
    part_number = forms.CharField(
        label=_('Part number'),
        required=False
    )
    console_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_server_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console server ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_ports = forms.NullBooleanField(
        required=False,
        label=_('Has power ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_outlets = forms.NullBooleanField(
        required=False,
        label=_('Has power outlets'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    interfaces = forms.NullBooleanField(
        required=False,
        label=_('Has interfaces'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    pass_through_ports = forms.NullBooleanField(
        required=False,
        label=_('Has pass-through ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)
    weight = forms.DecimalField(
        label=_('Weight'),
        required=False
    )
    weight_unit = forms.ChoiceField(
        label=_('Weight unit'),
        choices=add_blank_choice(WeightUnitChoices),
        required=False
    )


class DeviceRoleFilterForm(NetBoxModelFilterSetForm):
    model = DeviceRole
    config_template_id = DynamicModelMultipleChoiceField(
        queryset=ConfigTemplate.objects.all(),
        required=False,
        label=_('Config template')
    )
    tag = TagFilterField(model)


class PlatformFilterForm(NetBoxModelFilterSetForm):
    model = Platform
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    config_template_id = DynamicModelMultipleChoiceField(
        queryset=ConfigTemplate.objects.all(),
        required=False,
        label=_('Config template')
    )
    tag = TagFilterField(model)


class DeviceFilterForm(
    LocalConfigContextFilterForm,
    TenancyFilterForm,
    ContactModelFilterForm,
    NetBoxModelFilterSetForm
):
    model = Device
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Operation'), ('status', 'role_id', 'airflow', 'serial', 'asset_tag', 'mac_address')),
        (_('Hardware'), ('manufacturer_id', 'device_type_id', 'platform_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
        (_('Components'), (
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces', 'pass_through_ports',
        )),
        (_('Miscellaneous'), (
            'has_primary_ip', 'has_oob_ip', 'virtual_chassis_member', 'config_template_id', 'local_context_data',
        ))
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('Location')
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        },
        label=_('Rack')
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        label=_('Role')
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    device_type_id = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Model')
    )
    platform_id = DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        null_option='None',
        label=_('Platform')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=DeviceStatusChoices,
        required=False
    )
    airflow = forms.MultipleChoiceField(
        label=_('Airflow'),
        choices=add_blank_choice(DeviceAirflowChoices),
        required=False
    )
    serial = forms.CharField(
        label=_('Serial'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('Asset tag'),
        required=False
    )
    mac_address = forms.CharField(
        required=False,
        label=_('MAC address')
    )
    config_template_id = DynamicModelMultipleChoiceField(
        queryset=ConfigTemplate.objects.all(),
        required=False,
        label=_('Config template')
    )
    has_primary_ip = forms.NullBooleanField(
        required=False,
        label=_('Has a primary IP'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    has_oob_ip = forms.NullBooleanField(
        required=False,
        label='Has an OOB IP',
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    virtual_chassis_member = forms.NullBooleanField(
        required=False,
        label=_('Virtual chassis member'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    console_server_ports = forms.NullBooleanField(
        required=False,
        label=_('Has console server ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_ports = forms.NullBooleanField(
        required=False,
        label=_('Has power ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    power_outlets = forms.NullBooleanField(
        required=False,
        label=_('Has power outlets'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    interfaces = forms.NullBooleanField(
        required=False,
        label=_('Has interfaces'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    pass_through_ports = forms.NullBooleanField(
        required=False,
        label=_('Has pass-through ports'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)


class VirtualDeviceContextFilterForm(
    TenancyFilterForm,
    NetBoxModelFilterSetForm
):
    model = VirtualDeviceContext
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('device', 'status', 'has_primary_ip')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
    )
    device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        label=_('Device'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        required=False,
        choices=add_blank_choice(VirtualDeviceContextStatusChoices)
    )
    has_primary_ip = forms.NullBooleanField(
        required=False,
        label=_('Has a primary IP'),
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)


class ModuleFilterForm(LocalConfigContextFilterForm, TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Module
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Hardware'), ('manufacturer_id', 'module_type_id', 'status', 'serial', 'asset_tag')),
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer'),
        fetch_trigger='open'
    )
    module_type_id = DynamicModelMultipleChoiceField(
        queryset=ModuleType.objects.all(),
        required=False,
        query_params={
            'manufacturer_id': '$manufacturer_id'
        },
        label=_('Type'),
        fetch_trigger='open'
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=ModuleStatusChoices,
        required=False
    )
    serial = forms.CharField(
        label=_('Serial'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('Asset tag'),
        required=False
    )
    tag = TagFilterField(model)


class VirtualChassisFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = VirtualChassis
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    tag = TagFilterField(model)


class CableFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Cable
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('site_id', 'location_id', 'rack_id', 'device_id')),
        (_('Attributes'), ('type', 'status', 'color', 'length', 'length_unit')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_('Location'),
        null_option='None',
        query_params={
            'site_id': '$site_id'
        }
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label=_('Rack'),
        null_option='None',
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
        }
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id',
            'location_id': '$location_id',
            'rack_id': '$rack_id',
            'tenant_id': '$tenant_id',
        },
        label=_('Device')
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=add_blank_choice(CableTypeChoices),
        required=False
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        required=False,
        choices=add_blank_choice(LinkStatusChoices)
    )
    color = ColorField(
        label=_('Color'),
        required=False
    )
    length = forms.IntegerField(
        label=_('Length'),
        required=False
    )
    length_unit = forms.ChoiceField(
        label=_('Length unit'),
        choices=add_blank_choice(CableLengthUnitChoices),
        required=False
    )
    tag = TagFilterField(model)


class PowerPanelFilterForm(ContactModelFilterForm, NetBoxModelFilterSetForm):
    model = PowerPanel
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id')),
        (_('Contacts'), ('contact', 'contact_role', 'contact_group')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id',
            'group_id': '$site_group_id',
        },
        label=_('Site')
    )
    location_id = DynamicModelMultipleChoiceField(
        queryset=Location.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('Location')
    )
    tag = TagFilterField(model)


class PowerFeedFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = PowerFeed
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'power_panel_id', 'rack_id')),
        (_('Tenant'), ('tenant_group_id', 'tenant_id')),
        (_('Attributes'), ('status', 'type', 'supply', 'phase', 'voltage', 'amperage', 'max_utilization')),
    )
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_group_id = DynamicModelMultipleChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label=_('Site group')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    power_panel_id = DynamicModelMultipleChoiceField(
        queryset=PowerPanel.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('Power panel')
    )
    rack_id = DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        null_option='None',
        query_params={
            'site_id': '$site_id'
        },
        label=_('Rack')
    )
    status = forms.MultipleChoiceField(
        label=_('Status'),
        choices=PowerFeedStatusChoices,
        required=False
    )
    type = forms.ChoiceField(
        label=_('Type'),
        choices=add_blank_choice(PowerFeedTypeChoices),
        required=False
    )
    supply = forms.ChoiceField(
        label=_('Supply'),
        choices=add_blank_choice(PowerFeedSupplyChoices),
        required=False
    )
    phase = forms.ChoiceField(
        label=_('Phase'),
        choices=add_blank_choice(PowerFeedPhaseChoices),
        required=False
    )
    voltage = forms.IntegerField(
        label=_('Voltage'),
        required=False
    )
    amperage = forms.IntegerField(
        label=_('Amperage'),
        required=False
    )
    max_utilization = forms.IntegerField(
        label=_('Max utilization'),
        required=False
    )
    tag = TagFilterField(model)


#
# Device components
#

class CabledFilterForm(forms.Form):
    cabled = forms.NullBooleanField(
        label=_('Cabled'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    occupied = forms.NullBooleanField(
        label=_('Occupied'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )


class PathEndpointFilterForm(CabledFilterForm):
    connected = forms.NullBooleanField(
        label=_('Connected'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )


class ConsolePortFilterForm(PathEndpointFilterForm, DeviceComponentFilterForm):
    model = ConsolePort
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type', 'speed')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Connection'), ('cabled', 'connected', 'occupied')),
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=ConsolePortTypeChoices,
        required=False
    )
    speed = forms.MultipleChoiceField(
        label=_('Speed'),
        choices=ConsolePortSpeedChoices,
        required=False
    )
    tag = TagFilterField(model)


class ConsoleServerPortFilterForm(PathEndpointFilterForm, DeviceComponentFilterForm):
    model = ConsoleServerPort
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type', 'speed')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Connection'), ('cabled', 'connected', 'occupied')),
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=ConsolePortTypeChoices,
        required=False
    )
    speed = forms.MultipleChoiceField(
        label=_('Speed'),
        choices=ConsolePortSpeedChoices,
        required=False
    )
    tag = TagFilterField(model)


class PowerPortFilterForm(PathEndpointFilterForm, DeviceComponentFilterForm):
    model = PowerPort
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Connection'), ('cabled', 'connected', 'occupied')),
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=PowerPortTypeChoices,
        required=False
    )
    tag = TagFilterField(model)


class PowerOutletFilterForm(PathEndpointFilterForm, DeviceComponentFilterForm):
    model = PowerOutlet
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Connection'), ('cabled', 'connected', 'occupied')),
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=PowerOutletTypeChoices,
        required=False
    )
    tag = TagFilterField(model)


class InterfaceFilterForm(PathEndpointFilterForm, DeviceComponentFilterForm):
    model = Interface
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'kind', 'type', 'speed', 'duplex', 'enabled', 'mgmt_only')),
        (_('Addressing'), ('vrf_id', 'l2vpn_id', 'mac_address', 'wwn')),
        (_('PoE'), ('poe_mode', 'poe_type')),
        (_('Wireless'), ('rf_role', 'rf_channel', 'rf_channel_width', 'tx_power')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id', 'vdc_id')),
        (_('Connection'), ('cabled', 'connected', 'occupied')),
    )
    vdc_id = DynamicModelMultipleChoiceField(
        queryset=VirtualDeviceContext.objects.all(),
        required=False,
        query_params={
            'device_id': '$device_id',
        },
        label=_('Virtual Device Context')
    )
    kind = forms.MultipleChoiceField(
        label=_('Kind'),
        choices=InterfaceKindChoices,
        required=False
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=InterfaceTypeChoices,
        required=False
    )
    speed = forms.IntegerField(
        label=_('Speed'),
        required=False,
        widget=NumberWithOptions(
            options=InterfaceSpeedChoices
        )
    )
    duplex = forms.MultipleChoiceField(
        label=_('Duplex'),
        choices=InterfaceDuplexChoices,
        required=False
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    mgmt_only = forms.NullBooleanField(
        label=_('Mgmt only'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    mac_address = forms.CharField(
        required=False,
        label=_('MAC address')
    )
    wwn = forms.CharField(
        required=False,
        label=_('WWN')
    )
    poe_mode = forms.MultipleChoiceField(
        choices=InterfacePoEModeChoices,
        required=False,
        label=_('PoE mode')
    )
    poe_type = forms.MultipleChoiceField(
        choices=InterfacePoETypeChoices,
        required=False,
        label=_('PoE type')
    )
    rf_role = forms.MultipleChoiceField(
        choices=WirelessRoleChoices,
        required=False,
        label=_('Wireless role')
    )
    rf_channel = forms.MultipleChoiceField(
        choices=WirelessChannelChoices,
        required=False,
        label=_('Wireless channel')
    )
    rf_channel_frequency = forms.IntegerField(
        required=False,
        label=_('Channel frequency (MHz)')
    )
    rf_channel_width = forms.IntegerField(
        required=False,
        label=_('Channel width (MHz)')
    )
    tx_power = forms.IntegerField(
        required=False,
        label=_('Transmit power (dBm)'),
        min_value=0,
        max_value=127
    )
    vrf_id = DynamicModelMultipleChoiceField(
        queryset=VRF.objects.all(),
        required=False,
        label=_('VRF')
    )
    l2vpn_id = DynamicModelMultipleChoiceField(
        queryset=L2VPN.objects.all(),
        required=False,
        label=_('L2VPN')
    )
    tag = TagFilterField(model)


class FrontPortFilterForm(CabledFilterForm, DeviceComponentFilterForm):
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type', 'color')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Cable'), ('cabled', 'occupied')),
    )
    model = FrontPort
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=PortTypeChoices,
        required=False
    )
    color = ColorField(
        label=_('Color'),
        required=False
    )
    tag = TagFilterField(model)


class RearPortFilterForm(CabledFilterForm, DeviceComponentFilterForm):
    model = RearPort
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'type', 'color')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
        (_('Cable'), ('cabled', 'occupied')),
    )
    type = forms.MultipleChoiceField(
        label=_('Type'),
        choices=PortTypeChoices,
        required=False
    )
    color = ColorField(
        label=_('Color'),
        required=False
    )
    tag = TagFilterField(model)


class ModuleBayFilterForm(DeviceComponentFilterForm):
    model = ModuleBay
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'position')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
    )
    tag = TagFilterField(model)
    position = forms.CharField(
        label=_('Position'),
        required=False
    )


class DeviceBayFilterForm(DeviceComponentFilterForm):
    model = DeviceBay
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
    )
    tag = TagFilterField(model)


class InventoryItemFilterForm(DeviceComponentFilterForm):
    model = InventoryItem
    fieldsets = (
        (None, ('q', 'filter_id', 'tag')),
        (_('Attributes'), ('name', 'label', 'role_id', 'manufacturer_id', 'serial', 'asset_tag', 'discovered')),
        (_('Location'), ('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_id')),
        (_('Device'), ('device_type_id', 'device_role_id', 'device_id', 'virtual_chassis_id')),
    )
    role_id = DynamicModelMultipleChoiceField(
        queryset=InventoryItemRole.objects.all(),
        required=False,
        label=_('Role'),
        fetch_trigger='open'
    )
    manufacturer_id = DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label=_('Manufacturer')
    )
    serial = forms.CharField(
        label=_('Serial'),
        required=False
    )
    asset_tag = forms.CharField(
        label=_('Asset tag'),
        required=False
    )
    discovered = forms.NullBooleanField(
        label=_('Discovered'),
        required=False,
        widget=forms.Select(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        )
    )
    tag = TagFilterField(model)


#
# Device component roles
#

class InventoryItemRoleFilterForm(NetBoxModelFilterSetForm):
    model = InventoryItemRole
    tag = TagFilterField(model)


#
# Connections
#

class ConsoleConnectionFilterForm(FilterForm):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('Device')
    )


class PowerConnectionFilterForm(FilterForm):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('Device')
    )


class InterfaceConnectionFilterForm(FilterForm):
    region_id = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_('Region')
    )
    site_id = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={
            'region_id': '$region_id'
        },
        label=_('Site')
    )
    device_id = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        query_params={
            'site_id': '$site_id'
        },
        label=_('Device')
    )
