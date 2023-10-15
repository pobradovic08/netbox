from django import forms
from django.utils.translation import gettext_lazy as _

from extras.choices import *
from extras.models import *
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import BulkEditForm, add_blank_choice
from utilities.forms.fields import ColorField, DynamicModelChoiceField
from utilities.forms.widgets import BulkEditNullBooleanSelect

__all__ = (
    'ConfigContextBulkEditForm',
    'ConfigTemplateBulkEditForm',
    'CustomFieldBulkEditForm',
    'CustomFieldChoiceSetBulkEditForm',
    'CustomLinkBulkEditForm',
    'ExportTemplateBulkEditForm',
    'JournalEntryBulkEditForm',
    'SavedFilterBulkEditForm',
    'TagBulkEditForm',
    'WebhookBulkEditForm',
)


class CustomFieldBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=CustomField.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    group_name = forms.CharField(
        label=_('Group name'),
        required=False
    )
    description = forms.CharField(
        label=_('Description'),
        required=False
    )
    required = forms.NullBooleanField(
        label=_('Required'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    weight = forms.IntegerField(
        label=_('Weight'),
        required=False
    )
    choice_set = DynamicModelChoiceField(
        queryset=CustomFieldChoiceSet.objects.all(),
        required=False
    )
    ui_visibility = forms.ChoiceField(
        label=_("UI visibility"),
        choices=add_blank_choice(CustomFieldVisibilityChoices),
        required=False,
        initial=''
    )
    is_cloneable = forms.NullBooleanField(
        label=_('Is cloneable'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )

    nullable_fields = ('group_name', 'description', 'choice_set')


class CustomFieldChoiceSetBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=CustomFieldChoiceSet.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    base_choices = forms.ChoiceField(
        choices=add_blank_choice(CustomFieldChoiceSetBaseChoices),
        required=False
    )
    description = forms.CharField(
        required=False
    )
    order_alphabetically = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect()
    )

    nullable_fields = ('base_choices', 'description')


class CustomLinkBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=CustomLink.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    new_window = forms.NullBooleanField(
        label=_('New window'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    weight = forms.IntegerField(
        label=_('Weight'),
        required=False
    )
    button_class = forms.ChoiceField(
        label=_('Button class'),
        choices=add_blank_choice(CustomLinkButtonClassChoices),
        required=False
    )


class ExportTemplateBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ExportTemplate.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    mime_type = forms.CharField(
        label=_('MIME type'),
        max_length=50,
        required=False
    )
    file_extension = forms.CharField(
        label=_('File extension'),
        max_length=15,
        required=False
    )
    as_attachment = forms.NullBooleanField(
        label=_('As attachment'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )

    nullable_fields = ('description', 'mime_type', 'file_extension')


class SavedFilterBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=SavedFilter.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )
    weight = forms.IntegerField(
        label=_('Weight'),
        required=False
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    shared = forms.NullBooleanField(
        label=_('Shared'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )

    nullable_fields = ('description',)


class WebhookBulkEditForm(NetBoxModelBulkEditForm):
    model = Webhook

    pk = forms.ModelMultipleChoiceField(
        queryset=Webhook.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    enabled = forms.NullBooleanField(
        label=_('Enabled'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    type_create = forms.NullBooleanField(
        label=_('On create'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    type_update = forms.NullBooleanField(
        label=_('On update'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    type_delete = forms.NullBooleanField(
        label=_('On delete'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    type_job_start = forms.NullBooleanField(
        label=_('On job start'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    type_job_end = forms.NullBooleanField(
        label=_('On job end'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    http_method = forms.ChoiceField(
        choices=add_blank_choice(WebhookHttpMethodChoices),
        required=False,
        label=_('HTTP method')
    )
    payload_url = forms.CharField(
        required=False,
        label=_('Payload URL')
    )
    ssl_verification = forms.NullBooleanField(
        required=False,
        widget=BulkEditNullBooleanSelect(),
        label=_('SSL verification')
    )
    secret = forms.CharField(
        label=_('Secret'),
        required=False
    )
    ca_file_path = forms.CharField(
        required=False,
        label=_('CA file path')
    )

    nullable_fields = ('secret', 'conditions', 'ca_file_path')


class TagBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    color = ColorField(
        label=_('Color'),
        required=False
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )

    nullable_fields = ('description',)


class ConfigContextBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ConfigContext.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    weight = forms.IntegerField(
        label=_('Weight'),
        required=False,
        min_value=0
    )
    is_active = forms.NullBooleanField(
        label=_('Is active'),
        required=False,
        widget=BulkEditNullBooleanSelect()
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        max_length=100
    )

    nullable_fields = ('description',)


class ConfigTemplateBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=ConfigTemplate.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(
        label=_('Description'),
        max_length=200,
        required=False
    )

    nullable_fields = ('description',)


class JournalEntryBulkEditForm(BulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=JournalEntry.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    kind = forms.ChoiceField(
        label=_('Kind'),
        choices=add_blank_choice(JournalEntryKindChoices),
        required=False
    )
    comments = forms.CharField(
        label=_('Comments'),
        required=False,
        widget=forms.Textarea()
    )
