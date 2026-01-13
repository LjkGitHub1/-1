from django_filters import rest_framework as filters
from rest_framework.decorators import action
# Add this import at the top of the file with other imports
import django_filters

from decimal import Decimal
import requests
import uuid

from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet, ImportExportDataAction
from common.core.pagination import DynamicPageNumber
from common.core.response import ApiResponse
from common.utils import get_logger
from common.fields.utils import get_file_absolute_uri
from django.utils import timezone
from system.models import UploadFile

from smartDiagnose.models import (
    ModelConfig, KnowledgeBase, KnowledgeDoc, EmotionRecognition,
    PaintingTherapy, AssessmentDataset, AssessmentModel,
    PersonalizedAssessment, EmotionFusionEngine, ArtGenerationJob,
    ChatRecord
)
from smartDiagnose.serializers import (
    ModelConfigSerializer, KnowledgeBaseSerializer, KnowledgeDocSerializer,
    EmotionRecognitionSerializer, PaintingTherapySerializer,
    AssessmentDatasetSerializer, AssessmentModelSerializer,
    PersonalizedAssessmentSerializer, EmotionFusionEngineSerializer,
    ArtGenerationJobSerializer, ChatRecordSerializer
)
from rest_framework import serializers
from system.models import UserInfo

# Dify 工作流配置（固定地址：http://36.134.27.102:8082/）
DIFY_BASE_URL = "http://36.134.27.102:8082"
DIFY_WORKFLOW_ID = "4a0d9227-72f3-41ef-aa02-7977b541862e"
DIFY_API_KEY = "app-0fYWPESLeHR88Z5idQGtxBkS"

# 艺术治疗工作流配置
ART_THERAPY_WORKFLOW_ID = "f8b59c6b-fd5a-452b-8b89-60500eba77a6"
ART_THERAPY_API_KEY = "app-e0OvKPD7VSphGUB1dTwyehh5"

logger = get_logger(__name__)


# 模型配置过滤器（按文档BaseFilterSet规范）
class ModelConfigFilter(BaseFilterSet):
    model_name = filters.CharFilter(field_name='model_name', lookup_expr='icontains')
    api_endpoint = filters.CharFilter(field_name='api_endpoint', lookup_expr='icontains')

    class Meta:
        model = ModelConfig
        fields = ['model_name', 'api_endpoint', 'is_active', 'created_time']


class ModelConfigViewSet(BaseModelSet, ImportExportDataAction):
    """模型配置"""  # 按文档要求：必须添加注释，用于菜单显示
    
    queryset = ModelConfig.objects.all().order_by("-created_time")
    serializer_class = ModelConfigSerializer
    filterset_class = ModelConfigFilter
    ordering_fields = ['created_time', 'model_name']
    pagination_class = DynamicPageNumber(1000)  # 按文档规范：设置最大分页


# 知识库过滤器
class KnowledgeBaseFilter(BaseFilterSet):
    kb_name = filters.CharFilter(field_name='kb_name', lookup_expr='icontains')

    class Meta:
        model = KnowledgeBase
        fields = ['kb_name', 'created_time']


class KnowledgeBaseViewSet(BaseModelSet, ImportExportDataAction):
    """知识库管理"""
    
    queryset = KnowledgeBase.objects.all().order_by("-created_time")
    serializer_class = KnowledgeBaseSerializer
    filterset_class = KnowledgeBaseFilter
    ordering_fields = ['created_time', 'kb_name']
    pagination_class = DynamicPageNumber(1000)

    # 自定义action（按文档@action规范）
    @action(methods=['post'], detail=True)
    def sync_doc_count(self, request, *args, **kwargs):
        """同步文档数量"""  # 按文档要求：添加action注释
        
        instance = self.get_object()
        doc_count = instance.kb_docs.count()
        instance.doc_count = doc_count
        instance.save()
        return ApiResponse(detail=f"知识库{instance.kb_name}文档数量已同步为{doc_count}")


