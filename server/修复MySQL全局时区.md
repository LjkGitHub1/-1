# 修复 MySQL 全局时区

## 诊断结果分析

从诊断脚本的输出可以看到：
- ✅ 会话时区：`+08:00`（Django 的 `init_command` 已生效）
- ❌ 全局时区：`SYSTEM`（需要改为 `+08:00`）
- ⚠️ 时区数据未加载（使用 `+08:00` 不需要，但如果使用命名时区需要）

## 问题原因

MySQL 全局时区仍然是 `SYSTEM`，说明：
1. MySQL 配置文件可能没有正确设置
2. 或者 MySQL 服务没有重启
3. 或者配置文件路径不对

## 解决步骤

### 步骤 1：找到 MySQL 配置文件

```bash
# 方法 1：查找配置文件
mysql --help | grep "Default options" -A 1

# 方法 2：常见位置
ls -la /etc/mysql/mysql.conf.d/mysqld.cnf
ls -la /etc/mysql/my.cnf
ls -la /etc/my.cnf

# 方法 3：在宝塔面板中
# 软件商店 → MySQL → 设置 → 配置修改
```

### 步骤 2：编辑配置文件

**在宝塔面板中：**
1. 软件商店 → MySQL → 设置 → 配置修改
2. 找到 `[mysqld]` 部分
3. 添加或修改：`default-time-zone = '+08:00'`
4. 确保没有注释符号 `#` 在前面
5. 保存

**或使用命令行：**
```bash
# 编辑配置文件（根据实际路径）
nano /etc/mysql/mysql.conf.d/mysqld.cnf
# 或
nano /etc/mysql/my.cnf

# 在 [mysqld] 部分添加：
# default-time-zone = '+08:00'
```

**配置文件示例：**
```ini
[mysqld]
# ... 其他配置 ...
default-time-zone = '+08:00'
# ... 其他配置 ...
```

### 步骤 3：验证配置文件

```bash
# 检查配置文件中是否有设置
grep -i "time-zone" /etc/mysql/mysql.conf.d/mysqld.cnf
# 或
grep -i "time-zone" /etc/mysql/my.cnf
```

应该看到：`default-time-zone = '+08:00'`

### 步骤 4：重启 MySQL

**在宝塔面板中：**
- 软件商店 → MySQL → 重启

**或使用命令行：**
```bash
systemctl restart mysql
# 或
systemctl restart mysqld
```

### 步骤 5：验证全局时区

```bash
mysql -u root -p -e "SELECT @@global.time_zone, @@session.time_zone, NOW();"
```

**应该显示：**
```
+------------------+------------------+---------------------+
| @@global.time_zone | @@session.time_zone | NOW()               |
+------------------+------------------+---------------------+
| +08:00           | +08:00           | 2024-12-03 20:40:00 |
+------------------+------------------+---------------------+
```

如果仍然是 `SYSTEM`，检查：
1. 配置文件路径是否正确
2. MySQL 是否真的重启了
3. 是否有多个配置文件，MySQL 使用了另一个

### 步骤 6：重启 Django 服务

```bash
# 在宝塔面板中重启 Python 项目
# 或使用命令重启 Django 服务
```

### 步骤 7：再次运行诊断

```bash
cd server
python check_timezone.py
```

**应该看到：**
- 全局时区：`+08:00` ✅
- 会话时区：`+08:00` ✅
- 无错误信息 ✅

### 步骤 8：测试 API

```bash
curl http://127.0.0.1:8896/api/system/dashboard/user-login-trend
```

## 如果仍然显示 SYSTEM

### 检查 MySQL 实际使用的配置文件

```bash
# 查看 MySQL 实际使用的配置
mysql -u root -p -e "SHOW VARIABLES LIKE 'basedir';"
mysql -u root -p -e "SHOW VARIABLES LIKE 'datadir';"

# 检查所有可能的配置文件
find /etc -name "*.cnf" -type f 2>/dev/null | grep -i mysql
```

### 直接在 MySQL 中设置（临时方案）

```bash
mysql -u root -p
```

在 MySQL 中执行：
```sql
SET GLOBAL time_zone = '+08:00';
SELECT @@global.time_zone, @@session.time_zone;
```

**注意：** 这只是临时设置，重启 MySQL 后会失效。必须通过配置文件设置才能永久生效。

### 检查是否有多个 MySQL 实例

```bash
# 检查运行的 MySQL 进程
ps aux | grep mysql

# 检查 MySQL 监听的端口
netstat -tlnp | grep mysql
```

## 可选：加载时区数据（如果以后想使用命名时区）

虽然使用 `+08:00` 不需要时区数据，但如果以后想使用 `Asia/Shanghai` 等命名时区，可以加载：

```bash
# 安装工具
apt install mysql-server-core-8.0

# 加载时区数据
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql

# 验证
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```

## 验证清单

- [ ] MySQL 配置文件中有 `default-time-zone = '+08:00'`
- [ ] MySQL 服务已重启
- [ ] `mysql -u root -p -e "SELECT @@global.time_zone;"` 显示 `+08:00`（不是 `SYSTEM`）
- [ ] Django 服务已重启
- [ ] `python check_timezone.py` 显示全局时区为 `+08:00`
- [ ] API 测试正常

