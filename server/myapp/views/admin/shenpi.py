from django.db.models.aggregates import Avg
from rest_framework.decorators import api_view, authentication_classes
import pandas as pd

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import StudentApplication, Score, LoginLog
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import StudentApplicationSerializer
from rest_framework import status






class ScholarshipEvaluator:
    def __init__(self, year):
        self.year = year
        self.weights = {
            'family': 0.35, # 家庭信息
            'consumption': 0.25, # 消费信息
            'academic': 0.2, # 学业信息
            'behavior': 0.15,# 行为信息
            'validation': 0.05# 真实性验证
        }

    def get_family_score(self, student):
        """家庭经济状况评分"""
        score = 0
        # 收入负债比计算
        try:
            income = float(student.family_annual_income)
            debt = float(student.family_debt) if student.family_debt else 0
            ratio = debt / (income + 1e-6)
            score += min(100, 100 * ratio)
        except:
            pass

        # 家庭健康情况评分
        health_deduction = {
            '重大疾病': 15,
            '慢性病': 8,
            '健康': 0
        }
        score += health_deduction.get(student.family_health, 0)
family_score = ratio + health_deduction
        return family_score

    class StudentAnalyzer:
        def __init__(self, consumption_file='student_shopping.csv'):
            self.consumption_df = pd.read_csv(consumption_file)
            self.consumption_df['date'] = pd.to_datetime(self.consumption_df['date'])

        def get_consumption_score(self, student):
            student_id = student.get_id()
            student_df = self.consumption_df[self.consumption_df['student_id'] == student_id]

            if student_df.empty:
                return 50

            # 基础指标
            total_amount = student_df['amount'].sum()

            # 日均消费
            dates = student_df['date']
            time_span = (dates.max() - dates.min()).days + 1
            daily_avg = total_amount / time_span if time_span > 0 else 0

            # 消费稳定性
            daily_spending = student_df.groupby('date')['amount'].sum()
            variance = daily_spending.var() if len(daily_spending) > 1 else 0

            # 高端消费
            high_end_threshold = 75
            high_end_ratio = student_df[student_df['amount'] > high_end_threshold][
                                 'amount'].sum() / total_amount if total_amount > 0 else 0

            # 恩格尔系数
            food_expense = student_df[student_df['category'] == '食堂']['amount'].sum()
            engel_coefficient = food_expense / total_amount if total_amount > 0 else 0

            # 指标标准化
            avg_score = max(0, 100 - abs(daily_avg - 40) * 1.5)
            var_score = max(0, 100 - variance ** 0.5 * 0.8)
            ratio_score = 100 - (high_end_ratio * 200)
            engel_score = 100 - (engel_coefficient * 125)  # 系数每增加1%扣1.25分

            # 加权评分
            shopping_score = (
                    avg_score * 0.4 +
                    var_score * 0.25 +
                    ratio_score * 0.2 +
                    engel_score * 0.15
            )

            return shopping_score

        def get_academic_score(self, student):
            try:
                gpa = float(student.academic_performance)
                return academic_score(100, gpa * 25)
            except:
                return 0

    class PovertyAnalyzer:
        def __init__(self, data_file):
            self.df = pd.read_csv(data_file)
            self.preprocess_data()

        def preprocess_data(self):
            """预处理时间数据并计算夜间宿舍停留时间"""
            # 转换日期时间格式
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df['entry_datetime'] = pd.to_datetime(self.df['date'].astype(str) + ' ' + self.df['entry_time'])
            self.df['exit_datetime'] = pd.to_datetime(self.df['date'].astype(str) + ' ' + self.df['exit_time'])

            # 处理跨天记录
            mask = self.df['exit_datetime'] < self.df['entry_datetime']
            self.df.loc[mask, 'exit_datetime'] += pd.Timedelta(days=1)

            # 计算夜间宿舍停留时间
            self.df['night_minutes'] = self.df.apply(self._calculate_night_minutes, axis=1)

        def _calculate_night_minutes(self, row):
            """计算22:00-06:00时段的夜间停留时间"""
            if row['location'] != '宿舍楼':
                return 0

            entry = row['entry_datetime']
            exit = row['exit_datetime']

            # 定义夜间时段
            night_start = entry.replace(hour=22, minute=0, second=0)
            night_end = entry.replace(hour=6, minute=0, second=0) + pd.Timedelta(days=1)

            # 调整时段边界
            if entry.hour < 6:
                night_start = entry.replace(hour=22, minute=0, second=0) - pd.Timedelta(days=1)
                night_end = entry.replace(hour=6, minute=0, second=0)
            elif 6 <= entry.hour < 22:
                night_end = night_start + pd.Timedelta(days=1)

            # 计算交集时间
            start = max(entry, night_start)
            end = min(exit, night_end)
            return (end - start).total_seconds() // 60 if start < end else 0

        def get_poverty_score(self, student_id):
            """综合计算贫困生评分（0-100）"""
            data = self.df[self.df['student_id'] == student_id]
            if data.empty:
                return 50  # 默认中间值

            # 学习相关指标
            library_data = data[data['location'] == '图书馆']
            total_study = library_data['duration_minutes'].sum()
            study_days = library_data['date'].nunique()
            holiday_study = library_data[library_data['is_holiday'] == '是'].shape[0]

            # 生活规律指标
            dorm_data = data[data['location'] == '宿舍楼']
            night_stay = dorm_data['night_minutes'].sum()
            daily_stay = dorm_data['duration_minutes'].sum() - night_stay

            # 计算评分（权重可调整）
            scores = {
                'study_time': min(total_study / 15, 100),  # 每15分钟1分
                'study_consistency': (study_days / 30) * 100,  # 每月30天基准
                'holiday_study': min(holiday_study * 30, 100),  # 每次30分
                'night_stay': min(night_stay / 4, 100),  # 每4分钟1分
                'daily_activity': 100 - min(daily_stay / 3, 100)  # 白天活动得分
            }

            # 加权计算总分
            action_scores = {
                'study_time': 0.35,
                'study_consistency': 0.2,
                'holiday_study': 0.15,
                'night_stay': 0.2,
                'daily_activity': 0.1
            }

            return action_scores

    def validate_application(self, student):
        """申请真实性验证"""
        try:
            consumption = self.get_consumption_score(student)
            reported_income = float(student.family_annual_income)
            daily_income = reported_income / 365
            expected_consumption = daily_income * 3
            discrepancy = abs(consumption - expected_consumption)
            # 根据差异值返回具体评分（示例逻辑）
            true_score = max(0, 100 - discrepancy)  # 差异越大分数越低
            return true_score
        except:
            return 50  # 默认安全分

    def calculate_total_score(self, student):
        """综合评分计算（带权重验证）"""
        # 获取各维度原始分数
        try:
            scores = {
                'family': self.get_family_score(student),  # 家庭经济分
                'consumption': self.get_consumption_score(student),  # 消费行为分
                'academic': self.get_academic_score(student),  # 学业表现分
                'behavior': self.get_behavior_score(student),  # 行为特征分
                'validation': self.validate_application(student)  # 真实性验证分
            }
        except Exception as e:
            # 记录错误日志
            print(f"评分计算错误: {str(e)}")
            return 0  # 返回最低分保护系统

        # 权重验证（确保权重和为1）
        if not round(sum(self.weights.values()), 2) == 1.0:
            raise ValueError("权重配置错误，权重总和必须为1")

        # 加权计算
        total_score = sum(
            scores[category] * weight
            for category, weight in self.weights.items()
        )

        #按降序排列
        return sorted(results, key=lambda x: x['score'], reverse=True)