# -*- coding: utf-8 -*-
"""
===================================
全球各市场股票代码与外汇工具
===================================

提供：
1. 美股指数代码映射（如 SPX -> ^GSPC）
2. 美股股票代码识别（AAPL、TSLA 等）
3. 港股代码识别（HK 前缀）
4. Euronext 代码识别（.PA、.AS、.BR 等）
5. 外汇对代码识别（EURCNY、USDCNY 等）

支持的全球市场：
- 美股: AAPL, TSLA, BRK.B
- 香港: 0700.HK
- 法国: OR.PA (Euronext Paris)
- 荷兰: ASML.AS (Euronext Amsterdam)
- 比利时: GBT.BR (Euronext Brussels)
- 都柏林: CRH.DU (Euronext Dublin)
- 葡萄牙: PHM.LI (Euronext Lisbon)
- 外汇: EURCNY (欧元/人民币), USDCNY (美元/人民币)
"""

import re

# 美股代码正则：1-5 个大写字母，可选 .X 后缀（如 BRK.B）
_US_STOCK_PATTERN = re.compile(r'^[A-Z]{1,5}(\.[A-Z])?$')

# 港股代码正则：HK 前缀 + 4-5 位数字（如 HK00700）或 4-5 位数字 + .HK 后缀（如 0700.HK）
_HK_STOCK_PATTERN = re.compile(r'^(HK\d{4,5}|\d{4,5}\.HK)$')

# Euronext 代码正则：1-6 个大写字母，后跟 .XX 市场后缀
_EURONEXT_PATTERN = re.compile(r'^[A-Z]{1,6}\.(PA|AS|BR|DU|LI)$')

# 外汇对代码正则：3个字母(基础货币)+3个字母(报价货币) 或带Y/X后缀
_FOREX_PATTERN = re.compile(r'^[A-Z]{6}(Y|X)?$')

# 全球交易所市场后缀
GLOBAL_MARKET_SUFFIXES = {
    '.PA': '巴黎 (Paris)',
    '.AS': '阿姆斯特丹 (Amsterdam)',
    '.BR': '布鲁塞尔 (Brussels)',
    '.DU': '都柏林 (Dublin)',
    '.LI': '葡萄牙 (Lisbon)',
    '.HK': '香港 (Hong Kong)',
    '.SS': '上海 (Shanghai)',
    '.SZ': '深圳 (Shenzhen)',
}

# 支持的外汇对映射
FOREX_PAIRS = {
    'EURCNY': ('EURCNY=X', '欧元/人民币'),
    'EURCNY=X': ('EURCNY=X', '欧元/人民币'),
    'USDCNY': ('USDCNY=X', '美元/人民币'),
    'USDCNY=X': ('USDCNY=X', '美元/人民币'),
    'EUR': ('EURCNY=X', '欧元/人民币'),  # 简写别名
    'USD': ('USDCNY=X', '美元/人民币'),  # 简写别名 (注意：与美股代码冲突，需要上下文判断)
}

# 已知 Euronext 股票映射（无后缀代码 -> 带后缀代码）
# 这解决了"BNP"等无后缀代码被误认为美股的问题
KNOWN_EURONEXT_STOCKS = {
    # France (Paris) - .PA
    'BNP': 'BNP.PA',       # BNP Paribas
    'TTE': 'TTE.PA',       # TotalEnergies
    'OR': 'OR.PA',         # L'Oréal
    'MC': 'MC.PA',         # LVMH
    'RMS': 'RMS.PA',       # Hermès
    
    # Netherlands (Amsterdam) - .AS
    'ASML': 'ASML.AS',     # ASML Holding
    'AEX': 'AEX.AS',       # Amsterdam Exchange Index
    'RDSA': 'RDSA.AS',     # Royal Dutch Shell A
    
    # Belgium (Brussels) - .BR
    'GBT': 'GBT.BR',       # GBT Tokenize
    
    # Ireland (Dublin) - .DU
    'CRH': 'CRH.DU',       # CRH plc
    
    # Portugal (Lisbon) - .LI
    # (添加更多葡萄牙股票)
}


