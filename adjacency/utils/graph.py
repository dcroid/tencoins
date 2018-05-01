#!/usr/bin/python
# -*- coding: UTF-8 -*-
__project__ = 'ten'
__date__ = ''
__author__ = 'andreyteterevkov'


class Graph:

    def __init__(self, data):
        self.data = data
        self.num = 0
        self.tree = []
        self.cat_names = []

    def __call__(self):
       return self.node(self.data)

    def node(self, data, father=0, root_path=''):
        """
        Generator for passage full graph
            :param
                data - json request
                father - Id father
                root_path - path from root to node
            :returns -  generator
        """
        if not isinstance(data, dict):
            raise Exception('Error node type!')

        if 'name' in data:
            self.re_name(data['name'])
            self.num += 1
            path = [int(id) for id in root_path.split("|")[:-1]]
            yield {'name': data['name'], 'local_id': self.num, 'father': father, 'path': str(path)}

        if 'children' in data:

            if not isinstance(data['children'], list):
                raise Exception('Error children type!')

            father = self.num
            root_path += "{}|".format(father)
            for _ in data['children']:
                yield from self.node(_, father, root_path)

    def re_name(self, name):
        if name in self.cat_names:
            raise Exception('Name "{}" exists!'.format(name))
        self.cat_names.append(name)
        return
