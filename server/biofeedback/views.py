from django_filters import rest_framework as filters
from rest_framework.decorators import action
from common.core.modelset import BaseModelSet, ImportExportDataAction
from common.core.pagination import DynamicPageNumber
from common.core.response import ApiResponse
from .models import PatientInfo, EegBdfData, PdfReport
from .serializers import PatientInfoSerializer, EegBdfDataSerializer, PdfReportSerializer
from .filters import PatientInfoFilter, EegBdfDataFilter, PdfReportFilter

class PatientInfoViewSet(BaseModelSet, ImportExportDataAction):
    """病人信息管理"""
    queryset = PatientInfo.objects.all()
    serializer_class = PatientInfoSerializer
    filterset_class = PatientInfoFilter
    pagination_class = DynamicPageNumber(1000)
    ordering_fields = ["created_time", "first_visit_time"]

class EegBdfDataViewSet(BaseModelSet, ImportExportDataAction):
    """脑电BDF数据管理"""
    queryset = EegBdfData.objects.all()
    serializer_class = EegBdfDataSerializer
    filterset_class = EegBdfDataFilter
    pagination_class = DynamicPageNumber(1000)
    ordering_fields = ["collect_time", "created_time"]

    @action(methods=["post"], detail=True)
    def analyze(self, request, *args, **kwargs):
        """标记数据为已分析"""
        instance = self.get_object()
        instance.status = 1
        instance.save()
        return ApiResponse(detail=f"{instance.bdf_file_name} 标记为已分析")

class PdfReportViewSet(BaseModelSet, ImportExportDataAction):
    """PDF报告管理"""
    queryset = PdfReport.objects.all()
    serializer_class = PdfReportSerializer
    filterset_class = PdfReportFilter
    pagination_class = DynamicPageNumber(1000)
    ordering_fields = ["generate_time", "created_time"]

    @action(methods=["get"], detail=True)
    def download(self, request, *args, **kwargs):
        """下载报告文件"""
        instance = self.get_object()
        # 实际项目中需添加文件下载逻辑
        return ApiResponse(detail=f"报告 {instance.report_file_name} 下载链接生成成功", 
                          data={"download_url": instance.report_file_path})