# 用户输入 -> (Yahoo Finance 符号, 中文名称)
US_INDEX_MAPPING = {
    # 标普 500
    'SPX': ('^GSPC', '标普500指数'),
    '^GSPC': ('^GSPC', '标普500指数'),
    'GSPC': ('^GSPC', '标普500指数'),
    # 道琼斯工业平均指数
    'DJI': ('^DJI', '道琼斯工业指数'),
    '^DJI': ('^DJI', '道琼斯工业指数'),
    'DJIA': ('^DJI', '道琼斯工业指数'),
    # 纳斯达克综合指数
    'IXIC': ('^IXIC', '纳斯达克综合指数'),
    '^IXIC': ('^IXIC', '纳斯达克综合指数'),
    'NASDAQ': ('^IXIC', '纳斯达克综合指数'),
    # 纳斯达克 100
    'NDX': ('^NDX', '纳斯达克100指数'),
    '^NDX': ('^NDX', '纳斯达克100指数'),
    # VIX 波动率指数
    'VIX': ('^VIX', 'VIX恐慌指数'),
    '^VIX': ('^VIX', 'VIX恐慌指数'),
    # 罗素 2000
    'RUT': ('^RUT', '罗素2000指数'),
    '^RUT': ('^RUT', '罗素2000指数'),
}


def is_us_index_code(code: str) -> bool:
    """
    判断代码是否为美股指数符号。

    Args:
        code: 股票/指数代码，如 'SPX', 'DJI'

    Returns:
        True 表示是已知美股指数符号，否则 False

    Examples:
        >>> is_us_index_code('SPX')
        True
        >>> is_us_index_code('AAPL')
        False
    """
    return (code or '').strip().upper() in US_INDEX_MAPPING


def is_us_stock_code(code: str) -> bool:
    """
    判断代码是否为美股股票符号（排除美股指数）。

    美股股票代码为 1-5 个大写字母，可选 .X 后缀如 BRK.B。
    美股指数（SPX、DJI 等）明确排除。

    Args:
        code: 股票代码，如 'AAPL', 'TSLA', 'BRK.B'

    Returns:
        True 表示是美股股票符号，否则 False

    Examples:
        >>> is_us_stock_code('AAPL')
        True
        >>> is_us_stock_code('TSLA')
        True
        >>> is_us_stock_code('BRK.B')
        True
        >>> is_us_stock_code('SPX')
        False
        >>> is_us_stock_code('600519')
        False
    """
    normalized = (code or '').strip().upper()
    # 美股指数不是股票
    if normalized in US_INDEX_MAPPING:
        return False
    return bool(_US_STOCK_PATTERN.match(normalized))


def is_hk_stock_code(code: str) -> bool:
    """
    判断代码是否为香港股票符号。

    港股代码格式：
    - HK 前缀 + 4-5 位数字（如 HK00700）
    - 4-5 位数字 + .HK 后缀（如 0700.HK）

    Args:
        code: 股票代码，如 'HK00700', '0700.HK'

    Returns:
        True 表示是港股符号，否则 False

    Examples:
        >>> is_hk_stock_code('HK00700')
        True
        >>> is_hk_stock_code('0700.HK')
        True
        >>> is_hk_stock_code('HK09988')
        True
        >>> is_hk_stock_code('AAPL')
        False
        >>> is_hk_stock_code('600519')
        False
    """
    normalized = (code or '').strip().upper()
    return bool(_HK_STOCK_PATTERN.match(normalized))


def get_us_index_yf_symbol(code: str) -> tuple:
    """
    获取美股指数的 Yahoo Finance 符号与中文名称。

    Args:
        code: 用户输入，如 'SPX', '^GSPC', 'DJI'

    Returns:
        (yf_symbol, chinese_name) 元组，未找到时返回 (None, None)。

    Examples:
        >>> get_us_index_yf_symbol('SPX')
        ('^GSPC', '标普500指数')
        >>> get_us_index_yf_symbol('AAPL')
        (None, None)
    """
    normalized = (code or '').strip().upper()
    return US_INDEX_MAPPING.get(normalized, (None, None))


