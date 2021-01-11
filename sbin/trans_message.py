import datetime
import time


def unixtime_to_datetime(local_time):
    date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(local_time))
    date_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date_time


class TransMessage():
    def __init__(self, data, app_name, test_env):
        self.data = data
        self.app_name = app_name
        if test_env:
            self.BASE_URL = 'http://test.cmcaifu.com'
        else:
            self.BASE_URL = 'https://www.cmcaifu.com'

    def trans_message(self):
        template_id = int(self.data.get('template_id'))
        if template_id == 1:
            return self.get_payment_succ()
        elif template_id == 3:
            return self.get_withdraw_succ()
        elif template_id == 4:
            return self.get_withdraw_fail()
        elif template_id == 5:
            return self.get_kaihu_succ()
        elif template_id == 6:
            return self.get_bind_succ()
        elif template_id == 7:
            return self.get_dongjie_message()
        elif template_id == 8:
            return self.get_full_bill_message()
        elif template_id == 9:
            return self.get_bill_fail_message()
        elif template_id == 10:
            return self.get_repayment_succ()
        elif template_id == 11:
            return self.get_cm_refund()  # 超募退款.
        elif template_id == 12:
            return self.get_register_code()
        elif template_id == 13:
            return self.get_vip_code()
        elif template_id == 14:
            return self.get_zst_code()
        elif template_id == 15:
            return self.get_xz_register_code()  # 血族注册.
        elif template_id == 16:
            return self.get_xz_tz_code()  # 血族渠道投资返现.
        elif template_id == 17:
            return self.get_not_xz_tz_code()  # 非血族渠道投资返现.
        elif template_id == 18:
            return self.get_kh_tz_code()  # 非血族渠道投资返现.
        elif template_id == 19:
            return self.get_dq_tz_code()  # 到期提醒.
        elif template_id == 20:
            return self.get_yx_code()
        elif template_id == 21:
            return self.get_zr_sq()  # 发起转让申请.
        elif template_id == 22:
            return self.get_zr_cs()  # 转让申请超时.
        elif template_id == 23:
            return self.get_zr_succ()  # 转让成功.
        elif template_id == 24:
            return self.get_pay_zr_succ()  # 购买债转成功.
        elif template_id == 25:
            return self.get_zq_cm_refund()  # 购买债权超募退款通知.
        else:
            return self.get_template_message()

    def get_payment_succ(self):
        title = '充值成功通知'
        url = self.get_url('transactions')
        content = '您于{}发起的{}元人民币的充值业务已受理成功，当前账户余额:{}元。 '.format(self.data.get('date'), self.data.get('amount', 0) / 100, self.data.get('balance', 0) / 100)
        return self.get_message_dict(title, content, url)

    def get_withdraw_succ(self):
        title = '提现成功通知'
        url = self.get_url('transactions')
        content = '您于{}申请的{}元人民币的提现业务已受理成功，资金到账时间为受理成功日（不含当日）起两个工作日内，请注意查收。'.format(self.data.get('date'), self.data.get('amount', 0) / 100)
        return self.get_message_dict(title, content, url)

    def get_withdraw_fail(self):
        title = '提现失败通知'
        content = '您于{}申请的{}元人民币的提现业务已受理失败。'.format(self.data.get('date'), self.data.get('amount', 0) / 100)
        return self.get_message_dict(title, content)

    def get_kaihu_succ(self):
        title = '中金开户成功通知'
        content = '您于{}在中金支付成功开户'.format(self.data.get('date'))
        return self.get_message_dict(title, content)

    def get_bind_succ(self):
        title = '中金绑卡成功通知'
        content = '您于{}在中金支付绑卡成功'.format(self.data.get('date'))
        return self.get_message_dict(title, content)

    def get_dongjie_message(self):
        title = '投标冻结资金通知'
        url = self.get_url('investments')
        content = '您向“{}”产品投资的 {}元资金已被冻结。产品募集成功后将自动划转至融资方账户并开始计息'.format(self.data.get('product_name'), self.data.get('amount', 0) / 100)
        return self.get_message_dict(title, content, url)

    def get_full_bill_message(self):
        title = '投资满标通知'
        url = self.get_url('investments')
        content = '您投资{}元的“{}”产品已成功满标，将于{}开始计息。'.format(self.data.get('amount', 0) / 100, self.data.get('product_name'), self.data.get('date', ''))
        return self.get_message_dict(title, content, url)

    def get_bill_fail_message(self):
        title = '投资流标通知'
        url = self.get_url('investments')
        content = '我们非常抱歉的通知您，您投资的“{}”产品由于募集金额不足已流标，您投资的 {}元款项已返还至您的账户。 我们对由此造成的不便深表歉意。'.format(self.data.get('product_name'), self.data.get('amount', 0) / 100)
        return self.get_message_dict(title, content, url)

    def get_repayment_succ(self):
        title = '投资还款通知'
        url = self.get_url('investments')
        content = '您所投资“{}”产品的还款{}已转入您的账户，请注意查收。'.format(self.data.get('product_name'), self.data.get('amount', 0) / 100)
        return self.get_message_dict(title, content, url)

    def get_cm_refund(self):
        title = '超募退款通知'
        content = '您向{}产品投资的{}元资金，由于多人同时投资导致了超募的情况，您的认购资金中{}元已投资生效，剩余{}元已自动退款至您的账户余额中。'.format(self.data.get('product_name'), self.data.get('amount', 0) / 100, self.data.get('real_deal_amount') / 100, self.data.get('refund_amount') / 100)
        return self.get_message_dict(title, content, '')

    def get_register_code(self):
        title = '兑换码领取通知'
        content = '您已成功获取法宝网"注册邀请码"一枚：{},请及时去法宝网注册 www.ifabao.com.'.format(self.data.get('code', ''))
        return self.get_message_dict(title, content, '')

    def get_vip_code(self):
        title = '兑换码领取通知'
        content = '您已成功获取法宝网"VIP抵价券"一枚：{}，请及时去论坛内领奖兑换。'.format(self.data.get('code', ''))
        return self.get_message_dict(title, content, '')

    def get_zst_code(self):
        title = '兑换码领取通知'
        content = '您已成功获取{}"兑换码"一枚：{}。'.format(self.data.get('product_name', ''), self.data.get('code', ''))
        return self.get_message_dict(title, content, '')

    def get_xz_register_code(self):
        title = '血族注册开户返现通知'
        content = '您已成功开户并获得返现{}元。还有一大波返现活动正在进行，快来投资吧!'.format(self.data.get('amount', 0) / 100)
        url = self.get_url(self.BASE_URL + '/activities/101/', True)
        return self.get_message_dict(title, content, url)

    def get_xz_tz_code(self):
        title = '投资返现通知'
        content = '您已累计投资满{}元，获得奖励返现{}元。'.format(self.data.get('total_amount', 0) / 100, self.data.get('amount', 0) / 100)
        url = self.get_url(self.BASE_URL + '/activities/101/', True)
        return self.get_message_dict(title, content, url)

    def get_not_xz_tz_code(self):
        title = '投资返礼包通知'
        content = '您已成功获取"{}"，兑换码为：{}。'.format(self.data.get('product_name', ''), self.data.get('code'))
        return self.get_message_dict(title, content, '')

    def get_kh_tz_code(self):
        title = '开户返现通知'
        content = '您已成功开户并获得返现{}元。还有一大波活动正在进行，快来投资吧！'.format(self.data.get('amount', 0) / 100)
        url = 'mm://transactions'
        return self.get_message_dict(title, content, url)

    def get_dq_tz_code(self):
        title = '到期提醒'
        content = '您有{}即将到期，请尽快使用。'.format(self.data.get('prize', ''))
        return self.get_message_dict(title, content, '')

    def get_yx_code(self):
        title = '奖励通知'
        content = '您成功找回了金币，完成“疯狂的小鸟挑战”，获得国王的奖励"{}"'.format(self.data.get('prize', ''))
        return self.get_message_dict(title, content, '')

    def get_zr_sq(self):
        title = '债权转让申请发起通知'
        content = '您已经成功发起{}转让，本次转让本金{}元，转让价格{}元，募集截止时间为{}，超时系统将自动撤销转让。'.format(self.data.get('product_name', ''), self.data.get('original_principal', 0) / 100, self.data.get('gross', 0) / 100, self.data.get('close_time'))
        return self.get_message_dict(title, content, '')

    def get_zr_cs(self):
        title = '债权转让申请超时通知'
        content = '您对{}的转让申请超过募集截止时间，系统已自动撤销，请重新发起转让。'.format(self.data.get('product_name', ''))
        return self.get_message_dict(title, content, '')

    def get_zr_succ(self):
        title = '债权转让成功通知'
        content = '您申请的{}已经转让成功！本次转让本金{}元，转让价格{}元，已转{}元，扣除服务费{}元，实际到账{}元。'.format(self.data.get('product_name'), self.data.get('traded_principal', 0) / 100, self.data.get('gross', 0) / 100, self.data.get('traded_gross', 0) / 100, self.data.get('service_charge', 0) / 100, self.data.get('real_amount', 0) / 100)
        return self.get_message_dict(title, content, '')

    def get_pay_zr_succ(self):
        title = '购买债转成功通知'
        content = '恭喜您于{}成功购买债权转让产品{}，购买金额{}元，相对预期年化{}%。'.format(self.data.get('created_time'), self.data.get('product_name'), self.data.get('gross', 0) / 100, self.data.get('relative_rate', 0) / 100)
        return self.get_message_dict(title, content, '')

    def get_zq_cm_refund(self):
        title = '债权超募通知'
        content = '您投资的{}债权产品，由于多人同时投资导致了超募的情况， {}元已自动退款至您的账户余额中。'.format(self.data.get('product_name', ''), self.data.get('refund', 0) / 100)
        return self.get_message_dict(title, content, '')

    def get_template_message(self):
        title = '奖励通知'
        content = '您已成功参加 "{}"，获得奖励："{}"。'.format(self.data.get('activity', ''), self.data.get('prize', ''))
        return self.get_message_dict(title, content, '')

    def get_message_dict(self, title, content, url=''):
        created_time = self.data.get('handled_time', 0)
        if created_time != 0:
            created_time -= 8 * 60 * 60
        notify_data = {'title': title,
                       'content': content,
                       'id_str': self.data.get('id_str', 0),
                       'id': int(self.data.get('id_str', 0)),
                       'url': url,
                       'created_time': unixtime_to_datetime(created_time)}
        return notify_data

    def get_url(self, url, full=False):
        if 'http://' in url or 'https://' in url:
            return url
        if self.app_name == 'mm':
            return 'mm://{}'.format(url)
        else:
            if not full:
                return self.BASE_URL + '/accounts/{}'.format(url)
            return self.BASE_URL + url
