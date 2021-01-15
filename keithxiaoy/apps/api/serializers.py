from collections import OrderedDict

from django.contrib.auth import get_user_model
from railguns.django.db.utils import get_object_or_none
from railguns.rest_framework.mixins import TagsMixin, IdStrMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from railguns.utils.func_ext import get_result, get_app_name, is_offce, \
    BaseExceptions, is_valid_date

from .mixins import UserMixin

#
# def get_image_urls(value):
#     data = [{'url': item.strip(), 'uri': item.strip()} for item in value.split('|')]
#     return get_result(len(data), data)
#
#
# def get_order_uri(request, obj):
#     is_approver = 1 if obj.cur_approver == request.user.id else 0
#     vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=obj.flow, ording=obj.flow_node)
#     app_name = get_app_name(request)
#     if app_name == 'factor':
#         if is_offce(request) and obj.type == 'b' and obj.state == 4:
#             return 'factor://ticket/contract/add/{}'.format(obj.id)
#         if is_approver and obj.state != 2:
#             return vetting_node.mobile_url.replace('/PK', '/{}'.format(obj.id)).strip()
#         else:
#             if obj.type == 'c':
#                 return 'factor://customer/detail/{}'.format(obj.id)
#             elif obj.type == 'b':
#                 return 'factor://ticket/detail/{}'.format(obj.id)
#             else:
#                 return 'factor://transferdiscount/detail/{}'.format(obj.id)
#     else:
#         if is_offce(request) and obj.type == 'b' and obj.state == 4:
#             return '/bills/bind/contract/{}/'.format(obj.id)
#         if is_approver and obj.state != 2:
#             return vetting_node.web_url.replace('/PK', '/{}'.format(obj.id)).strip()
#         else:
#             if obj.type == 'c':
#                 return '/customers/{}/'.format(obj.id)
#             elif obj.type == 'b':
#                 return '/bills/{}/'.format(obj.id)
#             else:
#                 return '/transferdiscounts/{}/'.format(obj.id)
#     return ''
#
#
# class ValidateBill(Serializer):
#     number = serializers.CharField(max_length=100, default='')
#     bill_child_type = serializers.IntegerField(default=0)
#     financier = serializers.IntegerField(default=0)
#     drawer = serializers.IntegerField(default=0)
#     pay_value = serializers.IntegerField(default=0)
#     draw_time = serializers.CharField(default='')
#     positive_image_url = serializers.CharField(max_length=200, default='')
#     sale_contract_image_url = serializers.CharField(max_length=2000, default='')
#     invoice_image_url = serializers.CharField(max_length=200, default='')
#
#     def validate(self, data):
#         request = self.context.get('request')
#         data = request.data
#         if 'grace_period' not in data:
#             raise BaseExceptions('调整天数不合法')
#         if 'period' not in data:
#             raise BaseExceptions('贴现天数不合法')
#         if 'prepayment_amount' not in data:
#             raise BaseExceptions('放款金额金合法')
#         return data
#
#     def validate_number(self, value):
#         if len(value) < 1 or len(value) > 100:
#             ex = BaseExceptions('票号不合法')
#             raise ex
#         return value
#
#     def validate_bill_child_type(self, value):
#         if value not in [1, 2]:
#             raise BaseExceptions('票据类型不合法')
#         return value
#
#     def validate_financier(self, value):
#         customer_obj = get_object_or_none(Customer, using='default', pk=value)
#         if not customer_obj:
#             raise BaseExceptions('融资人不存在')
#         return value
#
#     def validate_drawer(self, value):
#         customer_obj = get_object_or_none(Customer, using='default', pk=value)
#         if not customer_obj:
#             raise BaseExceptions('出票人不存在')
#         return value
#
#     def validate_pay_value(self, value):
#         if value <= 0:
#             raise BaseExceptions('票面金额不合法')
#         return value
#
#     def validate_draw_time(self, value):
#         if not is_valid_date(value):
#             raise BaseExceptions('出票日格式不合法')
#         return value
#
#     def validate_positive_image_url(self, value):
#         if value == '':
#             raise BaseExceptions('请传入商票正面清晰照片')
#         return value
#
#     def validate_sale_contract_image_url(self, value):
#         if value == '':
#             raise BaseExceptions('请传入买卖合同附件')
#         return value
#
#     def validate_invoice_image_url(self, value):
#         if value == '':
#             raise BaseExceptions('请传入发票照片')
#         return value
#
#
# class ValidateLoanApplySerializer(Serializer):
#
#     def validate(self, data):
#         request = self.context.get('request')
#         data = request.data
#         if 'grace_period' not in data:
#             raise BaseExceptions('调整天数不合法')
#         if 'period' not in data:
#             raise BaseExceptions('贴现天数不合法')
#         if 'prepayment_amount' not in data:
#             raise BaseExceptions('放款金额金合法')
#         return data
#
#
# class OrganizationListSerializer(ModelSerializer):
#     class Meta:
#         model = Organization
#         exclude = ['remark', 'about']
#
#
# class OrderListSerializer(TagsMixin, UserMixin, ModelSerializer):
#     status = SerializerMethodField()
#     vetting = SerializerMethodField()
#     uri = SerializerMethodField()
#     type = SerializerMethodField()
#
#     class Meta:
#         model = Order
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_type(self, obj):
#         CHOICES = ('c', '授信审批'), ('b', '票据审批'), ('t', '转贴审批')
#         status_list = [i[1] for i in CHOICES if i[0] == obj.type]
#         return {
#             'code': obj.type,
#             'message': '' if status_list == [] else status_list[0]}
#
#     def get_status(self, obj):
#         if obj.state == -1:
#             return {'code': -1, 'message': '未提交'}
#         elif obj.state == 1:
#             return {'code': 1, 'message': '审核中'}
#         elif obj.state == 2:
#             return {'code': 2, 'message': '审核完成'}
#         elif obj.state == 3:
#             return {'code': 3, 'message': '审核失败'}
#         else:
#             return {'code': obj.state, 'message': '审核中'}
#
#     def get_vetting(self, obj):
#         if obj.state == 4:
#             return {'code': 4, 'message': '制作保理合同'}
#         if obj.state in [-1, 2, 3]:
#             return {'code': obj.state,
#                     'message': ''}
#         else:
#             vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=obj.flow, ording=obj.flow_node)
#             if vetting_node:
#                 return {'code': obj.state, 'message': vetting_node.name}
#         return {'code': 0, 'message': ''}
#
#     def get_uri(self, obj):
#         request = self.context.get('request')
#         return get_order_uri(request, obj)
#
#
# class OrderDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         exclude = ['updated_time']
#
#     def to_representation(self, value):
#         order_result = OrderListSerializer(value, context={'request': self.context.get('request')}).data
#         if value.type == 'c':
#             #  授信审批.
#             customer = get_object_or_none(Customer, using='default', pk=value.object_id)
#             if customer:
#                 order_result['customer'] = CustomerDetailSerializer(customer).data
#         elif value.type == 'b':
#             #  票据审批.
#             bill_object = get_object_or_none(Bill, using='default', pk=value.object_id)
#             if bill_object:
#                 order_result['bill'] = BillDetailSerializer(bill_object).data
#         else:
#             transfer_object = get_object_or_none(Transferdiscount, using='default', pk=value.object_id)
#             if transfer_object:
#                 order_result['transferdiscount'] = TransferdiscountDetailSerializer(transfer_object).data
#         diary_list = [VettingDiaryListSerializer(item).data for item in VettingDiary.objects.filter(order_id=value.id).order_by('created_time')]
#         vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=value.flow, ording=value.flow_node)
#         last_diary = {}
#         if value.state == 4:
#             last_diary = self.get_last_diary(None, '待制作', '制作保理合同', value.id, state=4)
#         if value.state not in [-1, 2, 3]:
#             if vetting_node:
#                 last_diary = self.get_last_diary(vetting_node.approver, '审批中', vetting_node.name, value.id)
#         if last_diary != {}:
#             diary_list.append(last_diary)
#         order_result['diaries'] = get_result(len(diary_list), diary_list)
#         return order_result
#
#     def get_last_diary(self, user, message, process_name, order_id, state=0):
#         data = {'id': 0,
#                 'user': self.get_user_info(user, state),
#                 'vetting_result': {'code': 1, 'message': message, 'color': '#F5A623'},
#                 'created_time': '2017-01-01 00:00:00',
#                 'is_active': True,
#                 'process_name': process_name,
#                 'order_id': order_id,
#                 'vetting_state': '',
#                 'remark': '',
#                 'tags': ''
#                 }
#         return data
#
#     def get_user_info(self, obj, state):
#         data = []
#         if obj:
#             data = [{'url': item.strip(), 'uri': item.strip()} for item in obj.image_urls.split('\n')]
#         name = '营销内勤' if state == 4 else ''
#         return OrderedDict([
#             ('id', obj.id if obj else 0),
#             ('username', obj.username if obj else ''),
#             ('name', obj.name if obj else name),
#             ('images', OrderedDict([('count', len(data)), ('next', None), ('previous', None), ('results', data)]))
#         ])
#
#
# class VettingDiaryListSerializer(UserMixin, ModelSerializer):
#     vetting_result = SerializerMethodField()
#
#     class Meta:
#         model = VettingDiary
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_vetting_result(self, obj):
#         CHOICES = ((-1, '不通过'), (1, '通过'))
#         status_list = [i[1] for i in CHOICES if i[0] == obj.vetting_result]
#         return {'code': obj.vetting_result,
#                 'message': '' if status_list == [] else status_list[0],
#                 'color': '#009688' if obj.vetting_result == 1 else '#D0011B'}
#
#
# class BillDetailSerializer(UserMixin, ModelSerializer):
#     financier = SerializerMethodField()
#     drawer = SerializerMethodField()
#     positive_image_url = SerializerMethodField()
#     negative_image_url = SerializerMethodField()
#     sale_contract_image_url = SerializerMethodField()
#     invoice_image_url = SerializerMethodField()
#     statement_image_url = SerializerMethodField()
#     invoice_statement_image_url = SerializerMethodField()
#     receivable_transfer_image_url = SerializerMethodField()
#     receivable_register_image_url = SerializerMethodField()
#     discount_agreement_image_url = SerializerMethodField()
#     invoice_sign_image_url = SerializerMethodField()
#     payment_requisition_image_url = SerializerMethodField()
#     discounting_voucher_image_url = SerializerMethodField()
#     interest_table_image_url = SerializerMethodField()
#     ticket_file_image_url = SerializerMethodField()
#     collection_agreement_image_url = SerializerMethodField()
#     other_files = SerializerMethodField()
#     download_urls = SerializerMethodField()
#     organizations = SerializerMethodField()
#     contract = SerializerMethodField()
#     loan_time = SerializerMethodField()
#     loan_apply = SerializerMethodField()
#
#     class Meta:
#         model = Bill
#         exclude = ['updated_time', 'user_id', 'user_image_urls', 'username']
#
#     def get_organizations(self, obj):
#         user_obj = get_object_or_none(get_user_model(), using='default', pk=obj.user_id)
#         organization_list = [OrganizationListSerializer(item).data for item in user_obj.organization.all()]
#         return get_result(len(organization_list), organization_list)
#
#     def get_contract(self, obj):
#         contract_obj = Contract.objects.filter(number=obj.contract_number)
#         if len(contract_obj) > 0:
#             return ContractListSerializer(contract_obj[0]).data
#         else:
#             return ContractListSerializer(None).data
#
#     def get_loan_time(self, obj):
#         loan_apply_list = LoanApply.objects.filter(bill_id=obj.id)
#         if len(loan_apply_list) > 0:
#             return LoanApplyDetailSerializer(loan_apply_list[0]).data
#         return LoanApplyDetailSerializer(None).data
#
#     def get_loan_apply(self, obj):
#         loan_apply_list = LoanApply.objects.filter(bill_id=obj.id)
#         data = [LoanApplyDetailSerializer(item).data for item in loan_apply_list]
#         return get_result(len(data), data)
#
#     def get_financier(self, obj):
#         customer_object = get_object_or_none(Customer, using='default', pk=obj.financier)
#         return CustomerListSerializer(customer_object).data
#
#     def get_drawer(self, obj):
#         customer_object = get_object_or_none(Customer, using='default', pk=obj.drawer)
#         return CustomerListSerializer(customer_object).data
#
#     def get_download_urls(self, obj):
#         annex_obj = get_object_or_none(Annex, using='default', bill_id=obj.id)
#         return AnnexDetailSerializer(annex_obj).data
#
#     def get_discount_agreement_image_url(self, obj):
#         return get_image_urls(obj.discount_agreement_image_url)
#
#     def get_invoice_sign_image_url(self, obj):
#         return get_image_urls(obj.invoice_sign_image_url)
#
#     def get_payment_requisition_image_url(self, obj):
#         return get_image_urls(obj.payment_requisition_image_url)
#
#     def get_discounting_voucher_image_url(self, obj):
#         return get_image_urls(obj.discounting_voucher_image_url)
#
#     def get_interest_table_image_url(self, obj):
#         return get_image_urls(obj.interest_table_image_url)
#
#     def get_ticket_file_image_url(self, obj):
#         return get_image_urls(obj.ticket_file_image_url)
#
#     def get_collection_agreement_image_url(self, obj):
#         return get_image_urls(obj.collection_agreement_image_url)
#
#     def get_other_files(self, obj):
#         return get_image_urls(obj.other_files)
#
#     def get_positive_image_url(self, obj):
#         return get_image_urls(obj.positive_image_url)
#
#     def get_negative_image_url(self, obj):
#         return get_image_urls(obj.negative_image_url)
#
#     def get_sale_contract_image_url(self, obj):
#         return get_image_urls(obj.sale_contract_image_url)
#
#     def get_invoice_image_url(self, obj):
#         return get_image_urls(obj.invoice_image_url)
#
#     def get_statement_image_url(self, obj):
#         return get_image_urls(obj.statement_image_url)
#
#     def get_invoice_statement_image_url(self, obj):
#         return get_image_urls(obj.invoice_statement_image_url)
#
#     def get_receivable_transfer_image_url(self, obj):
#         return get_image_urls(obj.receivable_transfer_image_url)
#
#     def get_receivable_register_image_url(self, obj):
#         return get_image_urls(obj.receivable_register_image_url)
#
#
# class AnnexDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Annex
#         exclude = ['bill_id']
#
#
# class CustomerListSerializer(UserMixin, ModelSerializer):
#     contacts = SerializerMethodField()
#     payments = SerializerMethodField()
#     business_license = SerializerMethodField()
#     financial_statements = SerializerMethodField()
#     organization_certificate = SerializerMethodField()
#     tax_enrol_certificate = SerializerMethodField()
#     loan_card = SerializerMethodField()
#     permits_accounts = SerializerMethodField()
#     legal_representative_id_card = SerializerMethodField()
#     institution_credit_code = SerializerMethodField()
#     attribute = SerializerMethodField()
#     ownership_quality = SerializerMethodField()
#
#     class Meta:
#         model = Customer
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_attribute(self, obj):
#         status_list = [i[1] for i in CONSUMER_ATTRIBUTE if i[0] == obj.attribute]
#         if status_list != []:
#             return {'code': obj.attribute,
#                     'message': '' if status_list == [] else status_list[0]}
#         return {'code': '0', 'message': ''}
#
#     def get_ownership_quality(self, obj):
#         status_list = [i[1] for i in OWNERSHIP_CHIOCES if i[0] == obj.ownership_quality]
#         if status_list != []:
#             return {'code': obj.ownership_quality,
#                     'message': '' if status_list == [] else status_list[0]}
#         return {'code': '0', 'message': ''}
#
#     def get_business_license(self, obj):
#         return get_image_urls(obj.business_license)
#
#     def get_financial_statements(self, obj):
#         return get_image_urls(obj.financial_statements)
#
#     def get_organization_certificate(self, obj):
#         return get_image_urls(obj.organization_certificate)
#
#     def get_tax_enrol_certificate(self, obj):
#         return get_image_urls(obj.tax_enrol_certificate)
#
#     def get_loan_card(self, obj):
#         return get_image_urls(obj.loan_card)
#
#     def get_permits_accounts(self, obj):
#         return get_image_urls(obj.permits_accounts)
#
#     def get_legal_representative_id_card(self, obj):
#         return get_image_urls(obj.legal_representative_id_card)
#
#     def get_institution_credit_code(self, obj):
#         return get_image_urls(obj.institution_credit_code)
#
#     def get_contacts(self, obj):
#         data = []
#         for item in obj.contacts.all():
#             data.append(ContactDetailSerializer(item).data)
#         return get_result(len(data), data)
#
#     def get_payments(self, obj):
#         data = []
#         for item in obj.payments.all():
#             data.append(PaymentDetailSerializer(item).data)
#         return get_result(len(data), data)
#
#
# class CustomerDetailSerializer(CustomerListSerializer):
#     class Meta:
#         model = Customer
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#
# class ContactDetailSerializer(TagsMixin, UserMixin, ModelSerializer):
#
#     class Meta:
#         model = Contact
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#
# class PaymentDetailSerializer(ModelSerializer):
#     contacts = SerializerMethodField()
#
#     class Meta:
#         model = PaymentAccount
#         exclude = ['updated_time']
#
#     def get_contacts(self, obj):
#         data = []
#         for item in obj.contacts.all():
#             data.append(ContactDetailSerializer(item).data)
#         return get_result(len(data), data)
#
#
# class ContractListSerializer(UserMixin, ModelSerializer):
#     buyers = SerializerMethodField()
#
#     class Meta:
#         model = Contract
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_buyers(self, obj):
#         data = []
#         for item in obj.buyers.all():
#             data.append(BuyerListSerializer(item).data)
#         return get_result(len(data), data)
#
#
# class ContractDetailSerializer(UserMixin, ModelSerializer):
#     buyers = SerializerMethodField()
#     seller = SerializerMethodField()
#
#     class Meta:
#         model = Contract
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_seller(self, obj):
#         customer_obj = get_object_or_none(Customer, using='default', pk=int(obj.seller_id))
#         return CustomerDetailSerializer(customer_obj).data
#
#     def get_buyers(self, obj):
#         data = []
#         for item in obj.buyers.all():
#             data.append(BuyerListSerializer(item).data)
#         return get_result(len(data), data)
#
#
# class BuyerListSerializer(UserMixin, ModelSerializer):
#     customer = SerializerMethodField()
#     business_type = SerializerMethodField()
#
#     class Meta:
#         model = Buyer
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_customer(self, obj):
#         customer_obj = get_object_or_none(Customer, using='default', pk=obj.customer_id)
#         return CustomerListSerializer(customer_obj).data
#
#     def get_business_type(self, obj):
#         CONSUMER_ATTRIBUTE = (('1', '公开'), ('2', '隐蔽'))
#         status_list = [i[1] for i in CONSUMER_ATTRIBUTE if i[0] == obj.business_type]
#         if status_list != []:
#             return {'code': obj.business_type,
#                     'message': '' if status_list == [] else status_list[0]}
#         return {'code': '0', 'message': ''}
#
#
# class VettingFlowListSerializer(ModelSerializer):
#     class Meta:
#         model = VettingFlow
#         fields = ['id', 'name']
#
#
# class UserPasswordSerializer(ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['password']
#
#     def validate_password(self, value):
#         if len(value) < 6:
#             raise ValidationError('password length must more than 6')
#         return value
#
#
# class LoanApplyDetailSerializer(ModelSerializer):
#     payment_account = SerializerMethodField()
#
#     class Meta:
#         model = LoanApply
#         exclude = ['updated_time', 'bill_id']
#
#     def get_payment_account(self, obj):
#         payment_obj = get_object_or_none(PaymentAccount, using='default', pk=obj.payment_account_id)
#         return PaymentDetailSerializer(payment_obj).data
#
#
# class NotificationDetailSerializer(IdStrMixin, ModelSerializer):
#     uri = SerializerMethodField()
#
#     class Meta:
#         model = Notification
#         exclude = ['updated_time', 'user_id', 'order_id', 'is_read']
#
#     def get_uri(self, obj):
#         request = self.context.get('request')
#         order_obj = get_object_or_none(Order, using='default', pk=obj.order_id)
#         if order_obj:
#             return get_order_uri(request, order_obj)
#         return ''
#
#
# class BankListSerializer(UserMixin, ModelSerializer):
#     type = SerializerMethodField()
#     contacts = SerializerMethodField()
#     payments = SerializerMethodField()
#
#     class Meta:
#         model = Bank
#         exclude = ['updated_time', 'user_id', 'username', 'user_image_urls']
#
#     def get_type(self, obj):
#         CHOICES = ((1, '商票质押'), (2, '商票贴现'))
#         status_list = [i[1] for i in CHOICES if i[0] == obj.type]
#         return {
#             'code': obj.type,
#             'message': '' if status_list == [] else status_list[0]}
#
#     def get_contacts(self, obj):
#         data = []
#         for item in obj.contacts.all():
#             data.append(ContactDetailSerializer(item).data)
#         return get_result(len(data), data)
#
#     def get_payments(self, obj):
#         data = []
#         for item in obj.payments.all():
#             data.append(PaymentDetailSerializer(item).data)
#         return get_result(len(data), data)
#
#
# class TransferdiscountDetailSerializer(ModelSerializer):
#     bill = SerializerMethodField()
#     drawer = SerializerMethodField()
#     bank = SerializerMethodField()
#
#     class Meta:
#         model = Transferdiscount
#         exclude = ['updated_time']
#
#     def get_bill(self, obj):
#         return BillDetailSerializer(obj.bill).data
#
#     def get_drawer(self, obj):
#         return CustomerListSerializer(obj.drawer).data
#
#     def get_bank(self, obj):
#         return BankListSerializer(obj.bank).data
