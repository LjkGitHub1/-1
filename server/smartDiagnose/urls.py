from rest_framework.routers import SimpleRouter

from smartDiagnose.views import (
    ModelConfigViewSet, KnowledgeBaseViewSet, KnowledgeDocViewSet,
    EmotionRecognitionViewSet, PaintingTherapyViewSet,
    AssessmentDatasetViewSet, AssessmentModelViewSet,
    PersonalizedAssessmentViewSet, EmotionFusionEngineViewSet,
    ArtGenerationJobViewSet, ChatRecordViewSet, DifyWorkflowViewSet,
    ArtTherapyWorkflowViewSet
)

# app_name = 'smartDsupported_type_texiagnose'

app_name = 'smartDiagnose'

# 按文档规范：SimpleRouter设置为False，去掉URL末尾斜线
router = SimpleRouter(False)

# 注册各视图集路由
router.register('model-config', ModelConfigViewSet, basename='model-config')
router.register('knowledge-base', KnowledgeBaseViewSet, basename='knowledge-base')
router.register('knowledge-doc', KnowledgeDocViewSet, basename='knowledge-doc')
router.register('emotion-recognition', EmotionRecognitionViewSet, basename='emotion-recognition')
router.register('painting-therapy', PaintingTherapyViewSet, basename='painting-therapy')
router.register('assessment-dataset', AssessmentDatasetViewSet, basename='assessment-dataset')
router.register('assessment-model', AssessmentModelViewSet, basename='assessment-model')
router.register('personalized-assessment', PersonalizedAssessmentViewSet, basename='personalized-assessment')
router.register('emotion-fusion', EmotionFusionEngineViewSet, basename='emotion-fusion')
router.register('art-generation-job', ArtGenerationJobViewSet, basename='art-generation-job')
router.register('chat-record', ChatRecordViewSet, basename='chat-record')
router.register('dify-workflow', DifyWorkflowViewSet, basename='dify-workflow')
router.register('art-therapy-workflow', ArtTherapyWorkflowViewSet, basename='art-therapy-workflow')

urlpatterns = [
]
urlpatterns += router.urls