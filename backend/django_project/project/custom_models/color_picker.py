from django import forms
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string


class ColorWidget(forms.Widget):
    class Media:
        js = [settings.STATIC_URL + "js/ColorPicker2.js"]

    def render(self, name, value, attrs=None):
        return render_to_string("color_picker_widget.html", locals())


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)
