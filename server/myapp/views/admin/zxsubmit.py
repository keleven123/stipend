from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes

from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import StudentApplication
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import StudentApplicationSerializer
from rest_framework import status

@api_view(['POST'])
def create(request):
    """
    创建新的助学金申请
    """
    # 反序列化请求数据
    serializer = StudentApplicationSerializer(data=request.data)

    # 验证数据有效性
    if serializer.is_valid():
        # 保存到数据库
        serializer.save()
        # 返回成功响应
        return APIResponse(
            code=0,
            msg='申请提交成功',
            data=serializer.data,
        )

    # 返回验证错误响应
    return APIResponse(
        code=1,
        msg='提交失败，请改正后再提交',
        data=serializer.errors,
    )


@api_view(['GET'])
def application_detail(request):
    """助学金申请查询接口"""
    try:
        # 获取请求参数（支持主键id或学号student_id查询）
        pk = request.GET.get('id')
        student_id = request.GET.get('student_id')

        # 参数校验
        if not pk and not student_id:
            return APIResponse(code=1, msg='必须提供id或student_id参数')

        # 优先使用主键查询
        if pk:
            application = StudentApplication.objects.get(pk=pk)
        else:
            application = StudentApplication.objects.get(student_id=student_id)

    except ValueError:
        return APIResponse(code=1, msg='参数格式错误')
    except StudentApplication.DoesNotExist:
        return APIResponse(code=1, msg='申请记录不存在')
    except Exception as e:
        return APIResponse(code=1, msg=f'服务器错误: {str(e)}')

    # 序列化数据
    serializer = StudentApplicationSerializer(StudentApplication)
    return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
def delete(request):

    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='学生账号无法进行此操作，请联系管理员')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        StudentApplication.objects.filter(id__in=ids_arr).delete()
    except StudentApplication.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')

@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        StudentApp = StudentApplication.objects.all().order_by('created_at')
        serializer = StudentApplicationSerializer(StudentApp, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):

    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='学生账号无法进行此操作，请联系管理员')

    try:
        pk = request.GET.get('id', -1)
        course = StudentApplication.objects.get(pk=pk)
    except StudentApplication.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = StudentApplicationSerializer(course, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='更新失败')