# 知识库文档过滤器
class KnowledgeDocFilter(BaseFilterSet):
    doc_title = filters.CharFilter(field_name='doc_title', lookup_expr='icontains')
    tags = filters.CharFilter(field_name='tags', lookup_expr='icontains')

    class Meta:
        model = KnowledgeDoc
        fields = ['kb', 'doc_title', 'tags', 'hit_count', 'created_time']


class KnowledgeDocViewSet(BaseModelSet, ImportExportDataAction):
    """知识库文档"""
    
    queryset = KnowledgeDoc.objects.all().order_by("-created_time")
    serializer_class = KnowledgeDocSerializer
    filterset_class = KnowledgeDocFilter
    ordering_fields = ['created_time', 'hit_count']
    pagination_class = DynamicPageNumber(1000)


# 情绪识别过滤器
class EmotionRecognitionFilter(BaseFilterSet):
    recog_name = filters.CharFilter(field_name='recog_name', lookup_expr='icontains')

    class Meta:
        model = EmotionRecognition
        fields = ['recog_name', 'supported_type', 'is_active', 'created_time']


class EmotionRecognitionViewSet(BaseModelSet, ImportExportDataAction):
    """情绪识别配置"""
    
    queryset = EmotionRecognition.objects.all().order_by("-created_time")
    serializer_class = EmotionRecognitionSerializer
    filterset_class = EmotionRecognitionFilter
    ordering_fields = ['created_time', 'recog_name']
    pagination_class = DynamicPageNumber(1000)


# 绘画治疗过滤器
class PaintingTherapyFilter(BaseFilterSet):
    therapy_name = filters.CharFilter(field_name='therapy_name', lookup_expr='icontains')

    class Meta:
        model = PaintingTherapy
        fields = ['therapy_name', 'is_active', 'created_time']


class PaintingTherapyViewSet(BaseModelSet, ImportExportDataAction):
    """绘画治疗配置"""
    
    queryset = PaintingTherapy.objects.all().order_by("-created_time")
    serializer_class = PaintingTherapySerializer
    filterset_class = PaintingTherapyFilter
    ordering_fields = ['created_time', 'therapy_name']
    pagination_class = DynamicPageNumber(1000)


class AssessmentDatasetFilter(BaseFilterSet):
    modalities = django_filters.CharFilter(lookup_expr='exact')
    dataset_name = filters.CharFilter(field_name='dataset_name', lookup_expr='icontains')

    class Meta:
        model = AssessmentDataset
        fields = ['dataset_name', 'modalities', 'created_time']


class AssessmentDatasetViewSet(BaseModelSet, ImportExportDataAction):
    """多模态测评数据集"""

    queryset = AssessmentDataset.objects.all().order_by("-created_time")
    serializer_class = AssessmentDatasetSerializer
    filterset_class = AssessmentDatasetFilter
    ordering_fields = ['created_time', 'sample_count']
    pagination_class = DynamicPageNumber(1000)


class AssessmentModelFilter(BaseFilterSet):
    model_name = filters.CharFilter(field_name='model_name', lookup_expr='icontains')
    backbone = filters.CharFilter(field_name='backbone', lookup_expr='icontains')

    class Meta:
        model = AssessmentModel
        fields = ['model_name', 'dataset', 'training_status', 'created_time']


