# Trading Strategies Directory / 交易策略目录

This directory stores **natural language strategy files** (YAML format). All `.yaml` files in this directory are automatically loaded when the system starts.

## How to Write Custom Strategies

Simply create a `.yaml` file describing your trading strategy in natural language (English, Chinese, or any language), **no code needed**.

### Minimal Template

```yaml
name: my_strategy          # Unique identifier (English, underscore-separated)
display_name: My Strategy  # Display name (can be in any language)
description: Brief description of the strategy's purpose

instructions: |
  Your strategy description...
  Write in natural language: judgment criteria, entry conditions, exit conditions, etc.
  You can reference tool names (such as get_daily_history, analyze_trend) to guide AI on which data tools to use.
```

### Complete Template

```yaml
name: my_strategy
display_name: My Strategy
description: Brief description of the strategy's applicable market scenarios

# Strategy category: trend, pattern, reversal, framework
category: trend

# Associated core trading principles (1-7), optional
core_rules: [1, 2]

# List of tools required by the strategy, optional
# Available tools: get_daily_history, analyze_trend, get_realtime_quote,
#                  get_sector_rankings, search_stock_news
required_tools:
  - get_daily_history
  - analyze_trend

# Strategy detailed description (natural language, supports Markdown format)
instructions: |
  **My Strategy Name**

  Judgment Criteria:

  1. **Condition One**:
     - Use `analyze_trend` to check MA alignment.
     - Describe the trend characteristics you expect to see...

  2. **Condition Two**:
     - Describe volume requirements...

  Score Adjustment:
  - sentiment_score adjustment when conditions are met
  - Note the strategy name in `buy_reason`
```

### Core Trading Principles Reference

| Number | Principle |
|--------|-----------|
| 1 | Strict Entry Strategy: Deviation < 5% before considering entry |
| 2 | Trend Trading: MA5 > MA10 > MA20 bullish alignment |
| 3 | Efficiency First: Volume confirms trend validity |
| 4 | Entry Preference: Retracement to MA support preferred |
| 5 | Risk Check: Bad news veto single factor |
| 6 | Volume-Price Coordination: Volume confirms price movement |
| 7 | Strong Trend Relaxation: Sector leaders can use relaxed standards |

## Custom Strategy Directory

In addition to this directory (built-in strategies), you can specify additional custom strategy directories via environment variables:

```env
AGENT_STRATEGY_DIR=./my_strategies
```

The system will load both built-in and custom strategies. If names conflict, custom strategies override built-in strategies.
