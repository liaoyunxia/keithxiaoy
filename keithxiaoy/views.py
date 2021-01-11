import json

from django.conf import settings
from django.http.response import HttpResponse, HttpResponseBadRequest
import requests
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class SwaggerSchemaView(APIView):
#     _ignore_model_permissions = True
#     exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)


class PaymentServiceCFCACallBackQuery(APIView):
    permission_classes = (AllowAny,)  # FIXME: 需要限定中金.

    def post(self, request, *args, **kwargs):
        headers = {'Content-Type': 'application/json'}
        url = '{}/notice'.format(settings.JAVA_API)
        result = requests.post(url, data=json.dumps(self.trans_params(request)), headers=headers).text
        try:
            data = json.loads(result)
            return HttpResponse(data['content'])  # 去除双引号.
        except:
            return HttpResponseBadRequest(result)

    def trans_params(self, request):
        temp_dic = {}
        for k, v in request.data.items():
            if k:
                temp_dic[k] = v
        return temp_dic

payment_service_callback = PaymentServiceCFCACallBackQuery.as_view()
