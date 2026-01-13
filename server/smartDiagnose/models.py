from decimal import Decimal

from django.db import models
from pilkit.processors import ResizeToFill

from common.core.models import DbAuditModel, upload_directory_path
from common.fields.image import ProcessedImageField
from system.models import UserInfo


class ModelConfig(DbAuditModel):
    """大模型配置"""
    # 普通字段
    model_name = models.CharField(verbose_name="模型名称", max_length=64, help_text="填写大模型官方名称")
    api_endpoint = models.URLField(verbose_name="API接口地址", help_text="大模型调用接口URL")
    api_key = models.CharField(verbose_name="调用密钥", max_length=128, help_text="接口访问密钥，加密存储")
    params = models.JSONField(verbose_name="调用参数", default=dict, help_text="如温度、最大token数，JSON格式")
    is_active = models.BooleanField(verbose_name="是否启用", default=True, help_text="启用后可用于业务调用")

    class Meta:
        verbose_name = "模型配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.model_name}"


class KnowledgeBase(DbAuditModel):
    """知识库管理"""
    kb_name = models.CharField(verbose_name="知识库名称", max_length=64, help_text="知识库分类名称")
    description = models.TextField(verbose_name="知识库描述", blank=True, null=True, help_text="简述知识库用途与内容")
    doc_count = models.IntegerField(verbose_name="文档数量", default=0, help_text="自动统计所属文档总数")

    class Meta:
        verbose_name = "知识库管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.kb_name}"


class KnowledgeDoc(DbAuditModel):
    """知识库文档"""
    # 外键关联
    kb = models.ForeignKey(to=KnowledgeBase, verbose_name="所属知识库", on_delete=models.CASCADE, related_name="kb_docs")
    # 普通字段
    doc_title = models.CharField(verbose_name="文档标题", max_length=128, help_text="文档核心主题")
    content = models.TextField(verbose_name="文档内容", help_text="知识库详细内容")
    tags = models.CharField(verbose_name="标签", max_length=256, blank=True, null=True, help_text="逗号分隔，如'焦虑症,心理疏导'")
    hit_count = models.IntegerField(verbose_name="命中次数", default=0, help_text="被问答调用的次数")
    # 文档附件（按文档Image/FileField规范）
    attach_file = models.FileField(verbose_name="文档附件", upload_to=upload_directory_path, blank=True, null=True, help_text="上传补充资料")

    class Meta:
        verbose_name = "知识库文档"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.doc_title}"


class EmotionRecognition(DbAuditModel):
    """情绪识别配置"""
    # 单选枚举（按文档Choices规范）
    class SupportTypeChoices(models.IntegerChoices):
        TEXT = 1, "文本识别"
        VOICE = 2, "语音识别"
        IMAGE = 3, "图像识别"
    
    recog_name = models.CharField(verbose_name="识别模型名称", max_length=64, help_text="情绪识别模型名称")
    api_endpoint = models.URLField(verbose_name="API接口地址", help_text="情绪识别接口URL")
    api_key = models.CharField(verbose_name="调用密钥", max_length=128, help_text="接口访问密钥")
    supported_type = models.SmallIntegerField(choices=SupportTypeChoices, default=SupportTypeChoices.TEXT, verbose_name="支持识别类型")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)
    # 缩略图（按文档ProcessedImageField规范）
    test_image = ProcessedImageField(verbose_name="测试图像", null=True, blank=True,
                                     upload_to=upload_directory_path,
                                     processors=[ResizeToFill(512, 512)],
                                     scales=[1, 2],
                                     format='png', help_text="上传测试用情绪图像")

    class Meta:
        verbose_name = "情绪识别配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.recog_name}"


