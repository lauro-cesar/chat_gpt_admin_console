import imp
from django import template
import json

register = template.Library()
from django.urls import reverse
import logging
logger = logging.getLogger(__name__)

@register.filter(name="contains_path")
def contains_path(model_path, app_path):
    if model_path.startswith(app_path):
        return "block"
    return "none"


@register.filter(name="active_path")
def active_path(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "menu-open active selected"
    return ""


@register.filter(name="active_url")
def active_url(v_1, v_2):
    l = [str(v_1)]
    if reverse(str(v_2)) in l:
        return "menu-open active selected"
    return ""


@register.filter(name="active_class")
def active_class(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "active selected"
    return ""


@register.filter(name="is_active_option")
def is_active_option(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "active selected"
    return ""


@register.filter(name="add_html_attr")
def add_html_attrs(field, attrs):
    return field


@register.filter(name="add_css_class")
def add_css_class(field, css):
    attrs = {}
    definition = css.split(",")
    for d in definition:
        if ":" not in d:
            attrs["class"] = d
        else:
            key, val = d.split(":")
            attrs[key] = val

    return field.as_widget(attrs=attrs)


@register.filter(name="add_attr")
def add_attr(field, css):
    attrs = {}
    definition = css.split(",")
    for d in definition:
        if ":" not in d:
            attrs["class"] = d
        else:
            key, val = d.split(":")
            attrs[key] = val

    return field.as_widget(attrs=attrs)


@register.filter(name="context_info")
def context_info(value):
    return dir(value)


@register.filter(name="object_keys")
def object_keys(value):
    return dir(value)


@register.filter(name="debug_me")
def debug_me(value):
    return value


@register.filter(name="is_right_msg")
def is_left_msg(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "right"
    return "left"


@register.filter(name="active_item")
def active_item(v_1, v_2):
    l = [str(v_1)]
    if reverse(str(v_2)) in l:
        return "menu-open active selected"
    return ""


@register.filter(name="active_class")
def active_class(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "active selected"
    return ""


@register.filter(name="is_active_option")
def is_active_option(v_1, v_2):
    l = [str(v_1)]
    if str(v_2) in l:
        return "active selected"
    return ""


@register.filter(name="sum_float")
def sum_float(value, arg):
    return value + arg


@register.filter(name="x_or_none")
def x_or_none(value, arg):
    return value + arg
