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

from myapp.views.admin.shenpi import ScholarshipEvaluator


@api_view(['GET'])
def evaluate_scholarship(request):
    evaluator = ScholarshipEvaluator(year=2025)
    results = evaluator.evaluate_applications()

    # 生成结构化结果
    output = []
    for res in results:
        if not res['anomaly'] and res['score'] > 50:
            output.append({
                "姓名": res['student'].name,
                "学号": res['student'].student_id,
                "联系方式": res['student'].contact,
                "权重值": res['score'],
            })

    return APIResponse(
        msg='成功',
        data={
            'qualified_students': output,
            'evaluation_criteria': evaluator.weights
        }
    )