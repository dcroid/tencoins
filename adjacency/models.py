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
        unique=True,
        db_index=True
    )

    local_id = models.PositiveIntegerField(
        default=1,
        null=False,
        verbose_name="Local Graph id",
        db_index=True
    )

    category = models.ForeignKey(
        to='CategoryId',
        on_delete=models.CASCADE,
        blank=True,
        null=False,
        verbose_name='Category id'
    )

    father = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Father',
        db_index=True
    )

    path = models.TextField(
        verbose_name='Path to node'
    )

    def __str__(self):
        return self.name


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
        query_parents = CategoryModel.objects.filter(
            local_id__in=json.loads(self.path), category_id=self.category_id)

        parents = {"father": [_.to_dict() for _ in query_parents]}
        family.update(parents)

        # get children
        query_children = CategoryModel.objects.filter(
            father=self.local_id, category_id=self.category_id)
        children = {"children": [_.to_dict() for _ in query_children]}
        family.update(children)

        # get siblings
        query_siblings = CategoryModel.objects.filter(
            father=self.father,
            category_id=self.category_id).exclude(pk=self.pk)
        siblings = {"siblings": [_.to_dict() for _ in query_siblings]}
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
            father=json['father'] if json['father'] != 0 else None,
            path=json['path'],
            category_id=json['category_id'],
            local_id=json['local_id']
        )

        node = cls(**new_object)
        return node


class CategoryId(models.Model):

    class Meta:
        db_table = 'category_id'

    data = models.TextField(
        verbose_name='Json dump',
        null=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create date",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated date",
    )

    def __str__(self):
        return "{}...".format(self.data[:58])