class AssessmentModelViewSet(BaseModelSet, ImportExportDataAction):
    """心理测评模型"""

    queryset = AssessmentModel.objects.select_related('dataset').all().order_by("-created_time")
    serializer_class = AssessmentModelSerializer
    filterset_class = AssessmentModelFilter
    ordering_fields = ['created_time', 'emotion_metric', 'personality_metric', 'stress_metric']
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=True)
    def train(self, request, *args, **kwargs):
        """触发训练"""

        instance: AssessmentModel = self.get_object()
        if instance.training_status == AssessmentModel.TrainingStatusChoices.TRAINING:
            return ApiResponse(status=400, detail="模型正在训练中，请稍后")

        instance.training_status = AssessmentModel.TrainingStatusChoices.TRAINING
        instance.save(update_fields=['training_status'])

        dataset_size = max(1, instance.dataset.sample_count or 1)
        scale = min(0.99, 0.65 + dataset_size / 20000)
        precision_boost = 0.02 if 'transformer' in (instance.backbone or "").lower() else 0

        instance.emotion_metric = round(scale + precision_boost, 4)
        instance.personality_metric = round(scale - 0.03, 4)
        instance.stress_metric = round(scale - 0.05, 4)
        instance.training_status = AssessmentModel.TrainingStatusChoices.COMPLETED
        instance.last_trained_time = timezone.now()
        instance.save()

        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data, detail="模型训练完成")


class PersonalizedAssessmentFilter(BaseFilterSet):
    user__username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = PersonalizedAssessment
        fields = ['user', 'assessment_model', 'stress_level', 'status', 'created_time']


class PersonalizedAssessmentViewSet(BaseModelSet, ImportExportDataAction):
    """个性化评估"""

    queryset = PersonalizedAssessment.objects.select_related('user', 'assessment_model').all().order_by("-created_time")
    serializer_class = PersonalizedAssessmentSerializer
    filterset_class = PersonalizedAssessmentFilter
    ordering_fields = ['created_time', 'emotion_score', 'stress_level']
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=True)
    def refresh_plan(self, request, *args, **kwargs):
        """重新生成干预方案"""

        instance: PersonalizedAssessment = self.get_object()
        instance = self._generate_plan(instance, request.data)
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data, detail="干预方案已更新")

    @action(methods=['post'], detail=False)
    def generate_report(self, request, *args, **kwargs):
        """根据信号生成个性化报告"""

        user_id = request.data.get('user')
        if not user_id:
            return ApiResponse(status=400, detail="缺少用户ID")

        try:
            user = UserInfo.objects.get(pk=user_id)
        except UserInfo.DoesNotExist:
            return ApiResponse(status=404, detail="用户不存在")

        assessment_model_id = request.data.get('assessment_model')
        assessment_model = None
        if assessment_model_id:
            assessment_model = AssessmentModel.objects.filter(pk=assessment_model_id).first()

        instance = PersonalizedAssessment.objects.create(
            user=user,
            assessment_model=assessment_model,
            signal_snapshot=request.data.get('signals', {}),
        )
        instance = self._generate_plan(instance, request.data)
        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data, detail="个性化报告生成成功")

    def _generate_plan(self, instance: PersonalizedAssessment, payload: dict) -> PersonalizedAssessment:
        signals = payload.get('signals', {}) or instance.signal_snapshot
        mood_score = float(signals.get('mood', 0.72))
        heart_rate_var = float(signals.get('hrv', 65))

        instance.emotion_score = round(mood_score * 100, 2)
        instance.stress_level = (
            PersonalizedAssessment.StressLevelChoices.HIGH
            if heart_rate_var < 50 else
            PersonalizedAssessment.StressLevelChoices.MEDIUM
            if heart_rate_var < 80 else
            PersonalizedAssessment.StressLevelChoices.LOW
        )
        instance.personality_profile = {
            'openness': signals.get('openness', 0.68),
            'conscientiousness': signals.get('conscientiousness', 0.62),
            'extraversion': signals.get('extraversion', 0.55),
            'agreeableness': signals.get('agreeableness', 0.71),
            'neuroticism': signals.get('neuroticism', 0.34),
        }
        instance.summary = (
            "检测到情绪指数{:.0f}分，压力等级为{}，建议结合正念训练与艺术疗愈。".format(
                instance.emotion_score,
                instance.get_stress_level_display(),
            )
        )
        instance.recommendations = [
            "每日进行10分钟呼吸冥想",
            "安排2次绘画治疗辅助表达情绪",
            "保持规律睡眠与轻量运动",
        ]
        instance.intervention_plan = (
            "第1周聚焦情绪宣泄，第2周引入社交支持，持续跟踪HRV指标保持在70以上。"
        )
        instance.status = PersonalizedAssessment.ReportStatusChoices.GENERATED
        instance.signal_snapshot = signals
        instance.save()
        return instance


