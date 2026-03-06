# -*- coding: utf-8 -*-
"""
===================================
Akshare Fetcher - Code Identification Utilities
===================================

提供股票代码识别辅助函数，用于区分不同市场的股票代码。
- _is_us_code: 判断是否为美股代码
- _is_hk_code: 判断是否为港股代码
- _is_euronext_code: 判断是否为欧洲交易所 (Euronext) 代码
- _is_forex_code: 判断是否为外汇对代码

本模块为遗留接口，函数实现依赖于 us_index_mapping 模块。
"""

import re


def _is_us_code(code: str) -> bool:
    """
    判断代码是否为美股股票代码。

    美股股票代码为 1-5 个大写字母，可选 .X 后缀（如 BRK.B）。

    Args:
        code: 股票代码，如 'AAPL', 'TSLA', 'BRK.B'

    Returns:
        True 表示是美股代码，否则 False

    Examples:
        >>> _is_us_code('AAPL')
        True
        >>> _is_us_code('TSLA')
        True
        >>> _is_us_code('BRK.B')
        True
        >>> _is_us_code('600519')
        False
        >>> _is_us_code('hk00700')
        False
    """
    normalized = (code or '').strip().upper()
    # US股票代码正则：1-5 个大写字母，可选 .X 后缀
    us_pattern = re.compile(r'^[A-Z]{1,5}(\.[A-Z])?$')
    return bool(us_pattern.match(normalized))


def _is_hk_code(code: str) -> bool:
    """
    判断代码是否为港股代码。

    港股代码通常包含 'HK' 前缀（不分大小写），如 'HK00700', 'hk09988'。

    Args:
        code: 股票代码，如 'HK00700', 'hk09988'

    Returns:
        True 表示是港股代码，否则 False

    Examples:
        >>> _is_hk_code('HK00700')
        True
        >>> _is_hk_code('hk00700')
        True
        >>> _is_hk_code('HK09988')
        True
        >>> _is_hk_code('AAPL')
        False
    """
    normalized = (code or '').strip().upper()
    # 港股代码包含 'HK' 前缀后跟 4-5 个数字
    hk_pattern = re.compile(r'^HK\d{4,5}$')
    return bool(hk_pattern.match(normalized))


def _is_euronext_code(code: str) -> bool:
    """
    判断代码是否为欧洲交易所 (Euronext) 代码。

    Euronext 代码格式：1-6 个大写字母 + .XX 市场后缀
    支持的市场：
    - .PA (巴黎 - Paris)
    - .AS (阿姆斯特丹 - Amsterdam)
    - .BR (布鲁塞尔 - Brussels)
    - .DU (都柏林 - Dublin)
    - .LI (葡萄牙 - Lisbon)

    Args:
        code: 股票代码，如 'OR.PA', 'ASML.AS', 'BNP.PA', 'TTE.PA'

    Returns:
        True 表示是 Euronext 代码，否则 False

    Examples:
        >>> _is_euronext_code('OR.PA')
        True
        >>> _is_euronext_code('ASML.AS')
        True
        >>> _is_euronext_code('BNP.PA')
        True
        >>> _is_euronext_code('TTE.PA')
        True
        >>> _is_euronext_code('AAPL')
        False
    """
    normalized = (code or '').strip().upper()
    # Euronext 代码正则：1-6 个大写字母，后跟 .XX 市场后缀
    euronext_pattern = re.compile(r'^[A-Z]{1,6}\.(PA|AS|BR|DU|LI)$')
    return bool(euronext_pattern.match(normalized))


def _is_forex_code(code: str) -> bool:
    """
    判断代码是否为支持的外汇对代码。

    外汇对代码通常为 6 个大写字母（基础货币 3 个字母 + 报价货币 3 个字母），
    可选带 =X 或 Y 后缀。

    支持的外汇对：
    - EURCNY (欧元/人民币)
    - USDCNY (美元/人民币)
    以及带 =X 后缀的变体

    Args:
        code: 外汇代码，如 'EURCNY', 'USDCNY', 'EURCNY=X'

    Returns:
        True 表示是支持的外汇对代码，否则 False

    Examples:
        >>> _is_forex_code('EURCNY')
        True
        >>> _is_forex_code('USDCNY')
        True
        >>> _is_forex_code('EURCNY=X')
        True
        >>> _is_forex_code('AAPL')
        False
    """
    normalized = (code or '').strip().upper()
    
    # 外汇对正则：6 个大写字母或 6 个大写字母 + (=X|Y|X) 后缀
    forex_pattern = re.compile(r'^[A-Z]{6}(=X|Y|X)?$')
    
    if not forex_pattern.match(normalized):
        return False
    
    # 进一步验证是否为真实的外汇对（基础货币和计价货币都是有效的）
    # 对于现在支持的对：EURCNY, USDCNY
    if len(normalized) == 6:
        # 不带后缀的外汇对
        return normalized in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY']
    else:
        # 带 =X、Y、X 后缀的外汇对
        if normalized.endswith('=X'):
            base = normalized[:-2]
        else:
            base = normalized[:-1]
        return base in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY']
