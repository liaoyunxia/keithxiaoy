from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^orders/$', views.OrderList.as_view()),
    url(r'^bills/$', views.BillList.as_view()),
    url(r'^bills/(?P<pk>[0-9]+)/$', views.BillDetail.as_view()),
    url(r'^banks/$', views.BankList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/password/$', views.UserPasswordUpdate.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/notifications/$', views.UserNotificationList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/notifications/status/$', views.UserNotificationStatus.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/approved/$', views.OrderApproved.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/unapproved/$', views.OrderUnApproved.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view()),
    url(r'^contracts/$', views.ContractCreate.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/contracts/$', views.OrderContractCreate.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/loan_apply/$', views.OrderLoanApplyCreate.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/check_list/$', views.OrderCheckCreate.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/loan_confirm/$', views.OrderLoanConfirm.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/loan_manager/$', views.OrderLoanManager.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/archives_manager/$', views.OrderArchivesManager.as_view()),
    url(r'^orders/(?P<pk>[0-9]+)/upload_material/$', views.OrderUploadMaterial.as_view()),
    url(r'^customers/$', views.CustomerList.as_view()),
    url(r'^customers/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view()),
    url(r'^customers/(?P<pk>[0-9]+)/payment_accounts/$', views.CustomerAccountList.as_view()),
    url(r'^customers/(?P<pk>[0-9]+)/contracts/$', views.CustomerContractList.as_view()),
    url(r'^payment_accounts/$', views.PaymentAccountList.as_view()),
]
