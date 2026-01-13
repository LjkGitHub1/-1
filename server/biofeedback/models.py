from django.db import models
from django.utils import timezone
from common.core.models import DbAuditModel

class PatientInfo(DbAuditModel):
    """病人信息表"""
    medical_record_no = models.CharField(max_length=50, unique=True, verbose_name="病历号")
    patient_name = models.CharField(max_length=50, verbose_name="病人姓名")
    gender = models.SmallIntegerField(choices=[(0, "未知"), (1, "男"), (2, "女")], default=0, verbose_name="性别")
    birth_date = models.DateField(verbose_name="出生日期")
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name="就诊科室")
    first_visit_time = models.DateTimeField(null=True, blank=True, verbose_name="首次就诊时间")
    remark = models.TextField(null=True, blank=True, verbose_name="备注信息")

    class Meta:
        verbose_name = "病人信息"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["patient_name"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return f"{self.patient_name}({self.medical_record_no})"

class EegBdfData(DbAuditModel):
    """脑电数据（BDF）表"""
    patient = models.ForeignKey(PatientInfo, on_delete=models.PROTECT, related_name="eeg_bdfs", verbose_name="关联病人")
    bdf_file_path = models.CharField(max_length=255, verbose_name="文件存储路径")
    bdf_file_name = models.CharField(max_length=100, verbose_name="文件名")
    collect_device = models.CharField(max_length=100, null=True, blank=True, verbose_name="采集设备型号")
    collect_time = models.DateTimeField(verbose_name="数据采集开始时间")
    status = models.SmallIntegerField(choices=[(0, "未处理"), (1, "已分析"), (2, "异常")], default=0, verbose_name="数据状态")

    class Meta:
        verbose_name = "脑电BDF数据"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["collect_time"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.bdf_file_name

class PdfReport(DbAuditModel):
    """PDF报告表"""
    patient = models.ForeignKey(PatientInfo, on_delete=models.PROTECT, related_name="pdf_reports", verbose_name="关联病人")
    bdf_data = models.ForeignKey(EegBdfData, on_delete=models.SET_NULL, null=True, blank=True, related_name="pdf_reports", verbose_name="关联BDF数据")
    report_file_path = models.CharField(max_length=255, verbose_name="文件存储路径")
    report_file_name = models.CharField(max_length=100, verbose_name="文件名")
    report_type = models.CharField(max_length=50, verbose_name="报告类型")
    report_version = models.CharField(max_length=20, verbose_name="报告版本")
    generate_time = models.DateTimeField(verbose_name="报告生成时间")

    class Meta:
        verbose_name = "PDF报告"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["generate_time"]),
            models.Index(fields=["report_type"]),
        ]

    def __str__(self):
        return f"{self.report_type}_{self.report_file_name}"