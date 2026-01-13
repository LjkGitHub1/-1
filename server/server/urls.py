"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import mimetypes
import os

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import finders
from django.urls import include, re_path
from django.views.static import serve as static_serve

from common.celery.flower import CeleryFlowerAPIView
from common.core.utils import auto_register_app_url
from common.swagger.views import JsonApi, SwaggerUI, Redoc
from common.utils.media import media_serve

swagger_apis = [
    re_path('^api-docs/schema/', JsonApi.as_view(), name='schema'),
    re_path('^api-docs/swagger/$', SwaggerUI.as_view(url_name='schema'), name='swagger-ui'),
    re_path('^api-docs/redoc/$', Redoc.as_view(url_name='schema'), name='schema-redoc'),
]

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^api/common/', include('common.urls', namespace='common')),
    re_path('^api/system/', include('system.urls', namespace='system')),
    re_path('^api/settings/', include('settings.urls', namespace='settings')),
    re_path('^api/notifications/', include('notifications.urls', namespace='notifications')),
    re_path('^api/flower/(?P<path>.*)$', CeleryFlowerAPIView.as_view(), name='flower-view'),
    # media路径配置 开发环境可以启动下面配置，正式环境需要让nginx读取资源，无需进行转发
    re_path('^media/(?P<path>.*)$', media_serve, {'document_root': settings.MEDIA_ROOT}),
]

# 靜態文件配置：使用 staticfiles 查找器和 STATIC_ROOT
def staticfiles_serve_view(request, path):
    """提供靜態文件，支持開發和生產環境"""
    from django.http import Http404, HttpResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    # 優先從 STATIC_ROOT 提供（生產環境，collectstatic 後的文件）
    static_root_path = os.path.join(settings.STATIC_ROOT, path)
    logger.debug(f"Looking for static file: path={path}, static_root_path={static_root_path}, exists={os.path.exists(static_root_path)}")
    
    if os.path.exists(static_root_path) and os.path.isfile(static_root_path):
        try:
            # 直接讀取文件並返回，避免 static_serve 的路徑問題
            with open(static_root_path, 'rb') as f:
                content = f.read()
            response = HttpResponse(content)
            # 設置 Content-Type
            content_type, _ = mimetypes.guess_type(static_root_path)
            if content_type:
                response['Content-Type'] = content_type
            elif path.endswith('.js'):
                response['Content-Type'] = 'application/javascript; charset=utf-8'
            elif path.endswith('.css'):
                response['Content-Type'] = 'text/css; charset=utf-8'
            elif path.endswith('.png'):
                response['Content-Type'] = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                response['Content-Type'] = 'image/jpeg'
            elif path.endswith('.svg'):
                response['Content-Type'] = 'image/svg+xml'
            response['Cache-Control'] = 'public, max-age=3600'
            logger.debug(f"Serving static file from STATIC_ROOT: {static_root_path}")
            return response
        except (IOError, OSError) as e:
            logger.error(f"Error reading file {static_root_path}: {e}")
            pass
    
    # 使用 finders 查找靜態文件（開發環境，從應用程序中查找）
    static_file = finders.find(path)
    if static_file and os.path.isfile(static_file):
        try:
            with open(static_file, 'rb') as f:
                content = f.read()
            response = HttpResponse(content)
            # 設置 Content-Type
            content_type, _ = mimetypes.guess_type(static_file)
            if content_type:
                response['Content-Type'] = content_type
            elif path.endswith('.js'):
                response['Content-Type'] = 'application/javascript; charset=utf-8'
            elif path.endswith('.css'):
                response['Content-Type'] = 'text/css; charset=utf-8'
            response['Cache-Control'] = 'public, max-age=3600'
            logger.debug(f"Serving static file from finders: {static_file}")
            return response
        except (IOError, OSError) as e:
            logger.error(f"Error reading file {static_file}: {e}")
            pass
    
    # 如果找不到，返回 404
    logger.warning(f"Static file not found: path={path}, STATIC_ROOT={settings.STATIC_ROOT}")
    raise Http404(f"Static file '{path}' not found")

# 靜態文件 URL 必須在 swagger_apis 之前，確保優先匹配
# 統一使用 staticfiles_serve_view，它會自動處理開發和生產環境
# 開發環境：使用 finders 查找應用程序中的靜態文件
# 生產環境：如果 finders 找不到，會從 STATIC_ROOT 提供（collectstatic 後的文件）
urlpatterns = [
    re_path('^api/static/(?P<path>.*)$', staticfiles_serve_view),
] + urlpatterns

urlpatterns = swagger_apis + urlpatterns
auto_register_app_url(urlpatterns)
