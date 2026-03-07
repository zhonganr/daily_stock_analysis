# -*- coding: utf-8 -*-
"""
===================================
数据源策略层 - 包初始化
===================================

本包实现策略模式管理多个数据源，实现：
1. 统一的数据获取接口
2. 自动故障切换
3. 防封禁流控策略

数据源优先级（针对全球股市）：
1. YfinanceFetcher (Priority 0) - 最高优先级，用于美股、港股、其他全球市场

提示：仅支持全球市场（美股、港股等），已移除A股数据源。
"""

from .base import BaseFetcher, DataFetcherManager
from .yfinance_fetcher import YfinanceFetcher
from .us_index_mapping import (
    is_us_index_code, 
    is_us_stock_code, 
    is_hk_stock_code,
    is_euronext_stock,
    is_forex_pair,
    is_global_stock,
    get_us_index_yf_symbol,
    get_forex_yf_symbol,
    US_INDEX_MAPPING,
    GLOBAL_MARKET_SUFFIXES,
    FOREX_PAIRS,
    KNOWN_EURONEXT_STOCKS,
)

__all__ = [
    'BaseFetcher',
    'DataFetcherManager',
    'YfinanceFetcher',
    'is_us_index_code',
    'is_us_stock_code',
    'is_hk_stock_code',
    'is_euronext_stock',
    'is_forex_pair',
    'is_global_stock',
    'get_us_index_yf_symbol',
    'get_forex_yf_symbol',
    'US_INDEX_MAPPING',
    'GLOBAL_MARKET_SUFFIXES',
    'FOREX_PAIRS',
    'KNOWN_EURONEXT_STOCKS',
]
