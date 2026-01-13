import decimal

import common.core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("system", "0003_userloginlog_channel_name_and_more"),
        ("smartDiagnose", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssessmentDataset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated time"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="数据集描述"
                    ),
                ),
                (
                    "dataset_name",
                    models.CharField(max_length=128, verbose_name="数据集名称"),
                ),
                (
                    "modalities",
                    models.JSONField(
                        default=list,
                        help_text="如['voice','face','physio']",
                        verbose_name="包含模态",
                    ),
                ),
                (
                    "sample_count",
                    models.IntegerField(default=0, verbose_name="样本数量"),
                ),
                (
                    "label_schema",
                    models.JSONField(
                        default=dict,
                        help_text="如{'emotion':['正向','负向']}",
                        verbose_name="标签定义",
                    ),
                ),
                (
                    "storage_path",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="存储路径"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "dept_belong",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="dept_belong_query",
                        to="system.deptinfo",
                        verbose_name="Data ownership department",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="modifier_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modifier",
                    ),
                ),
            ],
            options={
                "verbose_name": "多模态测评数据集",
                "verbose_name_plural": "多模态测评数据集",
            },
        ),
        migrations.CreateModel(
            name="AssessmentModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated time"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "model_name",
                    models.CharField(max_length=128, verbose_name="模型名称"),
                ),
                (
                    "backbone",
                    models.CharField(
                        default="fusion-transformer",
                        max_length=64,
                        verbose_name="主干网络",
                    ),
                ),
                (
                    "training_params",
                    models.JSONField(default=dict, verbose_name="训练参数"),
                ),
                (
                    "training_status",
                    models.SmallIntegerField(
                        choices=[
                            (1, "待训练"),
                            (2, "训练中"),
                            (3, "已完成"),
                            (4, "失败"),
                        ],
                        default=1,
                        verbose_name="训练状态",
                    ),
                ),
                (
                    "emotion_metric",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=5, verbose_name="情绪指标"
                    ),
                ),
                (
                    "personality_metric",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=5, verbose_name="性格指标"
                    ),
                ),
                (
                    "stress_metric",
                    models.DecimalField(
                        decimal_places=4, default=0, max_digits=5, verbose_name="压力指标"
                    ),
                ),
                (
                    "last_trained_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="最近训练时间"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assessment_models",
                        to="smartDiagnose.assessmentdataset",
                        verbose_name="训练数据集",
                    ),
                ),
                (
                    "dept_belong",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="dept_belong_query",
                        to="system.deptinfo",
                        verbose_name="Data ownership department",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="modifier_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modifier",
                    ),
                ),
            ],
            options={
                "verbose_name": "心理测评模型",
                "verbose_name_plural": "心理测评模型",
            },
        ),
        migrations.CreateModel(
            name="EmotionFusionEngine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated time"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "engine_name",
                    models.CharField(max_length=128, verbose_name="引擎名称"),
                ),
                (
                    "fusion_strategy",
                    models.CharField(
                        choices=[
                            ("avg", "加权平均"),
                            ("attn", "注意力融合"),
                            ("rule", "规则融合"),
                        ],
                        default="avg",
                        max_length=16,
                        verbose_name="融合策略",
                    ),
                ),
                (
                    "weights",
                    models.JSONField(
                        default=dict,
                        help_text="如{'voice':0.4,'vision':0.4,'bio':0.2}",
                        verbose_name="模态权重",
                    ),
                ),
                (
                    "latest_accuracy",
                    models.DecimalField(
                        decimal_places=4,
                        default=0,
                        max_digits=5,
                        verbose_name="最新准确率",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="是否启用"),
                ),
                (
                    "bio_model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bio_engines",
                        to="smartDiagnose.emotionrecognition",
                        verbose_name="生理信号模型",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "dept_belong",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="dept_belong_query",
                        to="system.deptinfo",
                        verbose_name="Data ownership department",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="modifier_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modifier",
                    ),
                ),
                (
                    "vision_model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vision_engines",
                        to="smartDiagnose.emotionrecognition",
                        verbose_name="表情模型",
                    ),
                ),
                (
                    "voice_model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="voice_engines",
                        to="smartDiagnose.emotionrecognition",
                        verbose_name="语音模型",
                    ),
                ),
            ],
            options={
                "verbose_name": "情绪融合引擎",
                "verbose_name_plural": "情绪融合引擎",
            },
        ),
        migrations.CreateModel(
            name="ArtGenerationJob",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated time"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "prompt",
                    models.TextField(verbose_name="提示词"),
                ),
                (
                    "style",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="风格"
                    ),
                ),
                (
                    "guidance_scale",
                    models.DecimalField(
                        decimal_places=2,
                        default=decimal.Decimal("7.50"),
                        max_digits=4,
                        verbose_name="引导强度",
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (1, "待生成"),
                            (2, "生成中"),
                            (3, "已完成"),
                            (4, "失败"),
                        ],
                        default=1,
                        verbose_name="任务状态",
                    ),
                ),
                (
                    "output_url",
                    models.URLField(blank=True, null=True, verbose_name="图像地址"),
                ),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=common.core.models.upload_directory_path,
                        verbose_name="预览图",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(default=dict, verbose_name="生成参数"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "dept_belong",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="dept_belong_query",
                        to="system.deptinfo",
                        verbose_name="Data ownership department",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="modifier_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modifier",
                    ),
                ),
                (
                    "therapy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="generation_jobs",
                        to="smartDiagnose.paintingtherapy",
                        verbose_name="治疗配置",
                    ),
                ),
            ],
            options={
                "verbose_name": "艺术生成任务",
                "verbose_name_plural": "艺术生成任务",
            },
        ),
        migrations.CreateModel(
            name="PersonalizedAssessment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Created time"
                    ),
                ),
                (
                    "updated_time",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Updated time"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="Description",
                    ),
                ),
                (
                    "emotion_score",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=4,
                        verbose_name="情绪评分",
                    ),
                ),
                (
                    "personality_profile",
                    models.JSONField(default=dict, verbose_name="性格画像"),
                ),
                (
                    "stress_level",
                    models.SmallIntegerField(
                        choices=[(1, "低压"), (2, "中压"), (3, "高压")],
                        default=2,
                        verbose_name="压力等级",
                    ),
                ),
                (
                    "summary",
                    models.TextField(blank=True, null=True, verbose_name="评估摘要"),
                ),
                (
                    "recommendations",
                    models.JSONField(default=list, verbose_name="干预建议"),
                ),
                (
                    "intervention_plan",
                    models.TextField(
                        blank=True, null=True, verbose_name="干预计划"
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "草稿"), (2, "已生成"), (3, "已干预")],
                        default=1,
                        verbose_name="报告状态",
                    ),
                ),
                (
                    "signal_snapshot",
                    models.JSONField(default=dict, verbose_name="信号快照"),
                ),
                (
                    "assessment_model",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="generated_reports",
                        to="smartDiagnose.assessmentmodel",
                        verbose_name="评估模型",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="creator_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Creator",
                    ),
                ),
                (
                    "dept_belong",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="dept_belong_query",
                        to="system.deptinfo",
                        verbose_name="Data ownership department",
                    ),
                ),
                (
                    "modifier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        related_query_name="modifier_query",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modifier",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personalized_assessments",
                        to="system.userinfo",
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "个性化评估",
                "verbose_name_plural": "个性化评估",
            },
        ),
    ]


