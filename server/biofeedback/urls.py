from rest_framework.routers import SimpleRouter
from .views import PatientInfoViewSet, EegBdfDataViewSet, PdfReportViewSet

app_name = "biofeedback"
router = SimpleRouter(False)

router.register("patient", PatientInfoViewSet, basename="patient")
router.register("eeg-bdf", EegBdfDataViewSet, basename="eeg-bdf")
router.register("pdf-report", PdfReportViewSet, basename="pdf-report")

urlpatterns = router.urls