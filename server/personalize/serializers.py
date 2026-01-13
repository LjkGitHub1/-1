from rest_framework import serializers
from common.core.serializers import BaseModelSerializer
from common.fields.utils import input_wrapper
from personalize import models
from system.models import UserInfo


class AssessmentReportSerializer(BaseModelSerializer):
    class Meta:
        model = models.AssessmentReport
        # 包含pk用于删除/更新，包含所有业务字段及审计字段
        fields = [
            'pk', 'report_no', 'assess_type', 'assess_date', 'multimodal_data', 'core_conclusion',
            'risk_level', 'report_status', 'user', 'assessor', 'created_time', 'updated_time'
        ]
        # 前端表格展示字段（控制显示顺序和范围）
        table_fields = [
            'pk', 'report_no', 'assess_type', 'assess_date', 'user', 'assessor',
            'risk_level', 'report_status', 'created_time'
        ]
        # 字段额外参数（关联字段渲染、只读控制）
        extra_kwargs = {
            'pk': {'read_only': True},
            'report_no': {'read_only': True},  # 编号自动生成，前端不可编辑
            'user': {
                'attrs': ['pk', 'username'], 'required': True, 'format': "{username}({pk})",
                'input_type': 'api-search-user'  # 前端用用户搜索组件
            },
            'assessor': {
                'attrs': ['pk', 'username'], 'required': True, 'format': "{username}({pk})",
                'input_type': 'api-search-user'
            }
        }

    # 自定义字段：风险等级文本展示（只读）
    # risk_level_text = input_wrapper(serializers.SerializerMethodField)(read_only=True, input_type='text', label="风险等级")

    def get_risk_level_text(self, obj):
        return obj.get_risk_level_display()

    # 自动生成报告编号（创建时触发）
    def create(self, validated_data):
        from datetime import datetime
        import random
        date_str = datetime.now().strftime("%Y%m%d")
        random_str = f"{random.randint(100, 999)}"
        validated_data['report_no'] = f"REP{date_str}{random_str}"
        return super().create(validated_data)


class InterventionPlanSerializer(BaseModelSerializer):
    class Meta:
        model = models.InterventionPlan
        fields = [
            'pk', 'plan_no', 'plan_title', 'intervention_type', 'target_issue',
            'specific_measures', 'expected_effect', 'start_date', 'end_date',
            'plan_status', 'user', 'planner', 'report', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'plan_no', 'plan_title', 'intervention_type', 'start_date',
            'end_date', 'plan_status', 'user', 'report', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'plan_no': {'read_only': True},
            'user': {
                'attrs': ['pk', 'username'], 'required': True, 'format': "{username}({pk})",
                'input_type': 'api-search-user'
            },
            'planner': {
                'attrs': ['pk', 'username'], 'required': True, 'format': "{username}({pk})",
                'input_type': 'api-search-user'
            },
            'report': {
                'attrs': ['pk', 'report_no'], 'required': True, 'format': "{report_no}({pk})",
                'input_type': 'api-search-report'  # 自定义报告搜索组件
            }
        }

    # 自定义字段：方案状态文本
    # plan_status_text = input_wrapper(serializers.SerializerMethodField)(read_only=True, input_type='text', label="方案状态")

    def get_plan_status_text(self, obj):
        return obj.get_plan_status_display()

    # 自动生成方案编号
    def create(self, validated_data):
        from datetime import datetime
        import random
        date_str = datetime.now().strftime("%Y%m%d")
        random_str = f"{random.randint(100, 999)}"
        validated_data['plan_no'] = f"PLN{date_str}{random_str}"
        return super().create(validated_data)