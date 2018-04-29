from django.db import models
import json
# Create your models here.


class CategoryModel(models.Model):

    class Meta:
        db_table = 'category'

    name = models.CharField(
        max_length=56,
        verbose_name='Category name',
        null=False,
        unique=True
    )
    father = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Father'
    )

    path = models.CharField(
        max_length=1024,
        verbose_name='Path to node'
    )

    def to_dict(self):
        """
        Return myself (id, name)
        :return: dict
        """
        return {
            "id": self.id,
            "name": self.name
        }

    def get_family(self):
        """
        Get all adjacency (id, name): myself, parents, children, siblings
        :return: dict
        """
        family = self.to_dict()

        # get parents
        query_parents = CategoryModel.objects.in_bulk(json.loads(self.path))
        parents = {"father": [query_parents[f].to_dict() for f in query_parents]}
        family.update(parents)

        # get children
        query_children = CategoryModel.objects.filter(father=self)
        children = {"children": [f.to_dict() for f in query_children]}
        family.update(children)

        # get siblings
        query_siblings = CategoryModel.objects.filter(father=self.father).exclude(pk=self.pk)
        siblings = {"siblings": [f.to_dict() for f in query_siblings]}
        family.update(siblings)

        return family


    @classmethod
    def create_object(cls, json):
        """
        Create new Category object
        :param - json
        :return - object
        """
        new_object = dict(
            name=json['name'],
            father_id=json['father'] if json['father'] != 0 else None,
            path=json['path']
        )

        node = cls(**new_object)
        return node

