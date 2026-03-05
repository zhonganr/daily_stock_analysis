# 外汇对支持

## 概述

系统现已支持外汇对分析，可以像监控股票一样监控和分析外汇价格走势。

## 支持的外汇对

| 外汇对 | 中文名称 | Yahoo Finance 符号 |
|--------|---------|------------------|
| **EURCNY** | 欧元/人民币 | EURCNY=X |
| **USDCNY** | 美元/人民币 | USDCNY=X |
| **GBPCNY** | 英镑/人民币 | GBPCNY=X |
| **JPYCNY** | 日元/人民币 | JPYCNY=X |
| **CHFCNY** | 瑞士法郎/人民币 | CHFCNY=X |

## 配置方式

### 在 STOCK_LIST 中添加外汇对

编辑 `.env` 文件，在 `STOCK_LIST` 中添加外汇对代码（用逗号分隔）：

```bash
# 只监控外汇对
STOCK_LIST=EURCNY,USDCNY

# 混合美股和外汇
STOCK_LIST=AAPL,TSLA,EURCNY,USDCNY

# 混合全球各市场（美股、港股、Euronext、外汇）
STOCK_LIST=AAPL,0700.HK,OR.PA,ASML.AS,EURCNY,USDCNY,GBPCNY
```

### 代码格式

外汇对代码支持两种格式（都会自动转为大写）：
- 不带后缀：`EURCNY`、`USDCNY`
- 带 =X 后缀：`EURCNY=X`、`USDCNY=X`（Yahoo Finance 标准格式）

## 使用示例

### 1. 分析外汇对

分析单个外汇对的价格走势：

```bash
/analyze EURCNY              # 精简分析
/analyze EURCNY full         # 完整分析
/analyze USDCNY              # 美元/人民币分析
```

**Bot 命令示例（Telegram、飞书等）：**
```
/analyze EURCNY
/analyze USDCNY full
```

**CLI 命令示例：**
```bash
python main.py EURCNY
python main.py USDCNY full
```

### 2. 使用特定策略分析

结合各种策略分析外汇对：

```bash
/ask EURCNY                  # 使用默认策略 (bull_trend)
/ask EURCNY 缠论分析          # 使用缠论
/ask USDCNY 波浪理论         # 使用波浪理论
/ask GBPCNY 均线金叉         # 使用均线金叉策略
```

### 3. 定时监控外汇对

设置定时任务，定期分析监控的外汇对：

```bash
# .env 配置
STOCK_LIST=AAPL,EURCNY,USDCNY
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
```

## 完整示例

### 示例 1：混合监控

监控美股、外汇、港股的混合组合：

**.env 配置：**
```bash
STOCK_LIST=AAPL,TSLA,MSFT,EURCNY,USDCNY,0700.HK

SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00

GEMINI_API_KEY=your-key-here
```

### 示例 2：仅监控外汇

只关注外汇对的价格分析：

**.env 配置：**
```bash
STOCK_LIST=EURCNY,USDCNY,GBPCNY,JPYCNY
```

**Bot 命令：**
```
/analyze EURCNY
/analyze USDCNY full
/ask EURCNY 缠论分析
/ask GBPCNY 波浪理论
```

### 示例 3：CLI 命令行使用

```bash
# 单个分析
python main.py EURCNY
python main.py USDCNY full

# 批量分析
python main.py EURCNY USDCNY GBPCNY

# 指定策略
python main.py USDCNY --strategy bull_trend
```

## 注意事项

### 1. 数据来源

外汇数据由 **YFinance** 提供。YFinance 支持主要外汇对的实时报价，但可能存在以下特点：
- 数据基本同步全球交易市场
- 周末及非交易时间无数据更新

### 2. 外汇特性

与股票分析相比，外汇对分析有以下特点：
- **24/5 交易**：周一至周五全天交易（与股票市场开收盘时间不同）
- **波动率**：通常低于个股，更稳定
- **技术指标**：同样支持所有技术分析方法
- **策略适用性**：缠论、波浪理论等都适用

### 3. 日期和交易日检查

