from django.urls import path, include

URLPATTERNS = [
    path('api/biofeedback/', include('biofeedback.urls')),
]

PERMISSION_WHITE_REURL = {
    "^/api/biofeedback/.*": ['*'],  # 暂时取消 biofeedback 接口的权限验证，允许外部直接访问
}