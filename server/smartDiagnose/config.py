from django.urls import path, include
# 在 smartDiagnose/apps.py 同级目录下创建 config.py 文件
# from .urls import urlpatterns as URLPATTERNS

# 按文档规范：路由配置，自动注入总服务
URLPATTERNS = [
    path('api/smartDiagnose/', include('smartDiagnose.urls', namespace='smartDiagnose')),
]

# 按文档规范：请求白名单，支持正则
PERMISSION_WHITE_REURL = [
    # 示例：开放问答请求接口无需权限
    r'^api/smartDiagnose/chat-record/send_question/$',
]

# 注意：Dify 工作流配置已移至 views.py 中，避免循环导入
# Dify 固定地址：http://36.134.27.102:8082/