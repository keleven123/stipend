# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from rest_framework import serializers
from myapp.handler import APIResponse
from myapp.models import StudentApplication
from myapp.serializers import StudentApplicationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json


@api_view(['GET'])
def generate_poem(request):
    # 读取 StudentApplication 表格里的内容
    students = StudentApplication.objects.all()
    student_info = "\n".join([
        f"姓名: {student.name}, "
        f"性别: {student.gender}, "
        f"学号: {student.student_id}, "
        f"联系方式: {student.contact}, "
        f"政治面貌: {student.political_status}, "
        f"社会实践经历: {student.social_practice}, "
        f"家庭成员信息: {student.family_members}, "
        f"家庭年收入: {student.family_annual_income}, "
        f"经济来源: {student.income_source}, "
        f"家庭负债情况: {student.family_debt}, "
        f"家庭成员健康状况: {student.family_health}, "
        f"是否享受低保: {student.is_low_income}, "
        f"其他补助: {student.subsidies}, "
        f"突发性经济困难说明: {student.emergency_situation}, "
        f"学业成绩/GPA: {student.academic_performance}, "
        f"申请理由与用途说明: {student.application_reason}, "
        f"创建时间: {student.created_at}, "
        f"更新时间: {student.updated_at}"
        for student in students
    ])

    client = OpenAI(
        base_url="https://api.deepseek.com/",
        api_key="sk-618db245e0b8410a819127f115534dfb"
    )

    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{
            "role": "user",
            "content": f"""
                        请严格按以下要求处理学生数据：
                        1. 分析以下学生信息，筛选需要资助的学生，并尽快返回结果。
                        2. 必须返回严格的标准JSON格式
                        3. JSON结构包含两个数组：selected（选中）和unselected（未选中）
                        4. 每个学生对象包含 name、student_id、contact、value字段
                        5. 不要包含任何额外说明或格式化符号
                        6. 确保JSON语法正确，键名使用英文双引号
                        7.请你计算出VALUE的值，VALUE = (家庭负债 / 家庭年收入)*100，高于50则selected（选中），低于50为unselected（未选中），并由高到低排列。

                        示例正确格式：
                        {{
                            "selected": [
                                {{"name": "张三", "student_id": "2020001", "contact": "13800138000","value":"0.4"}}
                            ],
                            "unselected": []
                        }}

                        学生数据：
                        {student_info}
                        """
        }]
    )

    # 打印原始响应用于调试
    raw_response = completion.choices[0].message.content
    print("[DEBUG] 原始API响应:", raw_response)  # 重要调试信息

    # 处理可能存在的代码块包裹
    if '```json' in raw_response:
        clean_response = raw_response.split('```json')[1].split('```')[0]
    elif '```' in raw_response:
        clean_response = raw_response.split('```')[1]
    else:
        clean_response = raw_response

    # 严格验证JSON格式
    try:
        result = json.loads(clean_response)

        # 验证数据结构
        if not all(key in result for key in ["selected", "unselected"]):
            raise ValueError("JSON结构缺少必要字段")

        for student in result["selected"] + result["unselected"]:
            if not all(field in student for field in ["name", "student_id", "contact", "value"]):
                raise ValueError("学生对象字段缺失")

    except (json.JSONDecodeError, ValueError) as e:
        print("[ERROR] JSON解析失败:", str(e))
        return Response({
            "error": "返回数据结构异常",
            "debug_info": {
                "raw_response": raw_response,
                "clean_response": clean_response,
                "error": str(e)
            }
        }, status=500)

    return APIResponse(
        code=0,
        msg='申请提交成功',
        data=result,
    )

# client = OpenAI(
#     base_url="https://api.deepseek.com/",
#     api_key="<YOUR_API_KEY>"
# )
#
# completion = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {
#                 "role": "user",
#                 "content": "模仿李白的风格写一首七律.飞机"
#         }
#     ]
# )
#
# print(completion.choices[0].message.content)
#
# def generate_poem(request):
#     if request.method == 'POST':
#         # 获取用户输入的内容
#         user_input = request.POST.get('content', '')
#
#         # 调用 OpenAI API
#         client = OpenAI(
#             base_url="https://api.deepseek.com/",
#             api_key="<YOUR_API_KEY>"
#         )
#
#         completion = client.chat.completions.create(
#             model="deepseek-chat",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": user_input
#                 }
#             ]
#         )
#
#         # 提取 OpenAI 的响应内容
#         poem = completion.choices[0].message.content
#
#         # 返回结果给网页
#         return JsonResponse({'poem': poem})
#     else:
#         # 如果是 GET 请求，返回包含输入框的页面
#         return render(request, 'generate_poem.html')


# def generate_poem(request):
#     if request.method == 'POST':
#         # 读取 StudentApplication 表格里的内容
#         students = StudentApplication.objects.all()
#         student_info = "\n".join([
#             f"姓名: {student.name}, 学号: {student.student_id}, 联系方式: {student.contact}"
#             for student in students
#         ])
#
#         # 调用 OpenAI API
#         client = OpenAI(
#             base_url="https://api.deepseek.com/",
#             api_key="<YOUR_API_KEY>"
#         )
#
#         completion = client.chat.completions.create(
#             model="deepseek-chat",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": f"根据以下学生信息，模仿李白的风格写一首七律:\n{student_info}"
#                 }
#             ]
#         )
#
#         # 提取 OpenAI 的响应内容
#         poem = completion.choices[0].message.content
#
#         # 返回结果给网页
#         return JsonResponse({'poem': poem})
#     else:
#         # 如果是 GET 请求，返回包含输入框的页面
#         return render(request, 'generate_poem.html')
