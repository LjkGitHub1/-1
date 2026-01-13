#!/usr/bin/env python
# -*- coding:utf-8 -*-
# project : xadmin-server
# filename : util
# author : ly_13
# date : 8/10/2024

from django.utils import timezone

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from common.utils import get_logger

logger = get_logger(__name__)


class CaptchaAuth(object):
    def __init__(self, captcha_key='', request=None):
        self.captcha_key = captcha_key
        self.request = request

    def __get_captcha_obj(self):
        return CaptchaStore.objects.filter(hashkey=self.captcha_key).first()

    def generate(self):
        self.captcha_key = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(self.captcha_key)
        
        # 检查是否通过代理访问（有 X-Forwarded-Host 头）
        if self.request:
            forwarded_host = self.request.META.get('HTTP_X_FORWARDED_HOST', '')
            if forwarded_host:
                # 通过代理访问，使用相对路径，让前端通过 Nginx 代理访问
                # 这样避免 CORS 问题，前端会使用当前域名访问
                pass  # 保持相对路径，不构建绝对 URL
            else:
                # 直接访问（开发环境），使用 build_absolute_uri
                try:
                    captcha_image = self.request.build_absolute_uri(captcha_image)
                except Exception as e:
                    logger.warning(f"Failed to build absolute URI: {e}, using relative path")
                    # 如果构建失败，使用相对路径
                    pass
        
        captcha_obj = self.__get_captcha_obj()
        code_length = 0
        if captcha_obj:
            code_length = len(captcha_obj.response)
        return {"captcha_image": captcha_image, "captcha_key": self.captcha_key, "length": code_length}

    def valid(self, verify_code):
        try:
            CaptchaStore.objects.get(
                response=verify_code.strip(" ").lower(), hashkey=self.captcha_key, expiration__gt=timezone.now()
            ).delete()
        except CaptchaStore.DoesNotExist:
            return False
        return True
