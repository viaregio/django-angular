# -*- coding: utf-8 -*-
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.forms.util import flatatt
from django.forms.widgets import CheckboxInput as BaseCheckboxInput, \
        RadioFieldRenderer as BaseRadioFieldRenderer, RadioSelect as BaseRadioSelect
try:
    from django.forms.widgets import ChoiceFieldRenderer as BaseChoiceFieldRenderer, \
        CheckboxChoiceInput as BaseCheckboxChoiceInput, RadioChoiceInput as BaseRadioChoiceInput
except ImportError:  # in Django <= 1.5 these widgets did not exist
    from djangular.forms.shims import ChoiceFieldRenderer as BaseChoiceFieldRenderer, \
        CheckboxChoiceInput as BaseCheckboxChoiceInput, RadioChoiceInput as BaseRadioChoiceInput
from djangular.forms.widgets import CheckboxSelectMultiple as DjngCheckboxSelectMultiple


class CheckboxChoiceInput(BaseCheckboxChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        label_attrs = ['class="checkbox-inline"']
        if 'id' in self.attrs:
            label_attrs.append(format_html('for="{0}_{1}"', self.attrs['id'], self.index))
        label_for = mark_safe(' '.join(label_attrs))
        return format_html('<label {0}>{1} {2}</label>', label_for, self.tag(), self.choice_label)

    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        if 'ng-model' in self.attrs:
            self.attrs['ng-model'] = '%s.%s' % (self.attrs['ng-model'], self.choice_value)
        name = '%s.%s' % (self.name, self.choice_value)
        final_attrs = dict(self.attrs, type=self.input_type, name=name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        return format_html('<input{0} />', flatatt(final_attrs))


class CheckboxFieldRenderer(BaseChoiceFieldRenderer):
    choice_input_class = CheckboxChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        output = ['<div>']
        for widget in self:
            output.append(force_text(widget))
        output.append('</div>')
        return mark_safe('\n'.join(output))


class CheckboxInput(BaseCheckboxInput):
    def render(self, name, value, attrs=None):
        attrs = attrs or self.attrs
        label_attrs = ['class="checkbox-inline"']
        if 'id' in self.attrs:
            label_attrs.append(format_html('for="{0}"', self.attrs['id']))
        label_for = mark_safe(' '.join(label_attrs))
        tag = super(CheckboxInput, self).render(name, value, attrs)
        return format_html('<label {0}>{1} {2}</label>', label_for, tag, self.choice_label)


class RadioChoiceInput(BaseRadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        label_attrs = ['class="radio-inline"']
        if 'id' in self.attrs:
            label_attrs.append(format_html(' for="{0}_{1}"', self.attrs['id'], self.index))
        label_for = mark_safe(' '.join(label_attrs))
        return format_html('<label {0}>{1} {2}</label>', label_for, self.tag(), self.choice_label)


class RadioFieldRenderer(BaseRadioFieldRenderer):
    choice_input_class = RadioChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        output = ['<div>']
        for widget in self:
            output.append(force_text(widget))
        output.append('</div>')
        return mark_safe('\n'.join(output))


class RadioSelect(BaseRadioSelect):
    renderer = RadioFieldRenderer


class CheckboxSelectMultiple(DjngCheckboxSelectMultiple):
    renderer = CheckboxFieldRenderer
