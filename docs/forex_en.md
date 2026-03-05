# Forex Support - Usage Guide

## Overview

The system now supports forex pair analysis! You can monitor and analyze forex prices just like stocks.

## Supported Forex Pairs

| Pair | Chinese Name | Yahoo Finance Symbol |
|------|---------|------------------|
| **EURCNY** | EUR/CNY | EURCNY=X |
| **USDCNY** | USD/CNY | USDCNY=X |
| **GBPCNY** | GBP/CNY | GBPCNY=X |
| **JPYCNY** | JPY/CNY | JPYCNY=X |
| **CHFCNY** | CHF/CNY | CHFCNY=X |

## Configuration

### Add Forex to STOCK_LIST

Edit `.env` file and add forex pairs to `STOCK_LIST` (comma-separated):

```bash
# Forex pairs only
STOCK_LIST=EURCNY,USDCNY

# Mixed with US stocks
STOCK_LIST=AAPL,TSLA,EURCNY,USDCNY

# Mixed with all global markets
STOCK_LIST=AAPL,0700.HK,OR.PA,ASML.AS,EURCNY,USDCNY,GBPCNY
```

### Code Format

Forex codes support both formats (automatically converted to uppercase):
- Without suffix: `EURCNY`, `USDCNY`
- With =X suffix: `EURCNY=X`, `USDCNY=X` (Yahoo Finance standard format)

## Usage Examples

### 1. Analyze Forex Pairs

```bash
# Brief analysis
/analyze EURCNY

# Full report
/analyze EURCNY full
/analyze USDCNY full
```

**Bot Commands (Telegram, Feishu, etc.):**
```
/analyze EURCNY
/analyze USDCNY full
```

**CLI:**
```bash
python main.py EURCNY
python main.py USDCNY full
```

### 2. Strategy-Based Analysis

```bash
# Default strategy (bull_trend)
/ask EURCNY

# Specific strategy
/ask EURCNY chan_theory
/ask USDCNY wave_theory
/ask GBPCNY ma_golden_cross
```

### 3. Scheduled Monitoring

Set up scheduled tasks to analyze forex pairs:

**.env configuration:**
```bash
STOCK_LIST=AAPL,EURCNY,USDCNY,0700.HK

SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00

GEMINI_API_KEY=your-key-here
```

## Complete Examples

### Example 1: Mixed Portfolio

Monitor US stocks, forex, and HK stocks together:

**.env:**
```bash
STOCK_LIST=AAPL,TSLA,MSFT,EURCNY,USDCNY,0700.HK

SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
```

### Example 2: Forex Only

Focus only on forex pair analysis:

**.env:**
```bash
STOCK_LIST=EURCNY,USDCNY,GBPCNY,JPYCNY
```

**Commands:**
```
/analyze EURCNY
/ask USDCNY 缠论分析
/ask GBPCNY wave_theory
```

### Example 3: CLI Usage

```bash
# Single analysis
python main.py EURCNY
python main.py USDCNY full

# Batch analysis
python main.py EURCNY USDCNY GBPCNY

# With strategy
python main.py USDCNY --strategy bull_trend
```

## Notes

### 1. Data Source

Forex data is provided by **YFinance**. Characteristics:
- Real-time quotes synced with global markets
- No data updates on weekends and non-trading hours

### 2. Forex Characteristics

Forex analysis differs from stock analysis:
- **24/5 Trading**: Available Monday-Friday round-the-clock
- **Lower Volatility**: Generally more stable than individual stocks
- **Technical Analysis**: All technical indicators apply
- **Strategy Use**: Chan theory, wave theory, etc. all applicable

### 3. Trading Day Check

```bash
# Forex trades 24/5, keep default trading day check
TRADING_DAY_CHECK_ENABLED=true
```

For forex-only setups, disable trading day check:
```bash
TRADING_DAY_CHECK_ENABLED=false
```

### 4. Code Format Notes

The system automatically handles these variants:
```python
EURCNY          # ✅ Supported
eurcny          # ✅ Supported (auto-uppercase)
EURCNY=X        # ✅ Supported (Yahoo Finance format)
eurcny=x        # ✅ Supported (auto-uppercase)
```

## Troubleshooting

### Issue 1: Analysis fails with "Invalid stock code"

**Cause**: Forex code format is incorrect

**Solution**:
- Use correct 3+3 letter format: EURCNY, USDCNY
- Check for spaces or special characters
- Case doesn't matter (auto-converted to uppercase)

```bash
# ❌ Wrong
EUR-CNY
EUR_CNY
eur cny

# ✅ Correct
EURCNY
eurcny
EURCNY=X
```

### Issue 2: No data or abnormal display

**Causes**:
- Network connectivity issue
- Yahoo Finance service unavailable
- No data during non-trading hours

**Solutions**:
- Check network connection
- Review logs in `./logs/`
- Retry during trading hours (Monday-Friday)

### Issue 3: Scheduled analysis not running

**Causes**:
- Scheduled tasks not enabled
- Scheduled time already passed
- Trading day check disabled

**Solutions**:
```bash
# Check configuration
grep SCHEDULE .env

# Manual test
python main.py EURCNY

# Force execution
python main.py EURCNY --force-run
```

## Configuration Reference

Complete `.env` example:

```bash
# Forex configuration
STOCK_LIST=AAPL,EURCNY,USDCNY,0700.HK

# AI Model
GEMINI_API_KEY=your-api-key
PROMPT_TEMPLATE_STYLE=default

# Scheduled Tasks
SCHEDULE_ENABLED=true
SCHEDULE_TIME=18:00
SCHEDULE_RUN_IMMEDIATELY=false
TRADING_DAY_CHECK_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_DIR=./logs
```

## FAQ

**Q: Can I mix forex with stocks in STOCK_LIST?**

A: Yes! `STOCK_LIST` supports any combination:
```bash
STOCK_LIST=AAPL,EURCNY,0700.HK,OR.PA
```

**Q: Which forex pairs are supported?**

A: Currently EURCNY, USDCNY, GBPCNY, JPYCNY, CHFCNY. Open an Issue or PR to request additional pairs.

**Q: Can I add custom forex pairs?**

A: Yes, modify `data_provider/us_index_mapping.py`:
- Update `FOREX_PAIRS` dictionary
- Update `is_forex_pair()` function

**Q: How accurate is forex analysis?**

A: Same as stock analysis. Technical analysis methods work equally well for forex, considering forex market characteristics (24/5 trading, holding costs, etc.).

**Q: Can I use `/ask` command for forex?**

A: Yes!
```bash
/ask EURCNY chan_theory
/ask USDCNY wave_theory
```

## Extending Support

To add more forex pairs, edit `data_provider/us_index_mapping.py`:

```python
# Add to FOREX_PAIRS dictionary
FOREX_PAIRS = {
    'AUDCNY': ('AUDCNY=X', 'AUD/CNY'),  # New
    'NZDCNY': ('NZDCNY=X', 'NZD/CNY'),  # New
    # ... other pairs
}

# Update is_forex_pair() function
def is_forex_pair(code: str) -> bool:
    # ...
    if len(normalized) == 6:
        return normalized in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY', 'AUDCNY', 'NZDCNY']
```

Restart the system to activate the changes.

## Feedback

Questions or suggestions (e.g., adding new forex pairs)? Feel free to [open an Issue](https://github.com/zhonganruo/daily_stock_analysis/issues) or submit a PR.
