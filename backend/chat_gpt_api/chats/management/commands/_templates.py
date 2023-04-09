"""
"""
TEMPLATE = """
{%load i18n static custom_icons %} 
{% spaceless %}
<label for="{{form.{{campo}}.id_for_label}}">{{form.{{campo}}.label}}</label>{{form.{{campo}}|add_attr:"form-control"}}{% endspaceless %}"""
