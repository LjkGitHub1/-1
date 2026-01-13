from django.db import models
from django.utils import timezone
from common.core.models import DbAuditModel
from system.models import UserInfo


class AssessmentReport(DbAuditModel):
    """评估报告模型"""
    class RiskLevelChoices(models.IntegerChoices):
        LOW = 1, "低"
        MEDIUM = 2, "中"
        HIGH = 3, "高"
    
    class StatusChoices(models.IntegerChoices):
        DRAFT = 1, "草稿"
        COMPLETED = 2, "已完成"
        ARCHIVED = 3, "已归档"

    # 关联关系
    user = models.ForeignKey(to=UserInfo, verbose_name="被评估人", on_delete=models.CASCADE, related_name="assessment_user")
    assessor = models.ForeignKey(to=UserInfo, verbose_name="评估人", on_delete=models.CASCADE, related_name="assessment_assessor")

    # 核心字段
    report_no = models.CharField(verbose_name="报告编号", max_length=32, unique=True)
    assess_type = models.CharField(verbose_name="评估类型", max_length=64, help_text="如：情绪测评、人格测评")
    assess_date = models.DateTimeField(verbose_name="评估日期", default=timezone.now)
    multimodal_data = models.JSONField(verbose_name="多模态数据", help_text="存储文本、语音等特征的JSON数据")
    core_conclusion = models.TextField(verbose_name="核心结论")
    risk_level = models.SmallIntegerField(choices=RiskLevelChoices, default=RiskLevelChoices.LOW, verbose_name="风险等级")
    report_status = models.SmallIntegerField(choices=StatusChoices, default=StatusChoices.DRAFT, verbose_name="报告状态")

    class Meta:
        verbose_name = "评估报告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.report_no}-{self.assess_type}"


class InterventionPlan(DbAuditModel):
    """干预方案模型"""
    class StatusChoices(models.IntegerChoices):
        PENDING = 1, "待执行"
        IN_PROGRESS = 2, "进行中"
        COMPLETED = 3, "已完成"

    # 关联关系
    user = models.ForeignKey(to=UserInfo, verbose_name="干预对象", on_delete=models.CASCADE, related_name="intervention_user")
    planner = models.ForeignKey(to=UserInfo, verbose_name="方案制定人", on_delete=models.CASCADE, related_name="intervention_planner")
    report = models.ForeignKey(to=AssessmentReport, verbose_name="关联评估报告", on_delete=models.CASCADE, related_name="intervention_report")

    # 核心字段
    plan_no = models.CharField(verbose_name="方案编号", max_length=32, unique=True)
    plan_title = models.CharField(verbose_name="方案标题", max_length=128)
    intervention_type = models.CharField(verbose_name="干预类型", max_length=64, help_text="如：认知行为疗法、正念训练")
    target_issue = models.TextField(verbose_name="核心问题", help_text="针对评估报告的问题描述")
    specific_measures = models.JSONField(verbose_name="具体措施", help_text="分阶段干预步骤的JSON数据")
    expected_effect = models.TextField(verbose_name="预期效果")
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    plan_status = models.SmallIntegerField(choices=StatusChoices, default=StatusChoices.PENDING, verbose_name="方案状态")

    class Meta:
        verbose_name = "干预方案"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.plan_no}-{self.plan_title}"