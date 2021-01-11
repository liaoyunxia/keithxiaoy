
class RequestUserMiddleware(object):
    """
    https://docs.djangoproject.com/en/dev/topics/http/middleware/#process-view
    https://github.com/transientskp/banana/blob/master/project/multidb.py
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.user.is_manager = self.is_manager(request)
        request.user.is_financier = self.is_financier(request)

    def is_manager(self, request):
        if not request.user.is_authenticated():
            return False
        group_name = [item.name for item in request.user.groups.all()]
        if '客户经理' in group_name:
            return True
        else:
            return False

    def is_financier(self, request):
        if not request.user.is_authenticated():
            return False
        group_name = [item.name for item in request.user.groups.all()]
        if '转贴人员' in group_name:
            return True
        else:
            return False
