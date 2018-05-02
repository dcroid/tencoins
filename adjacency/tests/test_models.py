#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'ten'
__date__ = ''
__author__ = 'andreyteterevkov'

from django.test import TestCase

from adjacency.models import CategoryModel, CategoryId


class CategoryModelTest(TestCase):

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


    def test_name_label(self):
        catalog = CategoryModel(pk=1)
        field_label = catalog._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Category name')


    def test_name_max_length(self):
        catalog = CategoryModel(pk=1)
        max_length = catalog._meta.get_field('name').max_length
        self.assertEquals(max_length, 56)


    def test_local_id_label(self):
        catalog = CategoryModel(pk=1)
        field_label = catalog._meta.get_field('local_id').verbose_name
        self.assertEquals(field_label, 'Local Graph id')


    def test_category_label(self):
        catalog = CategoryModel(pk=1)
        field_label = catalog._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'Category id')


    def test_father_label(self):
        catalog = CategoryModel(pk=1)
        field_label = catalog._meta.get_field('father').verbose_name
        self.assertEquals(field_label, 'Father')


    def test_path_label(self):
        catalog = CategoryModel(pk=1)
        field_label = catalog._meta.get_field('path').verbose_name
        self.assertEquals(field_label, 'Path to node')


    def test_to_dict(self):
        catalog = CategoryModel.objects.all()

        expected_dict = {
            "id": 2,
            "name": 'Catalog 1'
        }
        self.assertEquals(catalog[0].to_dict(), expected_dict)
