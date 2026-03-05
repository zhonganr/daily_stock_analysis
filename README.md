<div align="center">

# AI Stock Analysis System

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)

**AI-powered stock analysis system for global markets (US / Hong Kong / Euronext / Forex)**

Analyze your watchlist daily → generate a decision dashboard → push to multiple channels (Telegram/Discord/Email/WeChat Work/Feishu)

**Zero-cost deployment** · Runs on GitHub Actions · No server required

[**Quick Start**](#-quick-start) · [**Key Features**](#-key-features) · [**Sample Output**](#-sample-output) · [**Full Guide**](docs/full-guide_EN.md) · [**FAQ**](docs/FAQ_EN.md) · [**Changelog**](docs/CHANGELOG.md)

**English** | [简体中文](#-简体中文-chinese) | [繁體中文](docs/README_CHT.md)

</div>

## 💖 Sponsors

<div align="center">
  <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank">
    <img src="./sources/serpapi_banner_en.png" alt="Easily scrape real-time financial news data from search engines - SerpApi" height="160">
  </a>
</div>
<br>

## ✨ Key Features

| Module | Feature | Description |
|--------|---------|-------------|
| AI | Decision Dashboard | One-sentence conclusion + precise entry/exit levels + action checklist |
| Analysis | Multi-dimensional Analysis | Technicals + sentiment + real-time quotes |
| Market | Global Markets | US stocks, Hong Kong, Euronext (5 exchanges), Forex |
| Strategy | Regime Strategy | Built-in US market regime strategy (risk-on/neutral/risk-off) |
| Review | Market Review | Daily market overview, sector changes, northbound flows |
| Image Recognition | Batch Add | Upload screenshot → Vision AI auto-extracts stock codes |
| Backtest | AI Validation | Auto-evaluate historical analysis accuracy, win rates, SL/TP hits |
| **Agent Q&A** | **Strategy Chat** | **Multi-turn strategy dialog, 11 built-in strategies, Web/Bot/API** |
| Notifications | Multi-channel Push | Telegram, Discord, Email, WeChat Work, Feishu, DingTalk, Pushover |
| Automation | Scheduled Runs | GitHub Actions scheduled execution, no server required |

### Tech Stack & Data Sources

| Type | Supported |
|------|----------|
| LLMs | [AIHubMix](https://aihubmix.com/?aff=CfMq), Gemini, OpenAI-compatible, DeepSeek, Qwen, Claude (unified via [LiteLLM](https://github.com/BerriAI/litellm), multi-key load balancing) |
| Market Data | **YFinance (primary)** - Global market consistency |
| News Search | Tavily, SerpAPI, Bocha, Brave |

> **Note**: All market data uses YFinance for global consistency

### Built-in Trading Rules

| Rule | Description |
|------|-------------|
| No chasing highs | Auto warn when deviation > 5% (threshold configurable) |
| Trend trading | Bull alignment: MA5 > MA10 > MA20 |
| Precise levels | Entry price, stop loss, target price |
| Checklist | Each condition marked as Pass / Watch / Fail |
| News freshness | Configurable max age (default 3 days) |

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended)

> Zero cost, 5 minutes to deploy, no server required

#### 1. Fork this Repository

Click the `Fork` button in the upper right corner (give a Star ⭐ if you like it!)

#### 2. Configure Secrets

Go to `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**AI Model Configuration (configure at least one)**

> 💡 **Recommended: [AIHubMix](https://aihubmix.com/?aff=CfMq)** - Use one key for Gemini, GPT, Claude, DeepSeek globally, with free models available. **10% discount** available for this project.

| Secret | Description | Required |
|--------|------------|:----:|
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API Key (free models available) | Optional |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) free key | Optional |
| `ANTHROPIC_API_KEY` | [Anthropic Claude](https://console.anthropic.com/) API Key | Optional |
| `ANTHROPIC_MODEL` | Claude model (e.g., `claude-3-5-sonnet-20241022`) | Optional |
| `OPENAI_API_KEY` | OpenAI-compatible API Key (DeepSeek, Qwen, etc.) | Optional |
| `OPENAI_BASE_URL` | API endpoint (e.g., `https://api.deepseek.com/v1`) | Optional |
| `OPENAI_MODEL` | Model name (e.g., `deepseek-chat`) | Optional |

> Priority: Gemini > Anthropic > OpenAI. Configure at least one.

<details>
<summary><b>Notification Channels</b> (configure at least one)</summary>

| Secret | Description | Required |
|--------|------------|:----:|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token (@BotFather) | Optional |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Optional |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | Optional |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | Optional |
| `DISCORD_BOT_TOKEN` | Discord Bot Token | Optional |
| `DISCORD_CHANNEL_ID` | Discord Channel ID | Optional |
| `EMAIL_SENDER` | Sender email (e.g., `xxx@qq.com`) | Optional |
| `EMAIL_PASSWORD` | Email authorization code | Optional |
| `EMAIL_RECEIVERS` | Receiver emails (comma-separated) | Optional |
| `WECHAT_WEBHOOK_URL` | WeChat Work Webhook URL | Optional |
| `FEISHU_WEBHOOK_URL` | Feishu Webhook URL | Optional |
| `DINGDING_WEBHOOK_URL` | DingTalk Webhook URL | Optional |
| `PUSHPLUS_TOKEN` | PushPlus Token ([Get it](https://www.pushplus.plus)) | Optional |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook URLs (comma-separated) | Optional |

</details>

**Stock Configuration**

| Secret | Description | Required |
|--------|------------|:----:|
| `STOCK_LIST` | Stock codes (comma-separated). Supports US, HK, Euronext, Forex.<br/>Example: `AAPL,TSLA,0700.HK,OR.PA,EURCNY,USDCNY` | ✅ |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) Search API (for news) | Recommended |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) (US stocks optimized) | Optional |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/) API key | Optional |
| `BOCHA_API_KEYS` | [Bocha Search](https://open.bocha.cn/) (Chinese optimized) | Optional |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/) Token | Optional |
| `REPORT_LANGUAGE` | Report language: `en` (English) or `cn` (Chinese), default `en` | Optional |
| `AGENT_MODE` | Enable Agent strategy chat (`true`/`false`, default `false`) | Optional |

#### 3. Enable Actions

Go to `Actions` tab → Click `I understand my workflows, go ahead and enable them`

#### 4. Manual Test

`Actions` → `Daily Stock Analysis` → `Run workflow` → `Run workflow`

#### Done!

The system will run automatically every workday at **18:00 Beijing Time** (configurable).

---

### Option 2: Local / Docker Deployment

```bash
# Clone
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env && nano .env

# Run
python main.py                  # One-time analysis
python main.py --schedule       # Scheduled mode
python main.py --webui          # Start web interface + analysis
```

See [Full Guide](docs/full-guide_EN.md) for Docker setup.

---

## 📱 Sample Output

> For detailed documentation in Chinese, see below or visit [Full Guide (Chinese)](docs/full-guide.md)

### Decision Dashboard
```
🎯 2026-02-08 Decision Dashboard
Analyzed 3 stocks | 🟢Buy:1 🟡Hold:1 🔴Sell:1

📊 Summary
⚪ AAPL: Hold | Score 85 | Bullish
🟢 TSLA: Buy | Score 65 | Strong Bullish
🔴 Moutai: Sell | Score 35 | Bearish
```

---

<a id="简体中文-chinese"></a>

# 📈 股票智能分析系统

> ⬆️ English version above | 简体中文说明如下

## ✨ 功能特性

| 模块 | 功能 | 说明 |
|------|------|------|
| AI | 决策仪表盘 | 一句话核心结论 + 精确买卖点位 + 操作检查清单 |
| 分析 | 多维度分析 | 技术面（盘中实时 MA/多头排列）+ 舆情情报 + 实时行情 |
| 市场 | 全球市场 | 支持美股、港股、Euronext、外汇 |
| 策略 | 市场策略系统 | 内置美股「Regime Strategy」，输出 risk-on/neutral/risk-off 计划 |
| 复盘 | 大盘复盘 | 每日市场概览、板块涨跌 |
| 图片识别 | 从图片添加 | 上传自选股截图，Vision LLM 自动提取股票代码 |
| 回测 | AI 回测验证 | 自动评估历史分析准确率，方向胜率、止盈止损命中率 |
| **Agent 问股** | **策略对话** | **多轮策略问答，支持 11 种内置策略，Web/Bot/API** |
| 推送 | 多渠道通知 | 企业微信、飞书、Telegram、钉钉、邮件、Pushover |
| 自动化 | 定时运行 | GitHub Actions 定时执行，无需服务器 |

### 技术栈与数据来源

| 类型 | 支持 |
|------|------|
| AI 模型 | [AIHubMix](https://aihubmix.com/?aff=CfMq)、Gemini、OpenAI 兼容、DeepSeek、通义千问、Claude（统一通过 [LiteLLM](https://github.com/BerriAI/litellm) 调用）|
| 行情数据 | **YFinance**（全球市场数据源）|
| 新闻搜索 | Tavily、SerpAPI、Bocha、Brave |

### 内置交易纪律

| 规则 | 说明 |
|------|------|
| 严禁追高 | 乖离率超阈值（默认 5%，可配置）自动提示风险 |
| 趋势交易 | MA5 > MA10 > MA20 多头排列 |
| 精确点位 | 买入价、止损价、目标价 |
| 检查清单 | 每项条件以「满足 / 注意 / 不满足」标记 |
| 新闻时效 | 可配置新闻最大时效（默认 3 天） |

## 📱 推送效果

### 决策仪表盘
```
🎯 2026-02-08 决策仪表盘
共分析3只股票 | 🟢买入:0 🟡观望:2 🔴卖出:1

📊 分析结果摘要
⚪ 中钨高新(000657): 观望 | 评分 65 | 看多
⚪ 永鼎股份(600105): 观望 | 评分 48 | 震荡
🟡 新莱应材(300260): 卖出 | 评分 35 | 看空

⚪ 中钨高新 (000657)
📰 重要信息速览
💭 舆情情绪: 市场关注其AI属性与业绩高增长，情绪偏积极，但需消化短期获利盘和主力流出压力。
📊 业绩预期: 基于舆情信息，公司2025年前三季度业绩同比大幅增长，基本面强劲，为股价提供支撑。

🚨 风险警报:

风险点1：2月5日主力资金大幅净卖出3.63亿元，需警惕短期抛压。
风险点2：筹码集中度高达35.15%，表明筹码分散，拉升阻力可能较大。
风险点3：舆情中提及公司历史违规记录及重组相关风险提示，需保持关注。
✨ 利好催化:

利好1：公司被市场定位为AI服务器HDI核心供应商，受益于AI产业发展。
利好2：2025年前三季度扣非净利润同比暴涨407.52%，业绩表现强劲。
📢 最新动态: 【最新消息】舆情显示公司是AI PCB微钻领域龙头，深度绑定全球头部PCB/载板厂。2月5日主力资金净卖出3.63亿元，需关注后续资金流向。

---
生成时间: 18:00
```

### 大盘复盘
```
🎯 2026-01-10 大盘复盘

📊 主要指数
- 上证指数: 3250.12 (🟢+0.85%)
- 深证成指: 10521.36 (🟢+1.02%)
- 创业板指: 2156.78 (🟢+1.35%)

📈 市场概况
上涨: 3920 | 下跌: 1349 | 涨停: 155 | 跌停: 3

🔥 板块表现
领涨: 互联网服务、文化传媒、小金属
领跌: 保险、航空机场、光伏设备
```
## ⚙️ 配置说明

> 📖 完整环境变量、定时任务配置请参考 [完整配置指南](docs/full-guide.md)


## 🖥️ Web 界面

![img.png](sources/fastapi_server.png)

包含完整的配置管理、任务监控和手动分析功能。

**可选密码保护**：在 `.env` 中设置 `ADMIN_AUTH_ENABLED=true` 可启用 Web 登录，首次访问在网页设置初始密码，保护 Settings 中的 API 密钥等敏感配置。详见 [完整指南](docs/full-guide.md)。

### 从图片添加股票

在 **设置 → 基础设置** 中找到「从图片添加」区块，拖拽或选择自选股截图（如 APP 持仓页、行情列表截图），系统会通过 Vision AI 自动识别股票代码并合并到自选列表。

**配置与限制**：
- 需配置 `GEMINI_API_KEY`、`ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` 中至少一个（Vision 能力模型）
- 支持 JPG、PNG、WebP、GIF，单张最大 5MB；请求超时 60 秒

**API 调用**：`POST /api/v1/stocks/extract-from-image`，表单字段 `file`，返回 `{ "codes": ["600519", "300750", ...] }`。详见 [完整指南](docs/full-guide.md)。

### 🤖 Agent 策略问股

在 `.env` 中设置 `AGENT_MODE=true` 后启动服务，访问 `/chat` 页面即可开始多轮策略问答。

- **选择策略**：均线金叉、缠论、波浪理论、多头趋势等 11 种内置策略
- **自然语言提问**：如「用缠论分析 600519」，Agent 自动调用实时行情、K线、技术指标、新闻等工具
- **流式进度反馈**：实时展示 AI 思考路径（行情获取 → 技术分析 → 新闻搜索 → 生成结论）
- **多轮对话**：支持追问上下文，会话历史持久化保存
- **Bot 支持**：`/ask <code> [strategy]` 命令触发策略分析
- **自定义策略**：在 `strategies/` 目录下新建 YAML 文件即可添加策略，无需写代码

> **注意**：Agent 模式依赖外部 LLM（Gemini/OpenAI 等），每次对话会产生 API 调用费用。不影响非 Agent 模式（`AGENT_MODE=false` 或未设置）的正常运行。

### 启动方式

1. **启动服务**（默认会自动编译前端）
   ```bash
   python main.py --webui       # 启动 Web 界面 + 执行定时分析
   python main.py --webui-only  # 仅启动 Web 界面
   ```
   启动时会在 `apps/dsa-web` 自动执行 `npm install && npm run build`。
   如需关闭自动构建，设置 `WEBUI_AUTO_BUILD=false`，并改为手动执行：
   ```bash
   cd ./apps/dsa-web
   npm install && npm run build
   cd ../..
   ```

访问 `http://127.0.0.1:8000` 即可使用。

> 也可以使用 `python main.py --serve` (等效命令)

## 🗺️ Roadmap

查看已支持的功能和未来规划：[更新日志](docs/CHANGELOG.md)

> 有建议？欢迎 [提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)


---

## ☕ 支持项目

如果本项目对你有帮助，欢迎支持项目的持续维护与迭代，感谢支持 🙏  
赞赏可备注联系方式，祝股市长虹

| 支付宝 (Alipay) | 微信支付 (WeChat) | Ko-fi |
| :---: | :---: | :---: |
| <img src="./sources/alipay.jpg" width="200" alt="Alipay"> | <img src="./sources/wechatpay.jpg" width="200" alt="WeChat Pay"> | <a href="https://ko-fi.com/mumu157" target="_blank"><img src="./sources/ko-fi.png" width="200" alt="Ko-fi"></a> |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详见 [贡献指南](docs/CONTRIBUTING.md)

### 本地门禁（建议先跑）

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
```

如修改前端（`apps/dsa-web`）：

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

## 📄 License
[MIT License](LICENSE) © 2026 ZhuLinsen

如果你在项目中使用或基于本项目进行二次开发，
非常欢迎在 README 或文档中注明来源并附上本仓库链接。
这将有助于项目的持续维护和社区发展。

## 📬 联系与合作
- GitHub Issues：[提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

## ⭐ Star History
**如果觉得有用，请给个 ⭐ Star 支持一下！**

<a href="https://star-history.com/#ZhuLinsen/daily_stock_analysis&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
 </picture>
</a>

## ⚠️ 免责声明

本项目仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。作者不对使用本项目产生的任何损失负责。

---
