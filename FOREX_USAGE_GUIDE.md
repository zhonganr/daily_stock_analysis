#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
STOCK_LIST 中使用外汇对 - 示例与验证
===================================

展示如何在 STOCK_LIST 配置中直接使用外汇对
"""

import importlib.util

# 直接载入配置模块
spec = importlib.util.spec_from_file_location(
    "us_index_mapping",
    "data_provider/us_index_mapping.py"
)
us_index_mapping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(us_index_mapping)

is_global_stock = us_index_mapping.is_global_stock


def demo_stock_list_with_forex():
    """演示 STOCK_LIST 中包含外汇对的使用"""
    print("\n" + "=" * 60)
    print("📋 STOCK_LIST 中使用外汇对 - 示例")
    print("=" * 60)
    
    # 示例 1: 只有外汇对
    example1 = "EURCNY,USDCNY,GBPCNY"
    print(f"\n示例 1 - 只监控外汇对:")
    print(f"  STOCK_LIST={example1}")
    print(f"  解析为: {example1.split(',')}")
    
    # 示例 2: 混合美股和外汇
    example2 = "AAPL,TSLA,EURCNY,USDCNY"
    print(f"\n示例 2 - 混合美股和外汇对:")
    print(f"  STOCK_LIST={example2}")
    print(f"  解析为: {example2.split(',')}")
    
    # 示例 3: 混合所有市场
    example3 = "AAPL,0700.HK,OR.PA,ASML.AS,EURCNY,USDCNY"
    print(f"\n示例 3 - 混合全球各市场:")
    print(f"  STOCK_LIST={example3}")
    print(f"  解析为: {example3.split(',')}")
    
    return [example1, example2, example3]


def validate_stock_list_items(stock_list_str: str) -> bool:
    """验证 STOCK_LIST 所有项是否都被支持"""
    print(f"\n  ✓ 验证: STOCK_LIST={stock_list_str}")
    
    items = [c.strip().upper() for c in stock_list_str.split(',') if c.strip()]
    
    all_valid = True
    for code in items:
        valid = is_global_stock(code)
        status = "✅" if valid else "❌"
        print(f"    {status} {code:15} -> {'支持' if valid else '不支持'}")
        if not valid:
            all_valid = False
    
    return all_valid


def demo_usage_commands():
    """展示在命令中使用外汇对"""
    print("\n" + "=" * 60)
    print("🤖 Bot 命令中使用外汇对")
    print("=" * 60)
    
    commands = [
        ("/analyze EURCNY", "分析欧元/人民币"),
        ("/analyze EURCNY full", "完整分析EUR/CNY"),
        ("/ask USDCNY", "使用默认策略分析美元/人民币"),
        ("/ask EURCNY 缠论分析", "使用缠论分析欧元/人民币"),
        ("/ask GBPCNY 波浪理论", "使用波浪理论分析英镑/人民币"),
    ]
    
    for cmd, description in commands:
        print(f"\n  > {cmd}")
        print(f"    说明: {description}")


def main():
    print("\n" + "="*60)
    print("外汇对使用指南")
    print("="*60)
    
    # 展示示例
    examples = demo_stock_list_with_forex()
    
    # 验证示例
    print("\n" + "=" * 60)
    print("✓ 验证示例配置")
    print("=" * 60)
    
    all_passed = True
    for example in examples:
        if not validate_stock_list_items(example):
            all_passed = False
    
    # 展示命令用法
    demo_usage_commands()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 总结")
    print("=" * 60)
    
    print("""
✅ 外汇对完全支持！

配置步骤：
  1. 编辑 .env 文件
  2. 在 STOCK_LIST 中添加外汇对（与其他股票用逗号分隔）
  3. 支持的外汇对：EURCNY, USDCNY, GBPCNY, JPYCNY, CHFCNY
  4. 也支持 =X 后缀格式：EURCNY=X, USDCNY=X 等

命令使用：
  - /analyze EURCNY       # 分析欧元/人民币
  - /ask USDCNY           # 用策略分析美元/人民币
  
注意：
  - 代码自动转为大写（不区分大小写）
  - 香港股票支持两种格式：0700.HK 和 HK0700
  - 目前仅YFinance支持外汇（其他数据源已移除）
    """)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    exit(main())