class PaintingTherapy(DbAuditModel):
    """绘画治疗配置"""
    therapy_name = models.CharField(verbose_name="治疗模型名称", max_length=64, help_text="绘画治疗模型名称")
    api_endpoint = models.URLField(verbose_name="API接口地址", help_text="绘画生成接口URL")
    api_key = models.CharField(verbose_name="调用密钥", max_length=128, help_text="接口访问密钥")
    style_options = models.JSONField(verbose_name="绘画风格选项", default=list, help_text="JSON格式，如['治愈系','抽象派']")
    is_active = models.BooleanField(verbose_name="是否启用", default=True)
    # 示例图像（按文档ImageField规范）
    style_preview = models.ImageField(verbose_name="风格预览图", null=True, blank=True, upload_to=upload_directory_path, help_text="上传风格示例图")

    class Meta:
        verbose_name = "绘画治疗配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.therapy_name}"


class AssessmentDataset(DbAuditModel):
    """多模态心理测评数据集"""

    dataset_name = models.CharField(verbose_name="数据集名称", max_length=128)
    description = models.TextField(verbose_name="数据集描述", blank=True, null=True)
    modalities = models.JSONField(verbose_name="包含模态", default=list, help_text="如['voice','face','physio']")
    sample_count = models.IntegerField(verbose_name="样本数量", default=0)
    label_schema = models.JSONField(verbose_name="标签定义", default=dict, help_text="如{'emotion':['正向','负向']}")
    storage_path = models.CharField(verbose_name="存储路径", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "多模态测评数据集"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.dataset_name}"


class AssessmentModel(DbAuditModel):
    """多模态心理测评模型"""

    class TrainingStatusChoices(models.IntegerChoices):
        PENDING = 1, "待训练"
        TRAINING = 2, "训练中"
        COMPLETED = 3, "已完成"
        FAILED = 4, "失败"

    dataset = models.ForeignKey(
        to=AssessmentDataset,
        verbose_name="训练数据集",
        on_delete=models.PROTECT,
        related_name="assessment_models",
    )
    model_name = models.CharField(verbose_name="模型名称", max_length=128)
    backbone = models.CharField(verbose_name="主干网络", max_length=64, default="fusion-transformer")
    training_params = models.JSONField(verbose_name="训练参数", default=dict)
    training_status = models.SmallIntegerField(
        verbose_name="训练状态", choices=TrainingStatusChoices, default=TrainingStatusChoices.PENDING
    )
    emotion_metric = models.DecimalField(verbose_name="情绪指标", max_digits=5, decimal_places=4, default=0)
    personality_metric = models.DecimalField(verbose_name="性格指标", max_digits=5, decimal_places=4, default=0)
    stress_metric = models.DecimalField(verbose_name="压力指标", max_digits=5, decimal_places=4, default=0)
    last_trained_time = models.DateTimeField(verbose_name="最近训练时间", blank=True, null=True)

    class Meta:
        verbose_name = "心理测评模型"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.model_name}"


class PersonalizedAssessment(DbAuditModel):
    """个性化评估与干预"""

    class StressLevelChoices(models.IntegerChoices):
        LOW = 1, "低压"
        MEDIUM = 2, "中压"
        HIGH = 3, "高压"

    class ReportStatusChoices(models.IntegerChoices):
        DRAFT = 1, "草稿"
        GENERATED = 2, "已生成"
        INTERVENED = 3, "已干预"

    user = models.ForeignKey(
        to=UserInfo, verbose_name="用户", on_delete=models.CASCADE, related_name="personalized_assessments"
    )
    assessment_model = models.ForeignKey(
        to=AssessmentModel,
        verbose_name="评估模型",
        on_delete=models.SET_NULL,
        related_name="generated_reports",
        null=True,
        blank=True,
    )
    emotion_score = models.DecimalField(verbose_name="情绪评分", max_digits=4, decimal_places=2, default=0)
    personality_profile = models.JSONField(verbose_name="性格画像", default=dict)
    stress_level = models.SmallIntegerField(
        verbose_name="压力等级", choices=StressLevelChoices, default=StressLevelChoices.MEDIUM
    )
    summary = models.TextField(verbose_name="评估摘要", blank=True, null=True)
    recommendations = models.JSONField(verbose_name="干预建议", default=list)
    intervention_plan = models.TextField(verbose_name="干预计划", blank=True, null=True)
    status = models.SmallIntegerField(
        verbose_name="报告状态", choices=ReportStatusChoices, default=ReportStatusChoices.DRAFT
    )
    signal_snapshot = models.JSONField(verbose_name="信号快照", default=dict)

    class Meta:
        verbose_name = "个性化评估"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.user.username}-报告{self.pk}"


