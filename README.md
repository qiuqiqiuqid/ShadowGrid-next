# ShadowGrid-Next 使用说明

## 📖 快速开始

### 1. 创建 GitHub 仓库

请在 GitHub 上创建名为 `ShadowGrid-next` 的新仓库（或使用您自己的仓库名）。

### 2. 推送代码

在本地仓库目录中执行：

```bash
cd D:/Users/34647/Desktop/myProject/ShadowGrid-Next

# 设置远程仓库（替换为您自己的 GitHub 用户名）
git remote set-url origin https://github.com/YOUR_USERNAME/ShadowGrid-next.git

# 推送代码
git push origin next --force
```

### 3. 获取代码（其他人）

```bash
git clone https://github.com/YOUR_USERNAME/ShadowGrid-next.git
cd ShadowGrid-next
pip install -r requirements.txt
```

---

## 🏗️ 模块化架构说明

ShadowGrid-Next 使用模块化设计，支持：

### 模块类型

| 类型 | 说明 |
|------|------|
| **核心模块** | 必须包含，提供基础功能（ls/cd/pwd/cat/dl/ud/rm/mv/file/find） |
| **可选模块** | 编译时配置加载，如 network/persistence/privilege |
| **精简版** | 仅核心模块，避免杀毒软件识别 |

### 编译配置

编辑 `build_config.cfg` 选择需要的模块：

```ini
[modules]
core = true        # 必选
shell = true       # 必选
screenshot = false # 可选（精简版可禁用）
persistence = false # 可选模块
privilege = false   # 可选模块
credentials = false # 可选模块
network = false     # 可选模块
process = false     # 可选模块
environment = false # 可选模块
logging = false     # 可选模块
```

### 编译客户端

```bash
pyinstaller shadowgrid-next.spec
```

---

## 📁 项目结构

```
ShadowGrid-Next/
├── main.py              # 主程序入口
├── client.py            # 核心客户端（保留原兼容性）
├── admin.py             # 管理终端
├── server.py            # 服务端
├── build_config.cfg     # 编译配置（模块选择）
├── shadowgrid-next.spec # PyInstaller 配置
├── requirements.txt     # Python 依赖
└── docs/               # 文档（后续添加）
    ├── MODULES.md
    ├── ARCHITECTURE.md
    └── TUTORIAL.md
```

---

## ✨ v2.0.0 新特性

- ✅ 模块化架构
- ✅ 编译时模块选择
- ✅ 精简版避免杀毒软件识别
- ✅ 服务端仅数据转发
- ✅ 动态模块加载支持
- ✅ Magisk 风格模块系统
- ✅ Python 3.7 兼容

---

## 🔧 下一步开发

请参考 `MODULES.md` 了解如何开发新模块。
