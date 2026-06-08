# BlenderDeepSeek - Blender 深度搜索 AI 插件

![Header](https://user-images.githubusercontent.com/63528145/227160213-6862cd5e-b31f-43ea-a5e5-6cc340a95617.png)

## 📖 项目简介

Blender 可以通过 Python 脚本进行程序控制。如今以 DeepSeek 为代表的大语言模型，能够根据简单的自然语言生成这些 Python 脚本并完成执行。

本插件提供了简易易用的交互界面，将 DeepSeek 模型直接集成到 Blender 软件界面中，你可以使用自然语言指令来操控 Blender。

## ⚠️ 重要注意事项

本插件调用 DeepSeek 模型无需等待名单申请，仅需使用对应的 DeepSeek API 密钥即可使用。

**重要：** DeepSeek API 调用与网页端 DeepSeek 网页聊天账号不互通。本插件仅在你拥有自己的 DeepSeek API Key 密钥后才可正常使用全部功能。

## 📦 安装方法

### 方法 1：从仓库安装（推荐）

1. 在 GitHub 页面点击 `Code > Download ZIP` 下载本仓库
2. 打开 Blender，依次打开 `编辑 > 偏好设置 > 附加组件 > 安装`
3. 选中下载好的 ZIP 文件，点击 `安装附加组件`
4. 勾选 `DeepSeek Blender 助手` 对应的复选框，启用插件
5. 在插件偏好设置界面，粘贴你的 DeepSeek API 密钥
6. 如需实时查看代码生成过程，打开 `窗口 > 切换系统控制台`

### 方法 2：手动安装

1. 下载本文件夹到你的本地
2. 将 `BlenderDeepSeek` 文件夹复制到 Blender 的附加组件目录：
   - Windows: `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons`
   - macOS: `~/Library/Application Support/Blender/[version]/scripts/addons`
   - Linux: `~/.config/blender/[version]/scripts/addons`
3. 在 Blender 中启用插件

## 🚀 使用方法

1. 在 3D 视图界面打开侧边栏（未显示时按下快捷键 `N`），找到 `DeepSeek 助手` 选项卡
2. 在输入框内输入自然语言指令，例如：`在坐标原点创建一个立方体`
3. 点击 `执行` 按钮，插件将自动生成 Blender Python 代码并运行

### 示例指令

```
在原点创建一个立方体
创建一个球形并设置材质为红色
生成 10 个随机位置的物体
制作一个旋转动画
```

## ✅ 运行要求

- **Blender 版本**：3.1 或更高版本
- **DeepSeek API 密钥**：访问 https://platform.deepseek.com/api_keys 获取
- **网络连接**：需要连接到 DeepSeek API 服务

## ⭐ 功能特性

- 🎨 支持 `DeepSeek Chat` 和 `DeepSeek Reasoner` 两种模型
- 🌐 完全支持**中文**输入和输出
- 💬 保留对话历史，支持上下文理解
- 📝 实时显示生成的代码
- 🚀 一键执行生成的 Blender Python 代码
- 💰 比 GPT-4 更便宜的成本
- ⚡ 无需等待列表，开箱即用

## 📊 与 BlenderGPT 的区别

| 特性 | BlenderGPT (OpenAI) | BlenderDeepSeek |
|------|-------------------|----------------|
| **API 提供商** | OpenAI | DeepSeek |
| **模型** | GPT-4, GPT-3.5-Turbo | DeepSeek Chat, DeepSeek Reasoner |
| **申请门槛** | 需等待列表 | 无需申请 |
| **支持语言** | 英文优先 | 英文/中文 |
| **成本** | 较高 | 低廉 |
| **开箱即用** | 否 | 是 |

## 🔑 获取 API Key

### 步骤

1. 访问 [DeepSeek API 平台](https://platform.deepseek.com)
2. 点击 `注册` 或 `登录`
3. 完成账户验证
4. 进入 [API Keys 页面](https://platform.deepseek.com/api_keys)
5. 点击 `创建新的 API Key`
6. 复制生成的 API Key
7. 将 API Key 粘贴到 Blender 插件的偏好设置中

### 价格信息

DeepSeek API 相比 OpenAI 的 GPT-4 更经济：
- **DeepSeek Chat**：更快的响应速度，适合日常任务
- **DeepSeek Reasoner**：更强的推理能力，适合复杂任务

## 🛠️ 开发信息

### 项目结构

```
BlenderDeepSeek/
├── __init__.py          # 主插件文件
├── utilities.py         # 工具函数和 API 调用
├── README.md           # 说明文档
├── requirements.txt    # 依赖项
└── lib/                # 第三方库
    ├── requests/       # HTTP 请求库
    ├── aiohttp/        # 异步 HTTP 库
    └── ...
```

### 关键修改点

相比原始 BlenderGPT：

1. **API 端点**：从 OpenAI 改为 DeepSeek
2. **模型选项**：添加 `deepseek-chat` 和 `deepseek-reasoner`
3. **请求方式**：使用 `requests` 库而非 OpenAI SDK
4. **响应格式**：处理 Server-Sent Events (SSE) 流式响应
5. **用户界面**：更新为 DeepSeek 相关的提示和说明

## 📝 许可证

MIT License

## 🙏 致谢

感谢 [gd3kr](https://github.com/gd3kr) 开发了原始的 BlenderGPT 插件。本项目基于 BlenderGPT 修改，将 OpenAI API 替换为 DeepSeek API。

## 🐛 故障排除

### 问题 1：提示 "No API key detected"

**解决方案**：
1. 确保你已获取 DeepSeek API Key
2. 打开 Blender 偏好设置 > 附加组件 > DeepSeek Blender 助手
3. 在 "API Key" 字段中粘贴你的密钥
4. 重启 Blender

### 问题 2：生成代码执行出错

**解决方案**：
1. 打开 `窗口 > 切换系统控制台` 查看详细错误信息
2. 确保你的 Blender 版本是 3.1 或更高
3. 尝试简化你的指令

### 问题 3：API 请求超时

**解决方案**：
1. 检查你的网络连接
2. 尝试更简短的指令
3. 检查 DeepSeek API 服务状态

## 💬 联系和支持

如有问题或建议，欢迎在 GitHub Issues 中提出。

## 📢 更新日志

### v2.1.0 (2026-06-08)
- ✅ 初始版本发布
- ✅ 集成 DeepSeek Chat 和 Reasoner 模型
- ✅ 支持中文输入
- ✅ 实时代码显示