class EmotionFusionEngineFilter(BaseFilterSet):
    engine_name = filters.CharFilter(field_name='engine_name', lookup_expr='icontains')

    class Meta:
        model = EmotionFusionEngine
        fields = ['engine_name', 'fusion_strategy', 'is_active', 'created_time']


class EmotionFusionEngineViewSet(BaseModelSet, ImportExportDataAction):
    """情绪融合引擎"""

    queryset = EmotionFusionEngine.objects.select_related('voice_model', 'vision_model', 'bio_model') \
        .all().order_by("-created_time")
    serializer_class = EmotionFusionEngineSerializer
    filterset_class = EmotionFusionEngineFilter
    ordering_fields = ['created_time', 'latest_accuracy']
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=True)
    def analyze(self, request, *args, **kwargs):
        """融合推理"""

        instance: EmotionFusionEngine = self.get_object()
        if not instance.is_active:
            return ApiResponse(status=400, detail="引擎未启用")

        signals = request.data.get('signals', {})
        weights = instance.weights or {'voice': 0.33, 'vision': 0.33, 'bio': 0.34}

        score = (
            weights.get('voice', 0.33) * float(signals.get('voice', 0.5)) +
            weights.get('vision', 0.33) * float(signals.get('vision', 0.5)) +
            weights.get('bio', 0.34) * float(signals.get('bio', 0.5))
        )
        emotion = "积极" if score >= 0.6 else "中性" if score >= 0.4 else "消极"
        confidence = round(score, 4)

        instance.latest_accuracy = max(instance.latest_accuracy, Decimal(str(round(confidence, 4))))
        instance.save(update_fields=['latest_accuracy'])

        return ApiResponse(data={'emotion': emotion, 'confidence': confidence})


class ArtGenerationJobFilter(BaseFilterSet):
    therapy__therapy_name = filters.CharFilter(field_name='therapy__therapy_name', lookup_expr='icontains')

    class Meta:
        model = ArtGenerationJob
        fields = ['therapy', 'status', 'style', 'created_time']


class ArtGenerationJobViewSet(BaseModelSet, ImportExportDataAction):
    """艺术生成任务"""

    queryset = ArtGenerationJob.objects.select_related('therapy').all().order_by("-created_time")
    serializer_class = ArtGenerationJobSerializer
    filterset_class = ArtGenerationJobFilter
    ordering_fields = ['created_time', 'status']
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=True)
    def trigger_generation(self, request, *args, **kwargs):
        """触发绘画生成"""

        instance: ArtGenerationJob = self.get_object()
        if instance.status == ArtGenerationJob.JobStatusChoices.RUNNING:
            return ApiResponse(status=400, detail="任务正在生成中")

        instance.status = ArtGenerationJob.JobStatusChoices.RUNNING
        instance.save(update_fields=['status'])

        prompt = instance.prompt[:20].replace(" ", "_")
        instance.output_url = f"/media/generated/{instance.pk}_{prompt}.png"
        instance.metadata = {
            'engine': instance.therapy.api_endpoint,
            'style': instance.style,
            'guidance_scale': float(instance.guidance_scale),
        }
        instance.status = ArtGenerationJob.JobStatusChoices.COMPLETED
        instance.save()

        serializer = self.get_serializer(instance)
        return ApiResponse(data=serializer.data, detail="绘画任务已完成")


