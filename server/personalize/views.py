from django_filters import rest_framework as filters
from rest_framework.decorators import action
from common.core.filter import BaseFilterSet
from common.core.modelset import BaseModelSet, ImportExportDataAction
from common.core.pagination import DynamicPageNumber
from common.core.response import ApiResponse
from common.utils import get_logger
from personalize.models import AssessmentReport, InterventionPlan
from personalize.serializers import AssessmentReportSerializer, InterventionPlanSerializer

logger = get_logger(__name__)


# 评估报告过滤器
class AssessmentReportFilter(BaseFilterSet):
    report_no = filters.CharFilter(field_name='report_no', lookup_expr='icontains')
    assess_type = filters.CharFilter(field_name='assess_type', lookup_expr='icontains')
    core_conclusion = filters.CharFilter(field_name='core_conclusion', lookup_expr='icontains')

    class Meta:
        model = AssessmentReport
        fields = ['report_no', 'assess_type', 'risk_level', 'report_status', 'user', 'assessor', 'assess_date', 'created_time']


# 评估报告视图集
class AssessmentReportViewSet(BaseModelSet, ImportExportDataAction):
    """评估报告"""  # 必须添加注释，用于菜单显示和日志记录

    queryset = AssessmentReport.objects.all()
    serializer_class = AssessmentReportSerializer
    ordering_fields = ['assess_date', 'created_time']
    filterset_class = AssessmentReportFilter
    pagination_class = DynamicPageNumber(1000)  # 最大分页1000条

    @action(methods=['post'], detail=True)
    def archive(self, request, *args, **kwargs):
        """归档评估报告"""  # 操作注释必填

        instance = self.get_object()
        instance.report_status = AssessmentReport.StatusChoices.ARCHIVED
        instance.save()
        return ApiResponse(detail=f"报告{instance.report_no}已归档")


# 干预方案过滤器
class InterventionPlanFilter(BaseFilterSet):
    plan_no = filters.CharFilter(field_name='plan_no', lookup_expr='icontains')
    plan_title = filters.CharFilter(field_name='plan_title', lookup_expr='icontains')
    intervention_type = filters.CharFilter(field_name='intervention_type', lookup_expr='icontains')

    class Meta:
        model = InterventionPlan
        fields = ['plan_no', 'plan_title', 'intervention_type', 'plan_status', 'user', 'report', 'start_date', 'created_time']


# 干预方案视图集
class InterventionPlanViewSet(BaseModelSet, ImportExportDataAction):
    """干预方案"""

    queryset = InterventionPlan.objects.all()
    serializer_class = InterventionPlanSerializer
    ordering_fields = ['start_date', 'created_time']
    filterset_class = InterventionPlanFilter
    pagination_class = DynamicPageNumber(1000)

    @action(methods=['post'], detail=True)
    def start(self, request, *args, **kwargs):
        """启动干预方案"""

        instance = self.get_object()
        instance.plan_status = InterventionPlan.StatusChoices.IN_PROGRESS
        instance.save()
        return ApiResponse(detail=f"方案{instance.plan_no}已启动")