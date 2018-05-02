#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'ten'
__date__ = ''
__author__ = 'andreyteterevkov'

from django.test import TestCase
from adjacency.models import CategoryModel, CategoryId

class CatalogViewPostTest(TestCase):

    def test_create_from_post_false_view(self):
        response = self.client.post('/categories/')

        self.assertEqual(response.status_code, 200)
        if b'"status": "error",' in response.content:
            error = True
        else:
            error = False

        self.assertTrue(error)


    def test_create_from_post_true_view(self):
        json_str = ''' {
"name": "Category 4", "children": [
{
"name": "Category 4.1", "children": [
{
"name": "Category 4.1.1", "children": [
{
"name": "Category 4.1.1.1"
}, {
"name": "Category 4.1.1.2" },
{
"name": "Category 4.1.1.3"
} ]
}, {
"name": "Category 4.1.2", "children": [
{
"name": "Category 4.1.2.1"
}, {
"name": "Category 4.1.2.2" },
{
"name": "Category 4.1.2.3"
} ]
} ]
}, {
"name": "Category 4.2", "children": [
{
"name": "Category 4.2.1"
}, {
"name": "Category 4.2.2", "children": [
{
"name": "Category 4.2.2.1"
}, {
"name": "Category 4.2.2.2" }
] }
] }
] }'''
        response = self.client.post('/categories/',data=json_str, content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        if b'"status": "success",' in response.content:
            content = True
        else:
            content = False

        self.assertTrue(content)


class CatalogViewGetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category_id = CategoryId.objects.create(
            data='{}'
        )

        CategoryModel.objects.create(
            name="Category 4", local_id="1", father=None, path="[]", category=category_id
        )

    def test_get_id_from_view(self):
        response = self.client.get('/categories/3/')
        self.assertEqual(response.status_code, 200)

        if b'"id": 3,' in response.content:
            content = True
        else:
            content = False

        self.assertTrue(content)