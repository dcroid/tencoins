#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'ten'
__date__ = ''
__author__ = 'andreyteterevkov'


from django.test import TestCase

from adjacency.forms import JsonForm, NodeForm
from adjacency.models import CategoryModel, CategoryId


class JsonFormTest(TestCase):

    def test_data_json_valid_true(self):
        data_json = {'data_json': '{"name": "Catalog 1", "children": []}'}
        form = JsonForm(data_json)
        self.assertTrue(form.is_valid())

    def test_data_json_valid_false(self):
        data_json = {'data_json': "{'name': 'Catalog 1', 'children': []}"}
        form = JsonForm(data_json)
        self.assertFalse(form.is_valid())


class NodeFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category_id = CategoryId.objects.create(
            data='{}'
        )
        CategoryModel.objects.create(
            name="Catalog 1",
            local_id=1,
            father=None,
            path='[]',
            category=category_id
        )

    def test_name_valid_true(self):
        data_from = dict(
            name='Catalog 2',
            path='[1]',
            local_id=2,
            father=1
        )
        form = NodeForm(data_from)
        self.assertTrue(form.is_valid())

    def test_name_valid_false(self):
        data_from = dict(
            name='Catalog 1',
            path='[1]',
            local_id=2,
            father=1
        )
        form = NodeForm(data_from)
        self.assertFalse(form.is_valid())
