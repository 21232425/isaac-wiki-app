# 👼 以撒的结合 Wiki 智能助手 (Isaac Wiki Agent)

*本readme文件纯由AI生成，谨慎参考

这是一个基于大语言模型（LLM）和 Tool-Calling（工具调用）架构开发的《以撒的结合：忏悔》中文 Wiki 智能查询助手。

通过自然语言对话，助手能够自动推测意图、提取关键词，并自主调用工具检索和阅读 [以撒中文 HuijiWiki](https://isaac.huijiwiki.com/)，为玩家提供精准、详细的游戏资料解答。

## ✨ 核心特性

- 🧠 **真正的 Agent 架构**: 抛弃传统的正则匹配与硬编码字典。由大模型（如 DeepSeek、GPT-4o）自主决定搜索策略（`search_wiki`）和阅读具体页面（`read_wiki_page`）。
- 💬 **现代化 Web 界面**: 基于 Streamlit 构建的即时响应聊天界面，开箱即用，体验媲美 ChatGPT。
- ⚡ **无缝接入 DeepSeek**: 默认配置接入性价比极高且能力强大的 DeepSeek API（完全兼容 OpenAI 接口规范）。
- ☁️ **云端友好**: 针对 Streamlit Community Cloud 等免费平台优化，纯环境变量配置，杜绝 API Key 泄露风险。

## 📂 项目结构

```text
isaac-wiki-app/
├── web_app.py          # Streamlit 网页端入口文件（UI 界面）
├── true_agent.py       # 智能体核心逻辑（包含 Prompt 与 Tool-Calling 循环）
├── tools/              # 底层工具库（封装了与 Wiki API 交互的逻辑）
└── requirements.txt    # Python 依赖清单

```

## 🚀 本地快速开始

### 1. 准备工作

请确保你的电脑已安装 Python 3.8 或以上版本，并获取了 [DeepSeek](https://platform.deepseek.com/) 的 API Key。

### 2. 安装依赖

打开终端，在项目根目录下运行：

```bash
pip install -r requirements.txt

```

### 3. 配置环境变量

为了安全起见，API Key 不写在代码里，而是通过环境变量传递。
在终端中运行以下命令（将 `sk-xxxx` 替换为你的真实 Key）：

**Windows (PowerShell):**

```powershell
$env:DEEPSEEK_API_KEY="sk-xxxx"

```

**Mac / Linux:**

```bash
export DEEPSEEK_API_KEY="sk-xxxx"

```

### 4. 运行助手

**启动 Web 网页版（推荐）：**

```bash
streamlit run web_app.py

```

*(运行后会自动在浏览器中打开聊天界面)*

**启动纯命令行交互版：**

```bash
python true_agent.py -i

```

## ☁️ 部署到 Streamlit Cloud (免费向外分享)

1. 将本仓库完整 Push 到你自己的 GitHub 账号下。
2. 访问 [Streamlit Community Cloud](https://share.streamlit.io/) 并使用 GitHub 账号登录。
3. 点击 **"New app"**。
4. 选择你的仓库，**Main file path** 填写 `web_app.py`。
5. 点击 **"Advanced settings"**，在 Secrets 区域填入你的 API Key：
```toml
DEEPSEEK_API_KEY = "sk-你的真实APIKey"

```


6. 点击 **"Deploy!"**，几分钟后你就可以将生成的专属网址分享给朋友们了！

## ⚠️ 免责声明

本工具仅供学习交流使用，数据均来自《以撒的结合》中文 HuijiWiki，版权归原作者与社区所有。

```

### 如何在 GitHub 上添加这个文件？

1. 在你刚才上传好代码的 GitHub 仓库主页，文件列表的右上方，找到一个叫 **"Add a README"** 的绿色按钮（如果没有，点击顶部的 `Add file` -> `Create new file`，然后把文件名写成 `README.md`）。
2. 把上面的内容原封不动地复制进大文本框里。
3. 点击页面右上角绿色的 **"Commit changes"** 保存。

保存后，你的仓库主页就会像模像样地展示出这篇漂亮的图文介绍了！接下来，你就可以去 [Streamlit Community Cloud](https://share.streamlit.io/) 按照步骤部署你的网页了。遇到任何卡壳的地方随时告诉我！

```
