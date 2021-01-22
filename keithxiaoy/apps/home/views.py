from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from railguns.django.db.utils import get_object_or_none
from railguns.django.generics import WebView
from ..articles.models import Article


class HomeView(WebView):
    def get(self, request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect('/accounts/login/')
        title = kwargs.get('title', '{} - {}'.format(_(self.name), _('app_name')))
        # opt_type = self.request.GET.get('type', '')
        # endpoint = '{}{}'.format('/api/v1/orders', request.get_full_path())
        # template_name = self.template_nam

        top_article = Article.objects.filter(set_top=True, type=3).order_by('priority', '-modify_time').first()
        valid_blogs = Article.objects.filter(type=3).order_by('-modify_time').exclude(name='about_me', id=top_article.id)

        template_name = 'index.html'
        return render(request, template_name, locals())
