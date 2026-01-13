# 多模态心理测评系统

基于 Django + Vue3 构建的智能心理测评与诊疗平台，集成多模态数据融合、大语言模型、知识图谱等前沿技术，提供从数据采集、智能评估到个性化干预的完整解决方案。

## 📋 项目简介

本系统是一个综合性的心理测评平台，通过多模态数据融合技术，整合文本、语音、图像、生理信号等多种数据源，实现精准的心理健康评估和个性化的干预方案制定。

### 核心特性

- 🧠 **多模态数据融合**：支持文本、语音、图像、脑电、近红外等多种模态数据的统一管理
- 🤖 **AI智能诊疗**：集成大语言模型、知识图谱、情绪识别等AI技术
- 📊 **个性化评估**：基于多模态数据生成科学的心理评估报告
- 🎯 **精准干预**：根据评估结果制定个性化的干预方案
- 🔒 **权限管理**：基于RBAC的完善权限控制系统
- 📱 **现代化UI**：基于Vue3 + Element Plus的现代化前端界面

## 🏗️ 技术架构

### 前端 (client)
- **框架**: Vue 3 + TypeScript
- **UI组件**: Element Plus
- **状态管理**: Pinia
- **构建工具**: Vite
- **代码规范**: ESLint + Prettier

### 后端 (server)
- **框架**: Django + Django REST Framework
- **数据库**: MySQL/PostgreSQL
- **缓存**: Redis
- **任务队列**: Celery
- **API文档**: Swagger/OpenAPI

## 📦 项目结构

```
beyourself/
├── client/          # 前端项目
│   ├── src/        # 源代码
│   ├── public/     # 静态资源
│   └── ...
├── server/          # 后端项目
│   ├── common/     # 公共模块
│   ├── system/     # 系统管理模块
│   ├── smartDiagnose/  # 智慧诊疗模块
│   ├── personalize/    # 个性化评估模块
│   ├── biofeedback/    # 生物反馈模块
│   └── ...
└── README.md        # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+ / PostgreSQL 12+
- Redis 6.0+

### 后端启动

```bash
cd server

# 安装依赖
pip install -r requirements.txt

# 配置数据库（修改 config.yml）
# 执行数据库迁移
python manage.py migrate

# 启动服务
python manage.py runserver 0.0.0.0:8896
```

### 前端启动

```bash
cd client

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

详细部署文档请参考：
- [后端部署文档](server/README.md)
- [前端部署文档](client/README.md)

## 📚 核心模块

### 1. 个性化评估与干预模块
- 多模态数据管理
- 评估报告生成
- 干预方案制定

### 2. 智慧诊疗模块
- 模型配置管理
- 知识库管理
- 多模态情绪识别
- 智能心理问答
- 艺术治疗配置

详细模块介绍请参考：[系统模块介绍文档.md](系统模块介绍文档.md)

## 🔧 开发规范

- 代码风格遵循项目配置的 ESLint/Prettier 规则
- 提交信息遵循 Conventional Commits 规范
- API 接口遵循 RESTful 设计规范

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**注意**: 本项目基于 [xadmin](https://github.com/nineaiyu/xadmin-server) 二次开发，专注于多模态心理测评领域。

