from django.http import JsonResponse
from django.db import connection
from django.views import View
from adjacency.utils.graph import Graph
from .models import CategoryModel
from .forms import JsonForm, NodeForm


class CatalogView(View):

    def post(self, request):
        """
        Check json from request.body and create categories
        Note: From db Truncate old categories, then  Create new from request.body json
            :request.body - json
            :return - json
        """

        body = request.body.decode('utf-8')
        data_json = {'data_json': body}
        form = JsonForm(data_json)

        if not form.is_valid():
            return JsonResponse({'status': 'error', 'result': form.errors})


        data_graph = {'data': form.cleaned_data['data_json']}
        graph = Graph(**data_graph)
        bulk_object = []
        for node in graph():
            form_node = NodeForm(node)
            if not form_node.is_valid():
                return JsonResponse({'status': 'error', 'result': form_node.errors})

            bulk_object.append(CategoryModel.create_object(node))

        # TRUNCATE all object from db
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE`category`")

        # inserts the provided list of object
        CategoryModel.objects.bulk_create(bulk_object)
        return JsonResponse({'status': 'success', 'result': form.cleaned_data['data_json']})


    def get(self, *args, **kwargs):
        """
        Get id category, and your family
            :param kwargs:
                id - Id(pk) Category
            :return: json
        """
        cat = CategoryModel.objects.filter(pk=kwargs.get('id', 1))
        if not cat.exists():
            responce = JsonResponse({'status': 'false', 'error': 'Id {} not exists'.format(id)})
            responce.status_code = 404
            return responce
        return JsonResponse(cat.first().get_family())

