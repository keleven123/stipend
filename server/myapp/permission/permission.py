from myapp.models import User


def isDemoAdminUser(request):
    adminToken = request.META.get("HTTP_ADMINTOKEN")
    users = User.objects.filter(admin_token=adminToken)
    if len(users) > 0:
        user = users[0]
        if user.role == '3':  # （角色3）表示学生帐号，权限低
            print('学生帐号===>')
            return True
    return False