```bash
# 外汇是 24/5 交易，启用交易日检查时仍建议保持默认
TRADING_DAY_CHECK_ENABLED=true
```

如果只监控外汇对（不涉及股票），可考虑禁用交易日检查：
```bash
TRADING_DAY_CHECK_ENABLED=false
```

### 4. 代码格式说明

系统会自动处理这些变体：
```python
EURCNY          # ✅ 支持
eurcny          # ✅ 支持（自动转大写）
EURCNY=X        # ✅ 支持（Yahoo Finance 格式）
eurcny=x        # ✅ 支持（自动转大写）
```

## 故障排查

### 问题 1：分析失败，提示"无效的股票代码"

**原因**：外汇对代码格式不正确

**解决方案**：
- 确保使用正确的 3+3 字母格式，如 EURCNY、USDCNY
- 检查是否包含空格或特殊字符
- 代码大小写不影响（系统自动转大写）

```bash
# ❌ 错误
EUR-CNY
EUR_CNY
eur cny

# ✅ 正确
EURCNY
eurcny
EURCNY=X
```

### 问题 2：数据显示异常或无几据

**原因**：
- 网络连接问题
- Yahoo Finance 服务不稳定
- 非交易时间无数据更新

**解决方案**：
- 检查网络连接
- 查看日志文件 (`./logs/`)
- 在交易时间（周一至周五）重试

### 问题 3：自动分析不运行

**原因**：
- 定时任务未启用
- 设置的时间已过
- 交易日检查导致跳过（如果禁用此检查可设置 `--force-run`）

**解决方案**：
```bash
# 检查配置
grep SCHEDULE .env

# 手动测试
python main.py EURCNY

# 强制运行定时任务
python main.py EURCNY --force-run
```

## 相关配置

完整的 `.env` 示例：

```bash
# 外汇对配置
STOCK_LIST=AAPL,EURCNY,USDCNY,0700.HK

# AI 模型
GEMINI_API_KEY=your-api-key
PROMPT_TEMPLATE_STYLE=default

# 定时任务
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
SCHEDULE_RUN_IMMEDIATELY=false
TRADING_DAY_CHECK_ENABLED=true

# 日志
LOG_LEVEL=INFO
LOG_DIR=./logs
```

## 常见问题

**Q: 外汇对可以与股票混合使用吗？**

A: 可以。`STOCK_LIST` 支持任意组合：
```bash
STOCK_LIST=AAPL,EURCNY,0700.HK,OR.PA
```

**Q: 支持哪些外汇对？**

A: 目前支持 EURCNY, USDCNY, GBPCNY, JPYCNY, CHFCNY。如需其他外汇对，可提交 Issue 或 PR。

**Q: 可以自定义外汇对吗？**

A: 可以。修改 `data_provider/us_index_mapping.py` 中的 `FOREX_PAIRS` 字典和 `is_forex_pair()` 函数。

**Q: 外汇对分析的准确性如何？**

A: 与股票分析相同。技术分析方法对外汇对同样有效，但需注意外汇市场特性（24/5 交易、持仓成本等）。

**Q: 可以用 `/ask` 命令分析外汇对吗？**

A: 可以。
```bash
/ask EURCNY 缠论分析
/ask USDCNY 波浪理论
```

## 扩展支持

如需添加其他外汇对，修改 `data_provider/us_index_mapping.py`：

```python
# 在 FOREX_PAIRS 字典中添加新对
FOREX_PAIRS = {
    'AUDCNY': ('AUDCNY=X', '澳元/人民币'),  # 新增
    'NZDCNY': ('NZDCNY=X', '新西兰元/人民币'),  # 新增
    # ... 其他对
}

# 在 is_forex_pair() 函数中更新支持列表
def is_forex_pair(code: str) -> bool:
    # ...
    if len(normalized) == 6:
        return normalized in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY', 'AUDCNY', 'NZDCNY']
```

然后重新启动系统即可。

## 反馈与支持

如有问题或建议（如添加新外汇对），欢迎 [提交 Issue](https://github.com/zhonganruo/daily_stock_analysis/issues) 或 PR。
