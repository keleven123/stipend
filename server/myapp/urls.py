from django.urls import path

from myapp import views

app_name = 'myapp'
urlpatterns = [
    # api
    path('admin/zxsubmit/create', views.admin.zxsubmit.create),
    path('admin/zxsubmit/application_detail', views.admin.zxsubmit.application_detail),
    path('admin/zxsubmit/delete', views.admin.zxsubmit.delete),
    path('admin/zxsubmit/list', views.admin.zxsubmit.list_api),
    path('admin/zxsubmit/update', views.admin.zxsubmit.update),
    path('admin/zxsubmit/suanfa', views.admin.suanfa.generate_poem),
    path('admin/overview/count', views.admin.overview.count),
    path('admin/overview/sysInfo', views.admin.overview.sysInfo),
    path('admin/thing/detail', views.admin.thing.detail),
    path('admin/thing/create', views.admin.thing.create),
    path('admin/thing/update', views.admin.thing.update),
    path('admin/thing/delete', views.admin.thing.delete),
    path('admin/loginLog/list', views.admin.loginLog.list_api),
    path('admin/loginLog/create', views.admin.loginLog.create),
    path('admin/loginLog/update', views.admin.loginLog.update),
    path('admin/loginLog/delete', views.admin.loginLog.delete),
    path('admin/opLog/list', views.admin.opLog.list_api),
    path('admin/errorLog/list', views.admin.errorLog.list_api),
    path('admin/user/list', views.admin.user.list_api),
    path('admin/user/create', views.admin.user.create),
    path('admin/user/update', views.admin.user.update),
    path('admin/user/updatePwd', views.admin.user.updatePwd),
    path('admin/user/delete', views.admin.user.delete),
    path('admin/user/info', views.admin.user.info),
    path('admin/adminLogin', views.admin.user.admin_login),
]