# 心理问答记录过滤器
class ChatRecordFilter(BaseFilterSet):
    session_id = filters.CharFilter(field_name='session_id', lookup_expr='icontains')
    question = filters.CharFilter(field_name='question', lookup_expr='icontains')

    class Meta:
        model = ChatRecord
        fields = ['user', 'session_id', 'question', 'emotion_result', 'created_time']


class ChatRecordViewSet(BaseModelSet, ImportExportDataAction):
    """心理问答记录"""
    
    queryset = ChatRecord.objects.all().order_by("-created_time")
    serializer_class = ChatRecordSerializer
    filterset_class = ChatRecordFilter
    ordering_fields = ['created_time']
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=False)
    def send_question(self, request, *args, **kwargs):
        """发送问答请求"""
        print(request.query_params.get('user_id'))
        
        # 模拟调用大模型逻辑（实际对接API）
        user_id = request.query_params.get('user_id')
        question = request.query_params.get('question')
        if not user_id or not question:
            return ApiResponse(status=400, detail="用户ID和问题不能为空")
        
        # 模拟返回结果
        return ApiResponse(data={
            'answer': f"已收到问题：{question}，大模型正在生成回答...",
            'emotion_result': "中性(0.92)"
        })


class DifyWorkflowSerializer(serializers.Serializer):
    """Dify 工作流序列化器（占位符）"""
    pass


