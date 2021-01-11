from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.utils import get_object_or_none
from railguns.django.generics import WebView

from ..orders.models import Order
from ..vetting.models import VettingNode
from public.utils.func_ext import is_offce
from public.weixin.get_sign import JsApi_pub


def caculater(request):
    title = '贴现计算器'
    return render(request, 'caculater.html', locals())


class HomeView(WebView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/accounts/login/')
        title = kwargs.get('title', '{} - {}'.format(_(self.name), _('app_name')))
        opt_type = self.request.GET.get('type', '')
        endpoint = '{}{}'.format('/api/v1/orders', request.get_full_path())
        template_name = self.template_name if self.template_name else '{}.html'.format(self.name)
        return render(request, template_name, locals())


def wx_redirect_url(request):
    code = request.GET.get('code')
    order_id = int(request.GET.get('order_id', 0))
    order_obj = get_object_or_none(Order, using='default', id=order_id)
    if request.user.is_authenticated():
        url = get_order_url(request, order_obj)
        return redirect(url)
    js = JsApi_pub()
    if not code:
        redirectUrl = '{}/{}'.format(settings.BASE_URL, request.get_full_path())
        url = js.createOauthUrlForCode(redirectUrl)
        return redirect(url)
    else:
        js.setCode(code)
        openid = js.getOpenid()
        user = get_object_or_none(get_user_model(), social_user_id=openid)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        if order_obj:
            url = get_order_url(request, order_obj)
            return redirect(url)
        return redirect('/')


def get_order_url(request, obj):
    is_approver = 1 if obj.cur_approver == request.user.id else 0
    vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=obj.flow, ording=obj.flow_node)
    if is_offce(request) and obj.type == 'b' and obj.state == 4:
            return '/bills/bind/contract/{}/'.format(obj.id)
    if is_approver and obj.state != 2:
        return vetting_node.web_url.replace('/PK', '/{}'.format(obj.id)).strip()
    else:
        return '/customers/{}/'.format(obj.id) if obj.type == 'c' else '/bills/{}/'.format(obj.id)
    return ''
