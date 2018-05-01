#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'ten'
__date__ = ''
__author__ = 'andreyteterevkov'

from django import forms
from django.core.exceptions import ValidationError
import json
from .models import CategoryModel

class JsonForm(forms.Form):
    """
    Форма валидации request.body
    :param (str)data_json
    :return json
    """
    data_json = forms.CharField(required=True, min_length=2)

    def clean_data_json(self):
        data_json = self.cleaned_data['data_json'].replace("\r\n", "")
        if not data_json:
            raise ValidationError(('Not Json data'))
        try:
            data_json = json.loads(data_json)
        except ValueError:
            raise ValidationError(('ValueError in Json'))

        return data_json

class NodeForm(forms.Form):
    """
    Форма валидации node
    :param
        name(str):  Название Категории
        father(int):ID родителя
        path(str):  path from father to node
    """

    name = forms.CharField(required=True, max_length=56, min_length=1)
    father = forms.IntegerField(required=True, min_value=0)
    path = forms.CharField(required=False)
    local_id = forms.IntegerField(min_value=1, required=True)

    def clean_name(self):
        name = self.cleaned_data['name']
        existing_name = CategoryModel.objects.filter(name=name).exists()
        if existing_name:
            raise forms.ValidationError((f'Category name: {name} exist in other category graph'))

        return name