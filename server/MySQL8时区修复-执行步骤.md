# MySQL 8 时区修复 - 执行步骤

## 当前状态
- `mysql_tzinfo_to_sql` 命令不存在
- `mysql.time_zone_name` 表为空（0 条记录）

## 解决方案

### 方案 1：安装 mysql-server-core-8.0 并加载时区数据（推荐）

#### 步骤 1：安装 mysql-server-core-8.0

```bash
apt install mysql-server-core-8.0
```

#### 步骤 2：加载时区数据

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

输入 MySQL root 密码后，时区数据将被加载。

#### 步骤 3：验证时区数据

```bash
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```

应该返回一个大于 0 的数字（通常是 1000+）。

```bash
mysql -u root -p -e "SELECT * FROM mysql.time_zone_name WHERE Name LIKE 'Asia/%' LIMIT 5;"
```

应该能看到时区列表。

### 方案 2：直接在 MySQL 配置文件中设置时区（快速方案）

如果不想安装额外的包，可以直接在 MySQL 配置文件中设置时区。

#### 步骤 1：编辑 MySQL 配置文件

```bash
# 查找 MySQL 配置文件位置
mysql --help | grep "Default options" -A 1

# 通常位置：
# /etc/mysql/my.cnf
# /etc/my.cnf
# /etc/mysql/mysql.conf.d/mysqld.cnf
```

编辑配置文件（使用宝塔面板或命令行）：

```bash
nano /etc/mysql/mysql.conf.d/mysqld.cnf
# 或
nano /etc/mysql/my.cnf
```

在 `[mysqld]` 部分添加：

```ini
[mysqld]
default-time-zone = '+08:00'
```

#### 步骤 2：重启 MySQL

```bash
systemctl restart mysql
# 或
systemctl restart mysqld
```

#### 步骤 3：验证时区设置

```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

应该显示：
```
+------------------+------------------+---------------------+
| @@global.time_zone | @@session.time_zone | NOW()               |
+------------------+------------------+---------------------+
| +08:00           | +08:00           | 2024-12-03 20:30:00 |
+------------------+------------------+---------------------+
```

### 方案 3：使用 SQL 直接设置（临时方案）

如果无法修改配置文件，可以在 MySQL 中直接设置：

```bash
mysql -u root -p
```

在 MySQL 中执行：

```sql
SET GLOBAL time_zone = '+08:00';
SELECT @@global.time_zone, @@session.time_zone;
```

**注意：** 这个设置会在 MySQL 重启后失效，需要配合配置文件使用。

## 推荐操作流程

### 快速修复（5 分钟）

1. **安装 mysql-server-core-8.0：**
   ```bash
   apt install mysql-server-core-8.0
   ```

2. **加载时区数据：**
   ```bash
   mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
   ```

3. **在 MySQL 配置文件中设置默认时区：**
   ```bash
   # 编辑配置文件
   nano /etc/mysql/mysql.conf.d/mysqld.cnf
   # 添加：default-time-zone = '+08:00'
   ```

4. **重启 MySQL：**
   ```bash
   systemctl restart mysql
   ```

5. **验证：**
   ```bash
   mysql -u root -p -e "SELECT @@global.time_zone, COUNT(*) FROM mysql.time_zone_name;"
   ```

6. **重启 Django 服务**

### 仅配置文件方案（如果不想安装额外包）

1. **编辑 MySQL 配置文件，添加 `default-time-zone = '+08:00'`**
2. **重启 MySQL**
3. **重启 Django 服务**

## 验证修复

### 1. 检查 MySQL 时区

```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

### 2. 检查时区数据（如果已加载）

```bash
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```

### 3. 测试 Django API

重启 Django 服务后：
```bash
curl http://127.0.0.1:8896/api/system/dashboard/user-login-trend
```

## 注意事项

1. **Django 配置已更新：** `server/server/settings/base.py` 已修改，会在连接时自动设置时区
2. **重启服务：** 修改 MySQL 配置后，必须重启 MySQL 和 Django 服务
3. **时区数据 vs 时区设置：**
   - 加载时区数据：可以使用命名时区（如 `Asia/Shanghai`）
   - 仅设置时区：只能使用偏移量（如 `+08:00`）
   - 对于 Django，两种方式都可以工作

## 如果仍然报错

1. 检查 Django 日志，查看具体错误信息
2. 确认 MySQL 服务已重启
3. 确认 Django 服务已重启
4. 检查 Django 数据库连接配置是否正确

