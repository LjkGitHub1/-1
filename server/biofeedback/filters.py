from django_filters import rest_framework as filters
from common.core.filter import BaseFilterSet
from .models import PatientInfo, EegBdfData, PdfReport

class PatientInfoFilter(BaseFilterSet):
    patient_name = filters.CharFilter(lookup_expr="icontains", label="病人姓名")
    department = filters.CharFilter(lookup_expr="icontains", label="就诊科室")
    birth_date = filters.DateFromToRangeFilter(label="出生日期范围")

    class Meta:
        model = PatientInfo
        fields = ["patient_name", "gender", "department", "birth_date", "first_visit_time"]

class EegBdfDataFilter(BaseFilterSet):
    patient_name = filters.CharFilter(field_name="patient__patient_name", lookup_expr="icontains", label="病人姓名")
    collect_time = filters.DateTimeFromToRangeFilter(label="采集时间范围")
    collect_device = filters.CharFilter(lookup_expr="icontains", label="采集设备")

    class Meta:
        model = EegBdfData
        fields = ["patient", "collect_device", "collect_time", "status"]

class PdfReportFilter(BaseFilterSet):
    patient_name = filters.CharFilter(field_name="patient__patient_name", lookup_expr="icontains", label="病人姓名")
    generate_time = filters.DateTimeFromToRangeFilter(label="生成时间范围")
    report_type = filters.CharFilter(lookup_expr="icontains", label="报告类型")

    class Meta:
        model = PdfReport
        fields = ["patient", "bdf_data", "report_type", "report_version", "generate_time"]