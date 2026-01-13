#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
检查 MySQL 时区配置的脚本
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from django.db import connection

print("=" * 60)
print("MySQL 时区诊断")
print("=" * 60)

try:
    with connection.cursor() as cursor:
        # 检查全局时区
        cursor.execute("SELECT @@global.time_zone, @@session.time_zone, NOW();")
        result = cursor.fetchone()
        print(f"\n1. MySQL 时区设置:")
        print(f"   全局时区: {result[0]}")
        print(f"   会话时区: {result[1]}")
        print(f"   当前时间: {result[2]}")
        
        # 检查时区数据
        cursor.execute("SELECT COUNT(*) FROM mysql.time_zone_name;")
        count = cursor.fetchone()[0]
        print(f"\n2. 时区数据:")
        print(f"   mysql.time_zone_name 表中的记录数: {count}")
        
        if count > 0:
            cursor.execute("SELECT Name FROM mysql.time_zone_name WHERE Name LIKE 'Asia/%' LIMIT 5;")
            zones = cursor.fetchall()
            print(f"   Asia 时区示例: {[z[0] for z in zones]}")
        else:
            print("   ⚠️  时区数据未加载！")
        
        # 检查 Django 设置
        from django.conf import settings
        print(f"\n3. Django 配置:")
        print(f"   TIME_ZONE: {settings.TIME_ZONE}")
        print(f"   USE_TZ: {settings.USE_TZ}")
        
        # 检查数据库配置
        db_config = settings.DATABASES['default']
        print(f"\n4. 数据库配置:")
        print(f"   ENGINE: {db_config['ENGINE']}")
        if 'OPTIONS' in db_config and 'init_command' in db_config['OPTIONS']:
            print(f"   init_command: {db_config['OPTIONS']['init_command']}")
        else:
            print("   ⚠️  init_command 未设置！")
        
        # 测试时区转换
        from django.utils import timezone
        now = timezone.now()
        print(f"\n5. Django 时区测试:")
        print(f"   timezone.now(): {now}")
        print(f"   时区: {timezone.get_current_timezone()}")
        
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

