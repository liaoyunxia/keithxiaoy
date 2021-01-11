from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from railguns.django.db.utils import get_object_or_none

from ..accounts.models import WXUid
from .forms import UnRegisterForm

from django.shortcuts import render
from ..accounts.forms import LoginForm

from django.contrib import auth
from django.shortcuts import redirect
from django.utils import timezone

from public.weixin.get_sign import JsApi_pub


def login_m(request):
    title = 'H5登录'

    code = request.GET.get('code', None)
    if not code:
        js = JsApi_pub()
        redirectUrl = "{}/accounts/login/m/".format(settings.BASE_URL)
        url = js.createOauthUrlForCode(redirectUrl)
        return redirect(url)
    else:
        js = JsApi_pub()
        js.setCode(code)
        openid = js.getOpenid()
        if not openid:
            return redirect('/accounts/login/m/')
    return base_login(request, '', 'login.html', '', '', title, openid)


def base_login(request, nav_name="", template_name="", redirect_to='/', error_redirect='', title='', openid=''):
    nav_name = nav_name

    redirect_to = request.POST.get('next', request.GET.get('next', redirect_to))
    if redirect_to is None or redirect_to == '':
        redirect_to = '/'
    redirect_url = request.get_full_path() + '?next={}'.format(redirect_to)

    user_list = get_user_model().objects.all()
    if openid and openid != '0':
        obj = get_object_or_none(WXUid, social_user_id=openid)
        if obj:     # 这个微信号已经绑定过其他用户。直接登录那个用户.
            user = get_object_or_none(get_user_model(), pk=obj.user_id)
            if not request.POST.get('remember-cb', None):
                request.session.set_expiry(0)
            auth.login(request, user)
            user.last_login = timezone.now()
            user.save()
            if not user.is_login:
                redirect_to = '/accounts/update_password/'
            return redirect(redirect_to)

    # get是登录页面，否则是登录请求
    err_msg = ''
    if request.method != 'POST':
        return render(request, template_name, locals())

    form = LoginForm(request.POST)
    if not form.is_valid():
        err_msg = '验证失败,请重新输入'
        if error_redirect != '':
            return redirect(error_redirect)
        return render(request, template_name, locals())

    logininfo = form.cleaned_data
    user = auth.authenticate(username=logininfo['username'], password=logininfo['password'])
    if not user:
        err_msg = '用户名不存在或者密码错误'
        return render(request, 'login.html', locals())

    #  只有携带了openid才会走到这里
    if openid and openid != '0':
        obj = get_object_or_none(WXUid, user_id=user.id)
        if obj:     # 所登录的用户已经注册过.
            if obj.social_user_id != openid:
                err_msg = '欲登录用户已经绑定过其他微信'
                return render(request, 'login.html', locals())
        else:   # 所登录的用户未注册.
            obj = get_object_or_none(WXUid, social_user_id=openid)
            if not obj:     # 这个微信号已经绑定过其他用户。直接登录那个用户.
                WXUid(user_id=user.id, social_user_id=openid).save()

            user.social_user_id = openid
            if not request.POST.get('remember-cb', None):
                request.session.set_expiry(0)

    auth.login(request, user)
    user.last_login = timezone.now()
    user.save()
    # 未登录过.
    if not user.is_login:
        redirect_to = '/accounts/update_password/'
    return redirect(redirect_to)


def login(request):
    title = '登录'
    openid = request.POST.get('openid', '')
    return base_login(request, '', 'login.html', '', '', title, openid)


def logout(request):
    redirect_to = request.GET.get('next')
    if redirect_to is None or redirect_to == '':
        redirect_to = '/'
    auth.logout(request)
    return redirect(redirect_to)


@login_required
def update_password(request):
    return base_update_password(request, nav_name='accounts', template_name='update_password.html', redirect_to='/')


def base_update_password(request, nav_name='', template_name='', redirect_to='', error_template='', error_redirct=''):
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    # 注册成功后，需要跳转去的网址，默认为主页.
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, '/'))
    if redirect_to is None or redirect_to == '':
        redirect_to = '/'
#         if request.user.type == 0:
#             redirect_to = '/accounts/'
#         else:
#             redirect_to = '/business/accounts/'
    if request.method == 'POST':
        user = auth.authenticate(username=request.user.username, password=request.POST.get('old_password'))
        if not user:
            err_msg = '原始密码不正确'
            return render(request, template_name, locals())
        if request.POST.get('password', '') == '' or request.POST.get('repassword', '') == '' or len(request.POST.get('password', '')) < 6:
            err_msg = '输入的密码格式不正确'
            return render(request, template_name, locals())
        if request.POST.get('password', '') != request.POST.get('repassword', ''):
            err_msg = '两次输入的新密码不一致'
            return render(request, template_name, locals())
        user.set_password(request.POST.get('password'))
        user.is_login = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)
        return redirect(redirect_to)
    else:
        return render(request, template_name, locals())


def base_register(request, error_template='', error_redirect='', action_url='', redirect_to=''):
    """注册 基类"""
    err_msg = ''
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    request_data = request.GET
    # 注册成功后，需要跳转去的网址，默认为主页.
    if redirect_to == '':
        redirect_to = request.POST.get(redirect_field_name,
                                       request.get_full_path())
    if redirect_to is None or redirect_to == '':
        redirect_to = '/'
    if request.method == 'POST':
        # 页面间的跳转需要传递next参数.
        redirect_url = request.get_full_path() + '?next={}'.format(redirect_to)
        # 用于检查表单参数.
        form = UnRegisterForm(request.POST)
        # 手机验证码的检查.
        username = request.POST.get('username')
        # 用户参数校验.
        if form.is_valid():
            userinfo = form.cleaned_data
            VALID_USER_FIELDS = [f.name for f in get_user_model()._meta.get_fields() if f.name != 'id']
            user_data = {field: data for (field, data) in request.POST.items() if field in VALID_USER_FIELDS}
            user_data['username'] = request.POST.get('username').lower()
            user_data['nickname'] = '{}100{}'.format('FUND', request.POST.get('username').lower()[-4:])
            if not request.POST.get('phone_number'):
                user_data['phone_number'] = request.POST.get('username').lower()
            if request.POST.get('email'):
                user_data['email'] = request.POST.get('email').lower()
            user = get_user_model().objects.create_user(
                **user_data
            )
            # 创建一个个人资本账户.
            # 用户注册完成之后，自动登录.
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            # return HttpResponse('/userinfo/login/')
            return HttpResponseRedirect(redirect_to)
        else:
            # 校验错误的原因.
            err_msg = '表单验证失败'
            if error_redirect != '':
                return redirect(error_redirect)
            return render(request, error_template, locals())
    else:
        if action_url != '':
            return render(request, error_template, locals())
        else:
            return redirect(error_redirect)