def is_euronext_stock(code: str) -> bool:
    """
    判断代码是否为 Euronext 股票。

    Euronext 股票代码格式：1-6 个大写字母 + .XX 市场后缀
    支持的市场：
    - .PA (巴黎 - Paris)
    - .AS (阿姆斯特丹 - Amsterdam)
    - .BR (布鲁塞尔 - Brussels)
    - .DU (都柏林 - Dublin)
    - .LI (葡萄牙 - Lisbon)

    Args:
        code: 股票代码，如 'OR.PA', 'ASML.AS'

    Returns:
        True 表示是 Euronext 股票，否则 False

    Examples:
        >>> is_euronext_stock('OR.PA')
        True
        >>> is_euronext_stock('ASML.AS')
        True
        >>> is_euronext_stock('GBT.BR')
        True
        >>> is_euronext_stock('AAPL')
        False
    """
    normalized = (code or '').strip().upper()
    return bool(_EURONEXT_PATTERN.match(normalized))


def is_forex_pair(code: str) -> bool:
    """
    判断代码是否为支持的外汇对。

    支持的外汇对包括：
    - EURCNY (欧元/人民币)
    - USDCNY (美元/人民币)
    以及带 =X 后缀的变体

    Args:
        code: 外汇代码，如 'EURCNY', 'USDCNY', 'EURCNY=X'

    Returns:
        True 表示是支持的外汇对，否则 False

    Examples:
        >>> is_forex_pair('EURCNY')
        True
        >>> is_forex_pair('USDCNY')
        True
        >>> is_forex_pair('EURCNY=X')
        True
        >>> is_forex_pair('AAPL')
        False
    """
    normalized = (code or '').strip().upper()
    
    # 检查是否在支持的外汇对中
    if normalized in FOREX_PAIRS:
        return True
    
    # 检查是否匹配外汇对模式（6个字母或6个字母+Y/X后缀）
    if _FOREX_PATTERN.match(normalized):
        # 进一步验证是否为真实的外汇对（基础货币和计价货币都是有效的）
        # 对于现在支持的对：EURCNY, USDCNY
        if len(normalized) == 6:
            # EURCNY, USDCNY 等
            return normalized in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY']
        else:
            # EURCNY=X, USDCNY=X 等
            base = normalized[:-1]
            return base in ['EURCNY', 'USDCNY', 'GBPCNY', 'JPYCNY', 'CHFCNY']
    
    return False


def get_forex_yf_symbol(code: str) -> tuple:
    """
    获取外汇对的 Yahoo Finance 符号与中文名称。

    Args:
        code: 用户输入，如 'EURCNY', 'USDCNY', 'EURCNY=X'

    Returns:
        (yf_symbol, chinese_name) 元组，未找到时返回 (None, None)。

    Examples:
        >>> get_forex_yf_symbol('EURCNY')
        ('EURCNY=X', '欧元/人民币')
        >>> get_forex_yf_symbol('USDCNY')
        ('USDCNY=X', '美元/人民币')
        >>> get_forex_yf_symbol('AAPL')
        (None, None)
    """
    normalized = (code or '').strip().upper()
    return FOREX_PAIRS.get(normalized, (None, None))


def is_global_stock(code: str) -> bool:
    """
    判断代码是否为全球支持的股票或外汇对（除美股指数外）。

    支持的市场包括：
    - 美股 (美国)
    - Euronext (欧洲)
    - 港股 (香港)
    - 外汇对 (EURCNY, USDCNY 等)
    - 以及其他带市场后缀的代码

    Args:
        code: 股票代码或外汇代码

    Returns:
        True 表示支持，否则 False

    Examples:
        >>> is_global_stock('AAPL')
        True
        >>> is_global_stock('OR.PA')
        True
        >>> is_global_stock('0700.HK')
        True
        >>> is_global_stock('EURCNY')
        True
        >>> is_global_stock('USDCNY')
        True
        >>> is_global_stock('SPX')
        False (美股指数)
    """
    normalized = (code or '').strip().upper()
    
    # 排除美股指数
    if normalized in US_INDEX_MAPPING:
        return False
    
    # 美股
    if _US_STOCK_PATTERN.match(normalized):
        return True
    
    # Euronext
    if _EURONEXT_PATTERN.match(normalized):
        return True
    
    # 港股、其他带市场后缀的股票
    if any(suffix in normalized for suffix in GLOBAL_MARKET_SUFFIXES.keys()):
        return True
    
    # 外汇对
    if is_forex_pair(normalized):
        return True
    
    return False
