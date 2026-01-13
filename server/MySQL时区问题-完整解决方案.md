# MySQL 时区问题 - 完整解决方案

## 问题诊断

首先运行诊断脚本检查当前状态：

```bash
cd server
python check_timezone.py
```

## 完整解决步骤

### 步骤 1：验证 MySQL 时区设置

```bash
# 检查 MySQL 全局时区
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

**应该显示：**
```
+------------------+------------------+---------------------+
| @@global.time_zone | @@session.time_zone | NOW()               |
+------------------+------------------+---------------------+
| +08:00           | +08:00           | 2024-12-03 20:30:00 |
+------------------+------------------+---------------------+
```

如果显示 `SYSTEM` 或其他值，需要继续配置。

### 步骤 2：确保 MySQL 配置文件已设置

**在宝塔面板中：**
1. 软件商店 → MySQL → 设置 → 配置修改
2. 找到 `[mysqld]` 部分
3. 确保有：`default-time-zone = '+08:00'`
4. 保存并重启 MySQL

**或使用命令行：**
```bash
# 编辑配置文件
nano /etc/mysql/mysql.conf.d/mysqld.cnf

# 在 [mysqld] 部分添加：
# default-time-zone = '+08:00'

# 重启 MySQL
systemctl restart mysql
```

### 步骤 3：验证 MySQL 配置生效

```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

### 步骤 4：检查 Django 配置

已更新 `server/server/settings/base.py`，确保：
- `DB_OPTIONS['init_command']` 包含时区设置
- 配置在 `DATABASES` 定义之前设置

### 步骤 5：重启 Django 服务（重要！）

**必须重启 Django 服务才能应用新配置：**

```bash
# 根据您的部署方式选择：

# 方式 1：如果使用 systemd
sudo systemctl restart your-django-service

# 方式 2：如果使用 supervisor
sudo supervisorctl restart your-django-service

# 方式 3：如果使用宝塔面板
# 在宝塔面板中重启 Python 项目

# 方式 4：如果使用 gunicorn 直接运行
# 找到进程并重启
ps aux | grep gunicorn
kill -HUP <pid>
```

### 步骤 6：清除连接池（如果问题仍然存在）

如果 Django 使用了连接池（`CONN_MAX_AGE > 0`），可能需要：

**临时方案：** 将 `CONN_MAX_AGE` 设为 0，强制每次重新连接：

```python
# 在 server/server/settings/base.py 中
'CONN_MAX_AGE': 0,  # 临时设为 0，测试后可以改回 600
```

**或重启 Django 服务**，这会清除所有连接池。

### 步骤 7：验证修复

```bash
# 1. 运行诊断脚本
cd server
python check_timezone.py

# 2. 测试 API
curl http://127.0.0.1:8896/api/system/dashboard/user-login-trend

# 3. 在 Django shell 中测试
python manage.py shell
```

在 Django shell 中：
```python
from django.db import connection
from django.utils import timezone

# 检查数据库时区
cursor = connection.cursor()
cursor.execute("SELECT @@session.time_zone, NOW();")
print(cursor.fetchone())

# 检查 Django 时区
print(timezone.now())
```

## 常见问题排查

### Q1: MySQL 时区显示为 SYSTEM

**原因：** MySQL 配置文件未设置或未重启

**解决：**
1. 检查配置文件是否有 `default-time-zone = '+08:00'`
2. 确保 MySQL 已重启
3. 验证：`mysql -u root -p -e "SELECT @@global.time_zone;"`

### Q2: Django 仍然报错

**可能原因：**
1. Django 服务未重启
2. 连接池缓存了旧连接
3. `init_command` 未正确执行

**解决：**
1. **强制重启 Django 服务**
2. 临时设置 `CONN_MAX_AGE = 0` 测试
3. 检查 Django 日志，查看具体错误

### Q3: init_command 未执行

**检查方法：**
```python
# 在 Django shell 中
from django.conf import settings
print(settings.DATABASES['default']['OPTIONS'].get('init_command'))
```

**如果为空，检查：**
- `DB_ENGINE` 是否为 'mysql'
- `DB_OPTIONS` 是否在 `DATABASES` 定义之前设置

### Q4: 时区数据未加载

如果使用命名时区（如 `Asia/Shanghai`），需要加载时区数据：

```bash
# 安装工具
apt install mysql-server-core-8.0

# 加载时区数据
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

但使用 `+08:00` 不需要时区数据。

## 推荐配置检查清单

- [ ] MySQL 配置文件中有 `default-time-zone = '+08:00'`
- [ ] MySQL 服务已重启
- [ ] `mysql -u root -p -e "SELECT @@global.time_zone;"` 显示 `+08:00`
- [ ] Django 配置中 `DB_OPTIONS['init_command']` 包含时区设置
- [ ] Django 服务已重启
- [ ] 运行 `python check_timezone.py` 无错误
- [ ] API 测试正常

## 如果仍然无法解决

1. **运行诊断脚本：** `python check_timezone.py`
2. **检查 Django 日志：** 查看具体错误信息
3. **检查 MySQL 日志：** `/var/log/mysql/error.log`
4. **临时禁用时区：** 将 `USE_TZ = False`（不推荐，仅用于测试）

