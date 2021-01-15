
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import WXUid


class BaseForm(forms.Form):
    password = forms.CharField(label=_('Password'),
                               min_length=6,
                               widget=forms.PasswordInput)


class ValidateRegisterForm(forms.Form):
    username = forms.RegexField(label=_('username'),
                                min_length=3,
                                max_length=30,
                                regex=r'^[\w]+$',
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                error_messages={'invalid': _('This value may contain only letters, numbers and '
                                                             '@/./+/-/_ characters.')})


class RegisterInstitutionUserForm(BaseForm):
    username = forms.RegexField(label=_('username'),
                                min_length=3,
                                max_length=30,
                                regex=r'^[\w]+$',
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                error_messages={'invalid': _('This value may contain only letters, numbers and '
                                                             '@/./+/-/_ characters.')})

    institution_name = forms.RegexField(label=_('institution_name'),
                                        min_length=1,
                                        max_length=30,
                                        regex=r'^[\w]+$',
                                        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                                    '@/./+/-/_ only.'),
                                        error_messages={'invalid': _('This value may contain only letters, numbers and '
                                                                     '@/./+/-/_ characters.')})


class UnRegisterForm(forms.Form):

    def clean_openid(self):
        openid = self.cleaned_data['openid']
        if not openid or WXUid.objects.filter(pk=openid):
            raise forms.ValidationError('该微信用户已经注册，请等待认证通过')
        return openid


class LoginForm(forms.Form):
    username = forms.RegexField(label=_('username'),
                                min_length=5,
                                max_length=30,
                                regex=r'^[\w]+$',
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                error_messages={'invalid': _('This value may contain only letters, numbers and '
                                                             '@/./+/-/_ characters.')})
    password = forms.CharField(label=_('Password'),
                               min_length=6,
                               widget=forms.PasswordInput)
