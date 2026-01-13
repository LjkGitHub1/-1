from rest_framework import serializers
from common.core.serializers import BaseModelSerializer
from common.fields.utils import input_wrapper
from .models import PatientInfo, EegBdfData, PdfReport

class PatientInfoSerializer(BaseModelSerializer):
    class Meta:
        model = PatientInfo
        fields = ["pk", "medical_record_no", "patient_name", "gender", "birth_date", 
                  "contact_phone", "department", "first_visit_time", "remark", "created_time", "updated_time"]
        table_fields = ["pk", "medical_record_no", "patient_name", "gender", "birth_date", 
                        "department", "first_visit_time", "created_time"]
        extra_kwargs = {"pk": {"read_only": True}}

class EegBdfDataSerializer(BaseModelSerializer):
    patient_name = serializers.CharField(source="patient.patient_name", read_only=True, label="病人姓名")
    patient_id = serializers.IntegerField(source="patient.pk", write_only=True, label="病人ID")

    class Meta:
        model = EegBdfData
        fields = ["pk", "patient", "patient_id", "patient_name", "bdf_file_path", "bdf_file_name", 
                  "collect_device", "collect_time", "status", "created_time"]
        table_fields = ["pk", "patient_name", "bdf_file_name", "collect_device", "collect_time", "status", "created_time"]
        extra_kwargs = {
            "pk": {"read_only": True},
            "patient": {"read_only": True},
            "patient_id": {"required": True}
        }

class PdfReportSerializer(BaseModelSerializer):
    patient_name = serializers.CharField(source="patient.patient_name", read_only=True, label="病人姓名")
    patient_id = serializers.IntegerField(source="patient.pk", write_only=True, label="病人ID")
    bdf_file_name = serializers.CharField(source="bdf_data.bdf_file_name", read_only=True, label="关联BDF文件名")
    bdf_id = serializers.IntegerField(source="bdf_data.pk", write_only=True, required=False, label="BDF数据ID")

    class Meta:
        model = PdfReport
        fields = ["pk", "patient", "patient_id", "patient_name", "bdf_data", "bdf_id", "bdf_file_name",
                  "report_file_path", "report_file_name", "report_type", "report_version", 
                  "generate_time", "created_time"]
        table_fields = ["pk", "patient_name", "bdf_file_name", "report_type", "report_version", "generate_time", "created_time"]
        extra_kwargs = {
            "pk": {"read_only": True},
            "patient": {"read_only": True},
            "bdf_data": {"read_only": True}
        }