# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from server.forms import SubscriptionForm, SubscriptionFormWithNgModel


class NgFormValidationView(TemplateView):
    template_name = 'subscribe-form.html'
    form_class = SubscriptionForm
    form_attrs = { 'form_name': 'subscribe_form' }

    def get_context_data(self, **kwargs):
        context = super(NgFormValidationView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            # bound form
            form = self.form_class(self.request.POST, **self.form_attrs)
        else:
            # unbound form
            form = self.form_class(**self.form_attrs)
        form.fields['height'].widget.attrs['step'] = 0.05  # Ugly hack to set step size
        context.update(form=form, with_ws4redis=hasattr(settings, 'WEBSOCKET_URL'))
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['form'].is_valid():
            return HttpResponse('Form is valid and has been accepted.')
        return render(request, self.template_name, context)


class NgFormValidationViewWithNgModel(NgFormValidationView):
    template_name = 'subscribe-form-with-model.html'
    form_class = SubscriptionFormWithNgModel
    form_attrs = { 'scope_prefix': 'subscribe_data' }


class Ng3WayDataBindingView(NgFormValidationViewWithNgModel):
    template_name = 'three-way-data-binding.html'
