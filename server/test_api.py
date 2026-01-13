#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
测试 API 是否正常工作
"""
import os
import sys
import django
import requests

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

print("=" * 60)
print("API 测试")
print("=" * 60)

# 测试的 API 端点
test_apis = [
    "/api/system/dashboard/user-login-trend",
    "/api/system/dashboard/user-login-total",
    "/api/system/dashboard/today-operate-total",
]

base_url = "http://127.0.0.1:8896"

for api_path in test_apis:
    url = base_url + api_path
    print(f"\n测试: {api_path}")
    print("-" * 60)
    
    try:
        response = requests.get(url, timeout=5)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 成功")
            try:
                data = response.json()
                print(f"响应数据: {str(data)[:100]}...")
            except:
                print(f"响应内容: {response.text[:100]}...")
        elif response.status_code == 401:
            print("⚠️  需要认证（这是正常的，说明 API 工作正常）")
        else:
            print(f"❌ 错误: {response.status_code}")
            print(f"响应: {response.text[:200]}")
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：Django 服务可能未运行")
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
    except Exception as e:
        print(f"❌ 错误: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)





