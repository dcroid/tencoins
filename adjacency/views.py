from django.http import JsonResponse
from django.views import View
from adjacency.utils.graph import Graph
from .models import CategoryModel, CategoryId
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

        # create Graph id
        cat_id = CategoryId(**data_graph)
        cat_id.save()

        bulk_object = []
        for node in graph():
            node.update({'category_id': cat_id.id})
            form_node = NodeForm(node)
            if not form_node.is_valid():
                return JsonResponse({'status': 'error', 'result': form_node.errors})

            bulk_object.append(CategoryModel.create_object(node))

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

        id = kwargs.get('id', 1)
        cat = CategoryModel.objects.filter(pk=id)
        if not cat.exists():
            response = JsonResponse({'status': 'false', 'error': 'Id {} not exists'.format(id)})
            response.status_code = 404
            return response
        return JsonResponse(cat.first().get_family())