class EmotionFusionEngine(DbAuditModel):
    """多源情绪识别引擎"""

    class FusionStrategyChoices(models.TextChoices):
        AVERAGE = "avg", "加权平均"
        ATTENTION = "attn", "注意力融合"
        RULE = "rule", "规则融合"

    engine_name = models.CharField(verbose_name="引擎名称", max_length=128)
    voice_model = models.ForeignKey(
        to=EmotionRecognition,
        verbose_name="语音模型",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="voice_engines",
    )
    vision_model = models.ForeignKey(
        to=EmotionRecognition,
        verbose_name="表情模型",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vision_engines",
    )
    bio_model = models.ForeignKey(
        to=EmotionRecognition,
        verbose_name="生理信号模型",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bio_engines",
    )
    fusion_strategy = models.CharField(
        verbose_name="融合策略",
        max_length=16,
        choices=FusionStrategyChoices.choices,
        default=FusionStrategyChoices.AVERAGE,
    )
    weights = models.JSONField(verbose_name="模态权重", default=dict, help_text="如{'voice':0.4,'vision':0.4,'bio':0.2}")
    latest_accuracy = models.DecimalField(verbose_name="最新准确率", max_digits=5, decimal_places=4, default=0)
    is_active = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        verbose_name = "情绪融合引擎"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.engine_name}"


class ArtGenerationJob(DbAuditModel):
    """艺术生成任务"""

    class JobStatusChoices(models.IntegerChoices):
        PENDING = 1, "待生成"
        RUNNING = 2, "生成中"
        COMPLETED = 3, "已完成"
        FAILED = 4, "失败"

    therapy = models.ForeignKey(
        to=PaintingTherapy,
        verbose_name="治疗配置",
        on_delete=models.PROTECT,
        related_name="generation_jobs",
    )
    prompt = models.TextField(verbose_name="提示词")
    style = models.CharField(verbose_name="风格", max_length=64, blank=True, null=True)
    guidance_scale = models.DecimalField(
        verbose_name="引导强度", max_digits=4, decimal_places=2, default=Decimal("7.50")
    )
    status = models.SmallIntegerField(
        verbose_name="任务状态", choices=JobStatusChoices, default=JobStatusChoices.PENDING
    )
    output_url = models.URLField(verbose_name="图像地址", blank=True, null=True)
    preview_image = models.ImageField(
        verbose_name="预览图",
        upload_to=upload_directory_path,
        null=True,
        blank=True,
    )
    metadata = models.JSONField(verbose_name="生成参数", default=dict)

    class Meta:
        verbose_name = "艺术生成任务"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.therapy.therapy_name}-任务{self.pk}"


class ChatRecord(DbAuditModel):
    """心理问答记录"""
    # 外键关联（按文档ForeignKey规范）
    user = models.ForeignKey(to=UserInfo, verbose_name="用户", on_delete=models.CASCADE, related_name="chat_user")
    kb_ref = models.ForeignKey(to=KnowledgeDoc, verbose_name="关联知识库文档", on_delete=models.SET_NULL, null=True, blank=True, related_name="chat_refs")
    # 普通字段
    session_id = models.CharField(verbose_name="会话ID", max_length=64, help_text="标识一次完整对话")
    question = models.TextField(verbose_name="用户问题", help_text="用户输入的问题内容")
    answer = models.TextField(verbose_name="模型回答", blank=True, null=True, help_text="大模型返回的回答")
    emotion_result = models.CharField(verbose_name="情绪识别结果", max_length=64, blank=True, null=True, help_text="如'焦虑(0.85)'")

    class Meta:
        verbose_name = "心理问答记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}-{self.session_id}"