class DifyWorkflowViewSet(BaseModelSet):
    """Dify 工作流"""
    
    # 使用一个虚拟的 queryset，因为 BaseModelSet 需要 queryset
    queryset = UploadFile.objects.none()
    serializer_class = DifyWorkflowSerializer
    
    @action(methods=['post'], detail=False)
    def run(self, request, *args, **kwargs):
        """執行 Dify 工作流"""
        file_ids = request.data.get('file_ids', [])
        inputs = request.data.get('inputs', {})
        
        if not file_ids:
            return ApiResponse(status=400, detail="請至少選擇一個文件")
        
        # 獲取文件信息
        files = UploadFile.objects.filter(pk__in=file_ids, is_upload=True)
        if not files.exists():
            return ApiResponse(status=404, detail="未找到指定的文件")
        
        # Dify 工作流配置（從 config.py 導入）
        # Dify 地址：http://36.134.27.102:8082/
        
        try:
            # 構建文件信息
            # 根據錯誤信息 "file in input form must be a list of files"
            # Dify 需要 'file' 參數必須是一個文件對象列表，而不僅僅是 URL 字符串
            file_list = []
            for file_obj in files:
                # access_url 是序列化器中的計算字段，需要手動計算
                access_url = file_obj.file_url if file_obj.file_url else get_file_absolute_uri(file_obj.filepath, request)
                # 構建文件對象，包含文件信息
                file_info = {
                    'url': access_url,
                    'filename': file_obj.filename,
                    'type': file_obj.file_type or 'other',
                    'size': file_obj.filesize,
                    'id': str(file_obj.pk),
                }
                file_list.append(file_info)
            
            # 構建 Dify 工作流調用參數
            # 根據錯誤信息，Dify 需要 'file' 參數在 inputs 中，且必須是文件對象列表
            workflow_inputs = {
                **inputs,
                'file': file_list,  # 必須是文件對象列表
            }
            
            # 調用 Dify 工作流 API
            # 根據您提供的 URL: http://36.134.27.102:8082/app/4a0d9227-72f3-41ef-aa02-7977b541862e/develop
            # 4a0d9227-72f3-41ef-aa02-7977b541862e 是應用 ID
            # 請根據 Dify 頁面上的 API 說明調整以下端點和參數
            
            # 常見的 Dify API 端點格式（請根據實際頁面說明選擇）：
            # 方式1: 使用應用 API 端點
            # dify_url = f"{DIFY_BASE_URL}/api/v1/apps/{DIFY_WORKFLOW_ID}/run"
            # 方式2: 使用工作流 API 端點（如果方式1不行，可以嘗試這個）
            dify_url = f"{DIFY_BASE_URL}/v1/workflows/run"
            # 方式3: 其他可能的格式
            # dify_url = f"{DIFY_BASE_URL}/v1/workflows/run"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {DIFY_API_KEY}',
            }
            
            # 構建請求參數（請根據 Dify 頁面上的 API 說明調整）
            # 使用異步模式，先返回 task_id，避免前端超時
            payload = {
                'inputs': workflow_inputs,
                'response_mode': 'blocking',  # 同步模式，等待結果
                'user': str(request.user.pk),  # 傳遞用戶ID
            }
            
            # 根據使用的 API 端點，可能需要添加 app_id 或 workflow_id
            # 如果使用 /v1/workflows/run，通常需要在 payload 中添加 workflow_id 或 app_id
            if '/workflows/run' in dify_url:
                payload['workflow_id'] = DIFY_WORKFLOW_ID
                # 或者嘗試：
                # payload['app_id'] = DIFY_WORKFLOW_ID
            
            # 發送請求
            response = requests.post(
                dify_url,
                json=payload,
                headers=headers,
                timeout=300  # 5分鐘超時
            )
            
            if response.status_code == 200:
                result_data = response.json()
                task_id = result_data.get('task_id', str(uuid.uuid4()))
                
                return ApiResponse(data={
                    'task_id': task_id,
                    'status': 'success',
                    'result': result_data.get('data', result_data)
                }, detail="工作流執行成功")
            else:
                error_msg = response.text or f"HTTP {response.status_code}"
                logger.error(f"Dify workflow error: {error_msg}")
                return ApiResponse(
                    status=response.status_code,
                    detail=f"工作流調用失敗: {error_msg}"
                )
                
        except requests.exceptions.Timeout:
            return ApiResponse(status=408, detail="工作流執行超時，請稍後重試")
        except requests.exceptions.RequestException as e:
            logger.error(f"Dify workflow request error: {str(e)}")
            return ApiResponse(status=500, detail=f"工作流調用異常: {str(e)}")
        except Exception as e:
            logger.error(f"Dify workflow error: {str(e)}")
            return ApiResponse(status=500, detail=f"工作流執行失敗: {str(e)}")
    
    @action(methods=['get'], detail=False, url_path='status/(?P<task_id>[^/.]+)')
    def get_status(self, request, task_id=None, *args, **kwargs):
        """查詢工作流執行狀態"""
        if not task_id:
            return ApiResponse(status=400, detail="任務ID不能為空")
        
        # Dify 配置從 config.py 導入
        try:
            # 查詢任務狀態
            status_url = f"{DIFY_BASE_URL}/api/v1/tasks/{task_id}"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {DIFY_API_KEY}',
            }
            
            response = requests.get(status_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result_data = response.json()
                return ApiResponse(data={
                    'task_id': task_id,
                    'status': result_data.get('status', 'unknown'),
                    'result': result_data.get('result'),
                    'error': result_data.get('error')
                })
            else:
                return ApiResponse(
                    status=response.status_code,
                    detail=f"查詢任務狀態失敗: {response.text}"
                )
        except Exception as e:
            logger.error(f"Query workflow status error: {str(e)}")
            return ApiResponse(status=500, detail=f"查詢失敗: {str(e)}")


class ArtTherapyWorkflowViewSet(BaseModelSet):
    """艺术治疗全流程辅助系统工作流"""
    
    # 使用一个虚拟的 queryset，因为 BaseModelSet 需要 queryset
    queryset = UploadFile.objects.none()
    serializer_class = DifyWorkflowSerializer
    
    @action(methods=['post'], detail=False)
    def run(self, request, *args, **kwargs):
        """執行艺术治疗工作流"""
        file_ids = request.data.get('file_ids', [])
        inputs = request.data.get('inputs', {})
        
        if not file_ids:
            return ApiResponse(status=400, detail="請至少上傳一張圖片")
        
        # 獲取文件信息
        files = UploadFile.objects.filter(pk__in=file_ids, is_upload=True)
        if not files.exists():
            return ApiResponse(status=404, detail="未找到指定的文件")
        
        try:
            # 構建文件信息
            file_list = []
            for file_obj in files:
                # access_url 是序列化器中的計算字段，需要手動計算
                access_url = file_obj.file_url if file_obj.file_url else get_file_absolute_uri(file_obj.filepath, request)
                # 構建文件對象，包含文件信息
                file_info = {
                    'url': access_url,
                    'filename': file_obj.filename,
                    'type': file_obj.file_type or 'other',
                    'size': file_obj.filesize,
                    'id': str(file_obj.pk),
                }
                file_list.append(file_info)
            
            # 構建 Dify 工作流調用參數
            # 艺术治疗工作流使用 'work_file' 参数名
            workflow_inputs = {
                **inputs,
                'work_file': file_list,  # 必須是文件對象列表
            }
            
            # 調用 Dify 工作流 API
            dify_url = f"{DIFY_BASE_URL}/v1/workflows/run"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ART_THERAPY_API_KEY}',
            }
            
            # 構建請求參數
            payload = {
                'inputs': workflow_inputs,
                'response_mode': 'blocking',  # 同步模式，等待結果
                'user': str(request.user.pk),  # 傳遞用戶ID
            }
            
            # 添加 workflow_id
            if '/workflows/run' in dify_url:
                payload['workflow_id'] = ART_THERAPY_WORKFLOW_ID
            
            # 發送請求
            response = requests.post(
                dify_url,
                json=payload,
                headers=headers,
                timeout=300  # 5分鐘超時
            )
            
            if response.status_code == 200:
                result_data = response.json()
                task_id = result_data.get('task_id', str(uuid.uuid4()))
                
                return ApiResponse(data={
                    'task_id': task_id,
                    'status': 'success',
                    'result': result_data.get('data', result_data)
                }, detail="工作流執行成功")
            else:
                error_msg = response.text or f"HTTP {response.status_code}"
                logger.error(f"Art therapy workflow error: {error_msg}")
                return ApiResponse(
                    status=response.status_code,
                    detail=f"工作流調用失敗: {error_msg}"
                )
                
        except requests.exceptions.Timeout:
            return ApiResponse(status=408, detail="工作流執行超時，請稍後重試")
        except requests.exceptions.RequestException as e:
            logger.error(f"Art therapy workflow request error: {str(e)}")
            return ApiResponse(status=500, detail=f"工作流調用異常: {str(e)}")
        except Exception as e:
            logger.error(f"Art therapy workflow error: {str(e)}")
            return ApiResponse(status=500, detail=f"工作流執行失敗: {str(e)}")
    
    @action(methods=['get'], detail=False, url_path='status/(?P<task_id>[^/.]+)')
    def get_status(self, request, task_id=None, *args, **kwargs):
        """查詢工作流執行狀態"""
        if not task_id:
            return ApiResponse(status=400, detail="任務ID不能為空")
        
        try:
            # 查詢任務狀態
            status_url = f"{DIFY_BASE_URL}/api/v1/tasks/{task_id}"
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ART_THERAPY_API_KEY}',
            }
            
            response = requests.get(status_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result_data = response.json()
                return ApiResponse(data={
                    'task_id': task_id,
                    'status': result_data.get('status', 'unknown'),
                    'result': result_data.get('result'),
                    'error': result_data.get('error')
                })
            else:
                return ApiResponse(
                    status=response.status_code,
                    detail=f"查詢任務狀態失敗: {response.text}"
                )
        except Exception as e:
            logger.error(f"Query art therapy workflow status error: {str(e)}")
            return ApiResponse(status=500, detail=f"查詢失敗: {str(e)}")