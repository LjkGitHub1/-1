# MySQL 8 时区问题修复指南

## 错误信息
```
Database returned an invalid datetime value. Are time zone definitions for your database installed?
```

## MySQL 8 时区数据修复步骤

### 方法 1：加载时区数据（推荐）

#### 1. 检查时区表是否存在

```bash
mysql -u root -p -e "USE mysql; SHOW TABLES LIKE 'time_zone%';"
```

应该看到：
- `time_zone`
- `time_zone_leap_second`
- `time_zone_name`
- `time_zone_transition`
- `time_zone_transition_type`

#### 2. 检查时区数据是否已加载

```bash
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```

如果返回 0 或表不存在，需要加载时区数据。

#### 3. 加载时区数据

**Linux 系统：**
```bash
# 方法 1：使用系统时区文件（推荐）
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql

# 方法 2：如果方法1失败，尝试指定时区
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql

# 方法 3：只加载特定时区（如果系统没有 /usr/share/zoneinfo）
mysql_tzinfo_to_sql /usr/share/zoneinfo/Asia/Shanghai | mysql -u root -p mysql
```

**如果 `mysql_tzinfo_to_sql` 命令不存在：**
```bash
# 查找命令位置
which mysql_tzinfo_to_sql
# 或
find /usr -name mysql_tzinfo_to_sql 2>/dev/null

# 如果找不到，可能需要安装 MySQL 客户端工具
# Ubuntu/Debian:
sudo apt-get install mysql-client-core-8.0

# CentOS/RHEL:
sudo yum install mysql-community-client
```

#### 4. 验证时区数据

```bash
mysql -u root -p -e "SELECT * FROM mysql.time_zone_name WHERE Name LIKE 'Asia/%' LIMIT 10;"
```

应该能看到时区列表，包括 `Asia/Shanghai`。

### 方法 2：手动设置时区（临时方案）

如果无法加载时区数据，可以手动设置：

```sql
-- 连接到 MySQL
mysql -u root -p

-- 设置全局时区
SET GLOBAL time_zone = '+08:00';

-- 或使用命名时区（需要时区数据已加载）
SET GLOBAL time_zone = 'Asia/Shanghai';

-- 验证
SELECT @@global.time_zone, @@session.time_zone;
```

**注意：** 这需要在 MySQL 配置文件中永久设置，否则重启后会失效。

### 方法 3：在 MySQL 配置文件中设置

编辑 MySQL 配置文件（通常是 `/etc/mysql/my.cnf` 或 `/etc/my.cnf`）：

```ini
[mysqld]
default-time-zone = '+08:00'
# 或
# default-time-zone = 'Asia/Shanghai'
```

然后重启 MySQL：
```bash
sudo systemctl restart mysql
# 或
sudo systemctl restart mysqld
```

### 方法 4：在 Django 数据库配置中设置时区

修改 `server/server/settings/base.py`，在数据库配置中添加时区选项：

```python
if DB_ENGINE == 'mysql':
    DB_OPTIONS['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"
    DB_OPTIONS['charset'] = "utf8mb4"
    DB_OPTIONS['collation'] = "utf8mb4_bin"
    # 添加时区设置
    DB_OPTIONS['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+08:00'"
```

## 验证修复

### 1. 检查 MySQL 时区

```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

### 2. 检查 Django 连接

```bash
cd server
python manage.py shell
```

在 Django shell 中：
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT @@session.time_zone, NOW();")
print(cursor.fetchone())
```

### 3. 测试 API

重启 Django 服务后，测试 API：
```bash
curl http://127.0.0.1:8896/api/system/dashboard/user-login-trend
```

## 常见问题

### Q: `mysql_tzinfo_to_sql` 命令找不到？

A: 安装 MySQL 客户端工具：
```bash
# Ubuntu/Debian
sudo apt-get install mysql-client-core-8.0

# CentOS/RHEL
sudo yum install mysql-community-client
```

### Q: 加载时区数据时提示权限错误？

A: 确保使用 root 用户或有足够权限的用户：
```bash
sudo mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root -p mysql
```

### Q: 时区数据加载后仍然报错？

A: 检查：
1. Django 服务是否已重启
2. 数据库连接是否重新建立
3. MySQL 日志是否有错误

### Q: 如何检查当前 MySQL 时区？

A:
```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone;"
```

## 推荐配置

对于生产环境，推荐：
1. 加载完整的时区数据（方法 1）
2. 在 MySQL 配置文件中设置 `default-time-zone = 'Asia/Shanghai'`
3. 保持 Django 的 `USE_TZ = True`
4. 确保 Django 的 `TIME_ZONE = 'Asia/Shanghai'`

