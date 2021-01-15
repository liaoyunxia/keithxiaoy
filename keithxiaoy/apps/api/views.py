import json
import traceback

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from railguns.django.db.utils import get_object_or_none
from railguns.rest_framework.mixins import PutToPatchMixin, \
    PutToPatchApiViewMixin
from railguns.rest_framework.permissions import IsUserSelf, IsOwnerOnList
from railguns.rest_framework.response import ResponseBadRequest
import redis
from rest_framework import generics, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from public.rest_framework.serializers import UserCreatedSerializer
from public.utils.func_ext import write_log, is_offce, get_user_list, is_manager, \
    BaseExceptions, is_financier, get_result
from public.weixin.push_wechat_message import PushWechatMessage



#
# def order_approved(order_obj, request, taget=1):
#     vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=order_obj.flow, ording=order_obj.flow_node)
#     vetting_nodes = VettingNode.objects.filter(vetting_process=order_obj.flow).order_by('ording')
#     cur_node, next_node = 0, vetting_node
#     index = 0
#     for item in vetting_nodes:
#         index += 1
#         if order_obj.flow_node == item.ording:
#             if index != len(vetting_nodes):
#                 next_node = vetting_nodes[index]
#             cur_node = index
#     remark = request.data.get('remark', '')
#     if vetting_node:
#         if order_obj.cur_approver != request.user.id:
#             raise exceptions.PermissionDenied
#         if order_obj.state in [2, 3]:
#             raise exceptions.PermissionDenied
#         if cur_node == len(vetting_nodes):
#             order_obj.approved(2)
#         else:
#             order_obj.approved(taget)
#             if next_node.approver:
#                 order_obj.cur_approver = next_node.approver.id
#             else:
#                 order_obj.cur_approver = order_obj.user_id
#             order_obj.flow_node = next_node.ording
#         order_obj.save()
#         VettingDiary(process_name=vetting_node.name,
#                      order_id=order_obj.id,
#                      vetting_result=1,
#                      remark=remark,
#                      user_id=request.user.id,
#                      username=request.user.username).save()
#         title = "{}操作通知".format(vetting_node.vetting_process.name)
#         content = "{}业务申请单{}在{}审批通过，请及时查看处理。".format(vetting_node.vetting_process.name, order_obj.code, vetting_node.name)
#         write_log('notification_content', '{}'.format(content))
#         Notification(user_id=order_obj.user_id,
#                      title=title,
#                      content=content,
#                      order_id=order_obj.id).save()
#         node_user = get_object_or_none(get_user_model(), using='default', id=order_obj.user_id)
#         if node_user:
#             PushWechatMessage().send_message(node_user.social_user_id, title, content, order_obj.id)
#     return order_obj
#
#
# class UserPasswordUpdate(PutToPatchMixin, generics.UpdateAPIView):
#     """更新 密码"""
#     serializer_class = serializers.UserPasswordSerializer
#     queryset = get_user_model().objects.all()
#     permission_classes = [IsUserSelf]
#
#     def update(self, request, *args, **kwargs):
#         try:
#             if len(self.request.data.get('password', '')) < 6:
#                 return ResponseBadRequest('密码长度不能小于6')
#             user = self.request.user
#             user = auth.authenticate(username=user.username, password=self.request.data.get('old_password', ''))
#             if not user:
#                 return ResponseBadRequest('原始密码不正确')
#             if not user.is_login:
#                 user.is_login = True
#             user.password = make_password(self.request.data.get('password'))
#             user.save()
#             return Response(UserCreatedSerializer(user).data)
#         except Exception:
#             return ResponseBadRequest('密码修改失败')
#
#
# class UserNotificationList(generics.ListAPIView):
#     permission_classes = [IsOwnerOnList]
#     serializer_class = serializers.NotificationDetailSerializer
#
#     def get_queryset(self):
#         return Notification.objects.filter(user_id=self.request.user.id).order_by('-created_time')
#
#     def list(self, request, *args, **kwargs):
#         queryset = super(UserNotificationList, self).list(request, *args, **kwargs)
#         Notification.objects.filter(user_id=self.request.user.id).update(is_read=True)
#         return Response(queryset.data)
#
#
# class UserNotificationStatus(APIView):
#     permission_classes = [IsOwnerOnList]
#
#     def get(self, request, *args, **kwargs):
#         notification_count = Notification.objects.filter(user_id=self.request.user.id, is_read=False).count()
#         return Response({'code': 1 if notification_count > 0 else 0,
#                          'count': notification_count,
#                          'message': '有消息' if notification_count > 0 else '无消息'})
#
#
# class OrderList(generics.ListCreateAPIView):
#     serializer_class = serializers.OrderListSerializer
#     queryset = Order.objects.all()
#
#     def get_queryset(self):
#         if self.request.GET.get('type') == '1':
#             return Order.objects.filter(user_id=self.request.user.id).order_by('-updated_time')
#         elif self.request.GET.get('type') == '0':
#             if is_offce(self.request):
#                 return Order.objects.filter(user_id__in=get_user_list(self.request), state=4).order_by('-updated_time') | Order.objects.filter(cur_approver=self.request.user.id).exclude(state__in=[2, 3]).order_by('-updated_time')
#             return Order.objects.filter(cur_approver=self.request.user.id).exclude(state__in=[2, 3]).order_by('-updated_time')
#         else:
#             return Order.objects.filter(user_id__in=get_user_list(self.request)).order_by('-updated_time')
#
#     def create(self, request, *args, **kwargs):
#         if self.request.data.get('object_type') == 'b':
#             serializer = serializers.ValidateBill(data=request.data, context={'request': self.request})
#             serializer.is_valid(raise_exception=True)
#         if self.request.data.get('object_type') == 't':
#             if not is_financier(request):
#                 raise exceptions.PermissionDenied
#         else:
#             if not is_manager(request):
#                 raise exceptions.PermissionDenied
#         try:
#             write_log('order_create', '{}'.format(self.request.data))
#             order_object = get_object_or_none(Order, using='default', pk=self.request.data.get('id'))
#             if order_object and order_object.state == -1:
#                 raise exceptions.PermissionDenied
#             if self.request.data.get('object_type') == 'c':  # 授信审核申请.
#                 if order_object:
#                     #  若是修改，先清除联系人和账户的关联关系.
#                     self.clear_customer_relation(order_object)
#                 contacts = self.request.data.get('contacts', []) if isinstance(self.request.data.get('contacts', []), list) else json.loads(self.request.data.get('contacts', []))
#                 payments = self.request.data.get('payments', []) if isinstance(self.request.data.get('payments', []), list) else json.loads(self.request.data.get('payments', []))
#
#                 contact_fields = [f.name for f in Contact._meta.get_fields() if f.name != 'id']
#                 contact_list = self.get_contact_list(contact_fields, contacts)
#                 payment_fields = [f.name for f in PaymentAccount._meta.get_fields() if f.name != 'id']
#                 payment_list = self.get_payment_list(payment_fields, payments)
#                 customer_fields = [f.name for f in Customer._meta.get_fields() if f.name not in ['id', 'contacts', 'payments']]
#                 customer_data = {field: data for (field, data) in self.request.data.items() if field in customer_fields}
#                 if not order_object:
#                     customer = Customer.objects.create_customer(self.request, contact_list, payment_list, **customer_data)
#                 else:
#                     customer = Customer.objects.update_customer(order_object.object_id, contact_list, payment_list, **customer_data)
#                 order = self.create_order_object(customer, order_object)
#                 if not order:
#                     return ResponseBadRequest('请先确认所在单位以及流程都配置正确')
#                 return Response(serializers.OrderDetailSerializer(order, context={'request': self.request}).data)
#             elif self.request.data.get('object_type') == 'b':
#                 bill_fields = [f.name for f in Bill._meta.get_fields() if f.name != 'id']
#                 bill_data = {field: data for (field, data) in self.request.data.items() if field in bill_fields}
#                 if not order_object:
#                     bill = Bill.objects.create_bill(request, **bill_data)
#                 else:
#                     bill = Bill.objects.update_bill(order_object.object_id, **bill_data)
#                 order = self.create_order_object(bill, order_object)
#                 if not order:
#                     return ResponseBadRequest('请先确认所在单位以及流程都配置正确')
#                 redis_client = redis.Redis(host=settings.REDIS['HOST'],
#                                            port=settings.REDIS['PORT'],
#                                            db=settings.REDIS['DB'],
#                                            password=settings.REDIS['PASSWORD'])
#                 redis_client.lpush('annex_data_message', json.dumps(serializers.OrderDetailSerializer(order, context={'request': self.request}).data))
#                 return Response(serializers.OrderDetailSerializer(order, context={'request': self.request}).data)
#             else:
#                 transferdiscount_fields = [f.name for f in Transferdiscount._meta.get_fields() if f.name not in ['id', 'bill', 'drawer', 'bank']]
#                 transferdiscount_data = {field: data for (field, data) in self.request.data.items() if field in transferdiscount_fields}
#                 transferdiscount_data['bill_id'] = self.request.data.get('bill_id')
#                 transferdiscount_data['customer_id'] = self.request.data.get('customer_id')
#                 transferdiscount_data['bank_id'] = self.request.data.get('bank_id')
#                 if not order_object:
#                     transferdiscount = Transferdiscount.objects.create_transferdiscount(request, **transferdiscount_data)
#                 else:
#                     transferdiscount = Transferdiscount.objects.update_transferdiscount(order_object.object_id, **transferdiscount_data)
#                 order = self.create_order_object(transferdiscount, order_object)
#                 if not order:
#                     return ResponseBadRequest('请先确认所在单位以及流程都配置正确')
#                 return Response(serializers.OrderDetailSerializer(order, context={'request': self.request}).data)
#         except Exception as e:
#             traceback.print_exc(5)
#             return ResponseBadRequest('{}'.format(e))
#
#     def create_order_object(self, obj, order_object=None):
#         order_fields = [f.name for f in Order._meta.get_fields() if f.name != 'id']
#         order_data = {field: data for (field, data) in self.request.data.items() if field in order_fields}
#         submit_type = int(self.request.data.get('submit_type', 1))
#         if self.request.data.get('object_type') == 'c':
#             order_data['type'] = 'c'
#             order_data['flow_node'] = 0 if submit_type != 1 else 1
#         elif self.request.data.get('object_type') == 'b':
#             order_data['type'] = 'b'
#             order_data['flow_node'] = 0
#         else:
#             order_data['type'] = 't'
#             order_data['flow_node'] = 0 if submit_type != 1 else 1
#         order_data['object_id'] = obj.id
#         order_data['remark'] = self.request.data.get('order_remark', '')
#         user_orgiztion_list = self.request.user.organization.all()
#         if len(user_orgiztion_list) < 1:
#             return None
#         else:
#             flow_obj = VettingFlow.objects.filter(organization=user_orgiztion_list[0], type=self.request.data.get('object_type'))
#             if len(flow_obj) < 1:
#                 return None
#             order_data['flow'] = flow_obj[0].id
#             if not order_object:
#                 order = Order.objects.create_order(self.request, **order_data)
#             else:
#                 order = Order.objects.update_order(order_object.id, **order_data)
#             vetting_nodes = VettingNode.objects.filter(vetting_process=order.flow).order_by('ording')
#             if submit_type == 1:
#                 if self.request.data.get('object_type') in ['c', 't']:
#                     order.cur_approver = vetting_nodes[0].approver.id
#                     order.submit()
#                 else:
#                     order.contract_create(4)
#         order.save()
#         return order
#
#     def clear_customer_relation(self, order_object):
#         customer_obj = get_object_or_none(Customer, using='default', pk=order_object.object_id)
#         for contact in customer_obj.contacts.all():
#             contact.delete()
#         for payment_account in customer_obj.payments.all():
#             payment_account.delete()
#         customer_obj.contacts.clear()
#         customer_obj.payments.clear()
#
#     def get_contact_list(self, contact_fields, contacts=[]):
#         contact_list = []
#         for contact in contacts:
#             contact_data = {field: data for (field, data) in contact.items() if field in contact_fields}
#             contact = Contact.objects.create_contact(self.request, **contact_data)
#             contact_list.append(contact.id)
#         return contact_list
#
#     def get_payment_list(self, payment_fields, payments=[]):
#         payment_list = []
#         for payment_account in payments:
#             payment_data = {field: data for (field, data) in payment_account.items() if field in payment_fields}
#             payment_data['name'] = self.request.data.get('name')
#             payment = PaymentAccount.objects.create_payment(self.request, **payment_data)
#             payment_list.append(payment.id)
#         return payment_list
#
#
# class BillList(APIView):
#
#     def get(self, request, *args, **kwargs):
#         bill_list = Bill.objects.filter(user_id__in=get_user_list(request), status=3)
#         bill_data = [serializers.BillDetailSerializer(item).data for item in bill_list]
#         return Response(get_result(len(bill_data), bill_data))
#
#
# class BillDetail(generics.RetrieveAPIView):
#     serializer_class = serializers.BillDetailSerializer
#     queryset = Bill.objects.all()
#
#
# class BankList(APIView):
#
#     def get(self, request, *args, **kwargs):
#         bank_list = Bank.objects.filter(user_id__in=get_user_list(request))
#         bank_data = [serializers.BankListSerializer(item).data for item in bank_list]
#         return Response(get_result(len(bank_data), bank_data))
#
#
# class OrderDetail(generics.RetrieveDestroyAPIView):
#     serializer_class = serializers.OrderDetailSerializer
#     queryset = Order.objects.all()
#
#     def perform_destroy(self, instance):
#         self.clear_customer_relation(instance)
#         instance.delete()
#
#     def clear_customer_relation(self, order_object):
#         customer_obj = get_object_or_none(Customer, using='default', pk=order_object.object_id)
#         for contact in customer_obj.contacts.all():
#             contact.delete()
#         for payment_account in customer_obj.payments.all():
#             payment_account.delete()
#         customer_obj.contacts.clear()
#         customer_obj.payments.clear()
#
#
# class OrderApproved(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=kwargs.get('pk'))
#         order_obj = order_approved(order_obj, self.request, taget=1)
#         return Response(serializers.OrderDetailSerializer(order_obj, context={'request': self.request}).data)
#
#
# class OrderUnApproved(APIView):
#     serializer_class = serializers.OrderListSerializer
#     queryset = Order.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=kwargs.get('pk'))
#         vetting_node = get_object_or_none(VettingNode, using='default', vetting_process=order_obj.flow, ording=order_obj.flow_node)
#         vetting_nodes = VettingNode.objects.filter(vetting_process=order_obj.flow).order_by('ording')
#         if vetting_node:
#             if vetting_node.approver != self.request.user:
#                 raise exceptions.PermissionDenied
#             if order_obj.state in [2, 3]:
#                 raise exceptions.PermissionDenied
#             if vetting_node.return_node == 1:
#                 order_obj.unapproved(3)
#             else:
#                 order_obj.unapproved(1)
#                 order_obj.flow_node = vetting_node.return_node
#                 order_obj.cur_approver = vetting_nodes[vetting_node.return_node - 1].approver.id
#                 if vetting_node.return_node <= 5:  # 放款申请审核失败.
#                     for item in LoanApply.objects.filter(bill_id=order_obj.object_id):  # 删除掉审核失败的申请单.
#                         item.delete()
#             remark = self.request.data.get('remark', '')
#             order_obj.save()
#             VettingDiary(process_name=vetting_node.name,
#                          order_id=order_obj.id,
#                          vetting_result=-1,
#                          remark=remark,
#                          user_id=self.request.user.id,
#                          username=self.request.user.username).save()
#             title = "{}操作通知".format(vetting_node.vetting_process.name)
#             content = "{}业务申请单{}在{}审批未通过，请及时查看处理。".format(vetting_node.vetting_process.name, order_obj.code, vetting_node.name)
#             Notification(user_id=order_obj.user_id,
#                          title=title,
#                          content=content,
#                          order_id=order_obj.id).save()
#             node_user = get_object_or_none(get_user_model(), using='default', id=order_obj.user_id)
#             if node_user:
#                 PushWechatMessage().send_message(node_user.social_user_id, title, content, order_obj.id)
#             return Response(serializers.OrderDetailSerializer(order_obj, context={'request': self.request}).data)
#         else:
#             return ResponseBadRequest('节点错误')
#
#
# class ContractCreate(generics.CreateAPIView):
#     serializer_class = serializers.ContractDetailSerializer
#
#     def get_queryset(self):
#         return Contract.objects.filter(user_id__in=get_user_list(self.request))
#
#     def create(self, request, *args, **kwargs):
#         if not is_offce(request):
#             raise exceptions.PermissionDenied
#         serializer = serializers.ContractListSerializer(data=request.data)  # self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         contract_obj = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializers.ContractDetailSerializer(contract_obj).data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user.id,
#                         username=self.request.user.username,
#                         user_image_urls=self.request.user.image_urls)
#         buyers = self.request.data.get('buyers', []) if isinstance(self.request.data.get('buyers', []), list) else json.loads(self.request.data.get('buyers', []))
#         contract_obj = Contract.objects.get(pk=serializer.data.get('id'))
#         for buyer in buyers:
#             buyer_fields = [f.name for f in Buyer._meta.get_fields() if f.name != 'id']
#             buyer_data = {field: data for (field, data) in buyer.items() if field in buyer_fields}
#             buyer_object = Buyer.objects.create_buyer(self.request, **buyer_data)
#             contract_obj.buyers.add(buyer_object)
#         return contract_obj
#
#
# class OrderContractCreate(generics.CreateAPIView):
#     serializer_class = serializers.OrderDetailSerializer
#     queryset = Order.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         if not is_offce(request):
#             raise exceptions.PermissionDenied
#         if self.request.data.get('contract_number', '') == '':
#             raise BaseExceptions('保理合同编号不能为空')
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         bill_object = get_object_or_none(Bill, using='default', pk=order_obj.object_id)
#         bill_object.contract_number = self.request.data.get('contract_number')
#         bill_object.save()
#         vetting_nodes = VettingNode.objects.filter(vetting_process=order_obj.flow).order_by('ording')
#         order_obj.approved(1)
#         order_obj.flow_node = 1
#         order_obj.cur_approver = vetting_nodes[0].approver.id
#         order_obj.save()
#         VettingDiary(process_name='填写保理合同',
#                      order_id=order_obj.id,
#                      vetting_result=1,
#                      remark=self.request.data.get('remark', ''),
#                      user_id=self.request.user.id,
#                      username=self.request.user.username).save()
#         redis_client = redis.Redis(host=settings.REDIS['HOST'],
#                                    port=settings.REDIS['PORT'],
#                                    db=settings.REDIS['DB'],
#                                    password=settings.REDIS['PASSWORD'])
#         redis_client.lpush('annex_data_message', json.dumps(serializers.OrderDetailSerializer(order_obj, context={'request': self.request}).data))
#         return Response(serializers.OrderDetailSerializer(order_obj, context={'request': self.request}).data)
#
#
# class OrderLoanApplyCreate(generics.CreateAPIView):
#     serializer_class = serializers.LoanApplyDetailSerializer
#     queryset = LoanApply.objects.all()
#
#     def perform_create(self, serializer):
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         if not order_obj:
#             raise exceptions.NotFound
#         serializer.save(bill_id=order_obj.object_id,
#                         user_id=self.request.user.id,
#                         username=self.request.user.username,
#                         user_image_urls=self.request.user.image_urls)
#         order_obj = order_approved(order_obj, self.request, 7)
#
#
# class OrderCheckCreate(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         if not order_obj:
#             raise exceptions.NotFound
#         order_obj = order_approved(order_obj, self.request, 8)
#         return Response({'status': 'success'})
#
#
# class OrderLoanConfirm(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         if not order_obj:
#             raise exceptions.NotFound
#         order_obj = order_approved(order_obj, self.request, 9)
#         return Response({'status': 'success'})
#
#
# class OrderLoanManager(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         if not order_obj:
#             raise exceptions.NotFound
#         order_obj = order_approved(order_obj, self.request, 10)
#         return Response({'status': 'success'})
#
#
# class OrderArchivesManager(APIView):
#
#     def post(self, request, *args, **kwargs):
#         order_obj = get_object_or_none(Order, using='default', pk=get_pk_int(self))
#         if not order_obj:
#             raise exceptions.NotFound
#         order_obj = order_approved(order_obj, self.request, 11)
#         return Response({'status': 'success'})
#
#
# class CustomerList(generics.ListAPIView):
#     serializer_class = serializers.CustomerListSerializer
#
#     def get_queryset(self):
#         if self.request.GET.get('type') == 's':
#             return Customer.objects.filter(user_id__in=get_user_list(self.request), type='seller', is_active=True)
#         elif self.request.GET.get('type') == 'b':
#             return Customer.objects.filter(user_id__in=get_user_list(self.request), type='buyer', is_active=True)
#         else:
#             return Customer.objects.filter(user_id__in=get_user_list(self.request), is_active=True)
#
#
# class CustomerDetail(generics.RetrieveAPIView):
#     serializer_class = serializers.CustomerDetailSerializer
#     queryset = Customer.objects.all()
#
#
# class CustomerAccountList(generics.ListAPIView):
#     serializer_class = serializers.PaymentDetailSerializer
#
#     def get_queryset(self):
#         customer_obj = get_object_or_none(Customer, using='default', pk=get_pk_int(self))
#         if customer_obj:
#             return customer_obj.payments.all()
#         return []
#
#
# class CustomerContractList(generics.ListAPIView):
#     serializer_class = serializers.ContractDetailSerializer
#
#     def get_queryset(self):
#         return Contract.objects.filter(seller_id=get_pk_int(self))
#
#     def list(self, request, *args, **kwargs):
#         queryset = super(CustomerContractList, self).list(request, *args, **kwargs)
#         seller_obj = get_object_or_none(Customer, using='default', pk=get_pk_int(self))
#         if not seller_obj:
#             raise exceptions.NotFound
#         queryset.data['seller'] = serializers.CustomerListSerializer(seller_obj).data
#         return Response(queryset.data)
#
#
# class PaymentAccountList(generics.ListAPIView):
#     serializer_class = serializers.PaymentDetailSerializer
#
#     def get_queryset(self):
#         return PaymentAccount.objects.filter(user_id__in=get_user_list(self.request))
#
#
# class OrderUploadMaterial(PutToPatchApiViewMixin, APIView):
#
#     def patch(self, request, *args, **kwargs):
#         if self.request.data.get('discount_agreement_image_url', '') == '':
#             raise BaseExceptions('请传入贴现总协议资料')
#         order_obj = get_object_or_none(Order, using='default', pk=kwargs.get('pk'))
#         if not order_obj:
#             raise exceptions.NotFound
#         if order_obj.type != 'b':
#             return ResponseBadRequest('类型错误')
#         bill_obj = get_object_or_none(Bill, using='default', pk=order_obj.object_id)
#         if not bill_obj:
#             raise exceptions.NotFound
#         bill_fields = [f.name for f in Bill._meta.get_fields() if f.name != 'id']
#         bill_data = {field: data for (field, data) in self.request.data.items() if field in bill_fields}
#         Bill.objects.update_bill(bill_obj.id, **bill_data)
#         order_obj = order_approved(order_obj, self.request, 7)
#         return Response(serializers.OrderDetailSerializer(order_obj, context={'request': self.request}).data)
