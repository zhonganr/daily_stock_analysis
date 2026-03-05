# -*- coding: utf-8 -*-
"""
大盘复盘市场区域配置 - 美股版本

定义美股市场区域的指数、新闻搜索词、Prompt 提示等元数据，
供 MarketAnalyzer 使用。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class MarketProfile:
    """大盘复盘市场区域配置"""

    region: str  # "us"
    # 用于判断整体走势的指数代码
    mood_index_code: str
    # 新闻搜索关键词
    news_queries: List[str]
    # 指数点评 Prompt 提示语
    prompt_index_hint: str
    # 市场概况是否包含涨跌家数、涨停跌停
    has_market_stats: bool
    # 市场概况是否包含板块涨跌
    has_sector_rankings: bool


US_PROFILE = MarketProfile(
    region="us",
    mood_index_code="SPX",
    news_queries=[
        "US stock market",
        "S&P 500 NASDAQ",
        "market analysis",
    ],
    prompt_index_hint="Analyze S&P 500, Nasdaq, Dow Jones and other major index trends",
    has_market_stats=False,
    has_sector_rankings=False,
)


def get_profile(region: str) -> MarketProfile:
    """Return MarketProfile for region (US only)"""
    return US_PROFILE
