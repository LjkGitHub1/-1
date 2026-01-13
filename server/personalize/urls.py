#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : server
# filename : urls
# author : ly_13
# date : 6/6/2023
from rest_framework.routers import SimpleRouter

from personalize.views import AssessmentReportViewSet, InterventionPlanViewSet

app_name = 'personalize'

router = SimpleRouter(False)  # 设置为 False ,为了去掉url后面的斜线

# 评估报告类路由
router.register('assessment_report', AssessmentReportViewSet, basename='assessment_report')
# 干预方案类路由
router.register('intervention_plan', InterventionPlanViewSet, basename='intervention_plan')

urlpatterns = [
]
urlpatterns += router.urls
