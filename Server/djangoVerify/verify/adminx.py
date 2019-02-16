#from django.contrib import admin
from verify.models import UserMessage
import xadmin
from  xadmin import views
class UserInfoAdmin(object):
    list_display = ('userId','userName', 'date','isVerified','remainder')


class GlobalSettings(object):
    """标题及版权修改"""
    site_title = "用户注册后台管理系统"
    site_footer = "你们公司自己名字"
xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(UserMessage,UserInfoAdmin)


