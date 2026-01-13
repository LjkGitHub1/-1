from rest_framework import serializers

from common.core.serializers import BaseModelSerializer
from common.fields.utils import input_wrapper
from smartDiagnose import models
from system.models import UserInfo


class ModelConfigSerializer(BaseModelSerializer):
    class Meta:
        model = models.ModelConfig
        # 按文档规范：包含pk、业务字段、审计字段，table_fields控制表格显示
        fields = [
            'pk', 'model_name', 'api_endpoint', 'api_key', 'params', 'is_active',
            'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'model_name', 'api_endpoint', 'is_active', 'created_time'
        ]
        # 按文档extra_kwargs规范：控制字段属性与前端渲染
        extra_kwargs = {
            'pk': {'read_only': True},
            'api_key': {'write_only': True, 'help_text': '仅输入时显示，列表/详情不返回'},
            # 'is_active': {'input_type': 'switch', 'label': '启用状态'}
        }


class KnowledgeBaseSerializer(BaseModelSerializer):
    class Meta:
        model = models.KnowledgeBase
        fields = [
            'pk', 'kb_name', 'description', 'doc_count', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'kb_name', 'doc_count', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'doc_count': {'read_only': True, 'help_text': '自动统计，不可编辑'}
        }


class KnowledgeDocSerializer(BaseModelSerializer):
    class Meta:
        model = models.KnowledgeDoc
        fields = [
            'pk', 'kb', 'doc_title', 'content', 'tags', 'hit_count', 'attach_file',
            'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'kb', 'doc_title', 'tags', 'hit_count', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'hit_count': {'read_only': True},
            # 外键渲染（按文档api-search类型规范）
            # 'kb': {
            #     'attrs': ['pk', 'kb_name'], 'required': True, 'format': "{kb_name}({pk})",
            #     'input_type': 'api-search-knowledgebase'
            # },
            # 'attach_file': {'input_type': 'file-upload', 'label': '文档附件'}
        }

    # 自定义字段（按文档input_wrapper规范）
    # attach_file_name = input_wrapper(serializers.SerializerMethodField)(read_only=True, input_type='text', label="附件名称")

    def get_attach_file_name(self, obj):
        return obj.attach_file.name.split('/')[-1] if obj.attach_file else None


class EmotionRecognitionSerializer(BaseModelSerializer):
    class Meta:
        model = models.EmotionRecognition
        fields = [
            'pk', 'recog_name', 'api_endpoint', 'api_key', 'supported_type', 'is_active',
            'test_image', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'recog_name', 'supported_type', 'is_active', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'api_key': {'write_only': True},
            # 'supported_type': {'input_type': 'select', 'label': '识别类型'},
            # 'test_image': {'input_type': 'image-upload', 'label': '测试图像'}
        }

    # 枚举字段文本显示（按文档SerializerMethodField规范）
    # supported_type_text = input_wrapper(serializers.SerializerMethodField)(read_only=True, input_type='text', label="识别类型")

    def get_supported_type_text(self, obj):
        return obj.get_supported_type_display()


class PaintingTherapySerializer(BaseModelSerializer):
    class Meta:
        model = models.PaintingTherapy
        fields = [
            'pk', 'therapy_name', 'api_endpoint', 'api_key', 'style_options', 'is_active',
            'style_preview', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'therapy_name', 'is_active', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'api_key': {'write_only': True},
            # 'style_options': {'input_type': 'json-editor', 'label': '风格选项'},
            # 'style_preview': {'input_type': 'image-upload', 'label': '风格预览图'}
        }


class AssessmentDatasetSerializer(BaseModelSerializer):
    class Meta:
        model = models.AssessmentDataset
        fields = [
            'pk', 'dataset_name', 'description', 'modalities', 'sample_count',
            'label_schema', 'storage_path', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'dataset_name', 'sample_count', 'modalities', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'modalities': {'help_text': "输入JSON数组，例如['voice','vision']"},
            'label_schema': {'help_text': "输入JSON对象描述标签"},
        }


class AssessmentModelSerializer(BaseModelSerializer):
    class Meta:
        model = models.AssessmentModel
        fields = [
            'pk', 'dataset', 'model_name', 'backbone', 'training_params', 'training_status',
            'emotion_metric', 'personality_metric', 'stress_metric', 'last_trained_time',
            'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'model_name', 'dataset', 'training_status',
            'emotion_metric', 'personality_metric', 'stress_metric', 'updated_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'last_trained_time': {'read_only': True},
            'emotion_metric': {'read_only': True},
            'personality_metric': {'read_only': True},
            'stress_metric': {'read_only': True},
        }


class PersonalizedAssessmentSerializer(BaseModelSerializer):
    class Meta:
        model = models.PersonalizedAssessment
        fields = [
            'pk', 'user', 'assessment_model', 'emotion_score', 'personality_profile',
            'stress_level', 'summary', 'recommendations', 'intervention_plan',
            'status', 'signal_snapshot', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'user', 'assessment_model', 'emotion_score',
            'stress_level', 'status', 'updated_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'summary': {'read_only': True},
            'recommendations': {'read_only': True},
            'intervention_plan': {'read_only': True},
            'signal_snapshot': {'write_only': True},
        }


class EmotionFusionEngineSerializer(BaseModelSerializer):
    class Meta:
        model = models.EmotionFusionEngine
        fields = [
            'pk', 'engine_name', 'voice_model', 'vision_model', 'bio_model',
            'fusion_strategy', 'weights', 'latest_accuracy', 'is_active',
            'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'engine_name', 'fusion_strategy', 'latest_accuracy', 'is_active', 'updated_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'latest_accuracy': {'read_only': True},
        }


class ArtGenerationJobSerializer(BaseModelSerializer):
    class Meta:
        model = models.ArtGenerationJob
        fields = [
            'pk', 'therapy', 'prompt', 'style', 'guidance_scale', 'status',
            'output_url', 'preview_image', 'metadata', 'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'therapy', 'style', 'status', 'output_url', 'updated_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'output_url': {'read_only': True},
            'status': {'read_only': True},
        }


class ChatRecordSerializer(BaseModelSerializer):
    class Meta:
        model = models.ChatRecord
        fields = [
            'pk', 'user', 'session_id', 'question', 'answer', 'kb_ref', 'emotion_result',
            'created_time', 'updated_time'
        ]
        table_fields = [
            'pk', 'user', 'session_id', 'question', 'emotion_result', 'created_time'
        ]
        extra_kwargs = {
            'pk': {'read_only': True},
            'answer': {'read_only': True},
            'emotion_result': {'read_only': True},
            # 多外键渲染（按文档规范）
            'user': {
                'attrs': ['pk', 'username'], 'required': True, 'format': "{username}({pk})",
                # 'input_type': 'api-search-user'
            },
            'kb_ref': {
                'attrs': ['pk', 'doc_title'], 'required': False, 'format': "{doc_title}({pk})",
                'input_type': 'api-search-knowledgedoc'
            }
        }