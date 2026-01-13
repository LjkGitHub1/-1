#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xadmin-server
# filename : file
# author : ly_13
# date : 7/24/2024

import os
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from drf_spectacular.plumbing import build_object_type, build_basic_type, build_array_type
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiRequest, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

from common.core.config import SysConfig, UserConfig
from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet
from common.core.response import ApiResponse
from common.core.throttle import UploadThrottle
from common.swagger.utils import get_default_response_schema
from common.utils import get_logger
from system.models import UploadFile
from system.serializers.upload import UploadFileSerializer

logger = get_logger(__name__)


def get_upload_max_size(user_obj):
    return min(SysConfig.FILE_UPLOAD_SIZE, UserConfig(user_obj).FILE_UPLOAD_SIZE)

# 定义文件类型分类
FILE_TYPE_CATEGORIES = {
    '音频': {
        'extensions': {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus'},
    },
    '图片': {
        'extensions': {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'},
    },
    '视频': {
        'extensions': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m3u8'},
    },
    '文本': {
        'extensions': {
            '.txt', '.csv', '.json', '.xml', '.md', '.log', '.html', '.css', '.js',
            '.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.pptx', '.rtf',
            '.tex', '.odt', '.ods', '.odp', '.pages', '.numbers'
        },
    },
    '脑电': {
        'extensions': {'.edf', '.bdf', '.set', '.fdt', '.eeg', '.vhdr', '.vmrk','.e'},
    },
    '近红外': {
        'extensions': {'.snirf', '.nirs', '.hdr','.oxy'},
    }
}

# 文件分类
def classify_file_type(filename: str) -> str:
    """
    Classify file into specific data types
    Returns: 'audio', 'image', 'video', 'text', 'eeg', 'nirs', or 'other'
    """
    # Get file extension
    _, ext = os.path.splitext(filename.lower())
    
    # Check each category
    for category, info in FILE_TYPE_CATEGORIES.items():
        if ext in info['extensions']:
            return category
    
    return 'other'



class UploadFileFilter(BaseFilterSet):
    filename = filters.CharFilter(field_name='filename', lookup_expr='icontains')

    class Meta:
        model = UploadFile
        fields = ['filename', 'mime_type', 'md5sum', 'description', 'is_upload', 'is_tmp']


class UploadFileViewSet(BaseModelSet):
    """文件"""
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer
    ordering_fields = ['created_time', 'filesize']
    filterset_class = UploadFileFilter

    @extend_schema(
        responses=get_default_response_schema({
            'data': build_object_type(
                properties={
                    'file_upload_size': build_basic_type(OpenApiTypes.NUMBER),
                }
            )
        })
    )
    @action(methods=['get'], detail=False)
    def config(self, request, *args, **kwargs):
        """获取上传配置"""
        return ApiResponse(data={'file_upload_size': get_upload_max_size(request.user)})

    @extend_schema(
        description="文件上传",
        request=OpenApiRequest(
            build_object_type(properties={'file': build_array_type(build_basic_type(OpenApiTypes.BINARY))})
        ),
        responses={
            200: inline_serializer(name='result', fields={
                'code': serializers.IntegerField(),
                'detail': serializers.CharField(),
                'data': UploadFileSerializer(many=True)
            })
        }
    )
    @action(methods=['post'], detail=False, throttle_classes=[UploadThrottle, ], parser_classes=(MultiPartParser,))
    def upload(self, request, *args, **kwargs):
        """上传文件"""

        files = request.FILES.getlist('file', [])
        user_id = request.data.get('user_id')
        description = request.data.get('description', '')
        result = []
        file_upload_max_size = get_upload_max_size(request.user)
        
        # 验证用户ID是否存在（如果提供）
        user_obj = None
        if user_id:
            try:
                from system.models import UserInfo
                user_obj = UserInfo.objects.get(pk=user_id)
            except UserInfo.DoesNotExist:
                return ApiResponse(code=1004, detail=_("User not found"))
        
        for file_obj in files:
            try:
                if file_obj.size > file_upload_max_size:
                    return ApiResponse(code=1003,
                                       detail=_("upload file size cannot exceed {}").format(file_upload_max_size))
            except Exception as e:
                logger.error(f"user:{request.user} upload file type error Exception:{e}")
                return ApiResponse(code=1002, detail=_("Wrong upload file type"))
            
            # Classify file type
            file_type = classify_file_type(file_obj.name)
            
            obj = UploadFile.objects.create(
                creator=request.user, 
                filename=file_obj.name, 
                is_upload=True, 
                is_tmp=True,
                filepath=file_obj, 
                mime_type=file_obj.content_type, 
                filesize=file_obj.size, 
                file_type=file_type,
                description=description,
                user=user_obj
            )
            result.append(obj)
        return ApiResponse(data=self.get_serializer(result, many=True).data)
