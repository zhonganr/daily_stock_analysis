# -*- coding: utf-8 -*-
"""
===================================
股票分析命令
===================================

分析指定股票，调用 AI 生成分析报告。
"""

import re
import logging
from typing import List, Optional

from bot.commands.base import BotCommand
from bot.models import BotMessage, BotResponse
from data_provider.base import canonical_stock_code

logger = logging.getLogger(__name__)


class AnalyzeCommand(BotCommand):
    """
    股票分析命令
    
    分析指定股票代码，生成 AI 分析报告并推送。
    
    用法：
        /analyze 600519       - 分析贵州茅台（精简报告）
        /analyze 600519 full  - 分析并生成完整报告
    """
    
    @property
    def name(self) -> str:
        return "analyze"
    
    @property
    def aliases(self) -> List[str]:
        return ["a", "分析", "查"]
    
    @property
    def description(self) -> str:
        return "分析指定股票"
    
    @property
    def usage(self) -> str:
        return "/analyze <股票代码> [full]"
    
    def validate_args(self, args: List[str]) -> Optional[str]:
        """验证参数"""
        if not args:
            return "请输入股票代码"
        
        code = args[0].upper()

        # 验证股票代码格式：港股、美股、Euronext、外汇
        # 港股：0+4位数字+.HK
        # 美股：1-5个大写字母+.+2个后缀字母
        # Euronext: 1-6个字母+.+市场后缀(PA|AS|BR|DU|LI)
        # 外汇：6个字母(如 EURCNY) 或 6个字母+X后缀(如 EURCNY=X)
        
        # 使用导入的全局验证函数
        from data_provider import is_global_stock, is_forex_pair
        
        # 检查是否是美股指数（排除）
        from data_provider import is_us_index_code
        if is_us_index_code(code):
            return f"不支持美股指数代码: {code}（请输入具体股票代码）"
        
        # 检查是否是有效的全球股票或外汇对
        if is_global_stock(code):
            return None
        
        return f"无效的股票代码: {code}（支持: 港股0000.HK / 美股 / Euronext / 外汇）"
    
    def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
        """执行分析命令"""
        code = canonical_stock_code(args[0])
        
        # 检查是否需要完整报告（默认精简，传 full/完整/详细 切换）
        report_type = "simple"
        if len(args) > 1 and args[1].lower() in ["full", "完整", "详细"]:
            report_type = "full"
        logger.info(f"[AnalyzeCommand] 分析股票: {code}, 报告类型: {report_type}")
        
        try:
            # 调用分析服务
            from src.services.task_service import get_task_service
            from src.enums import ReportType
            
            service = get_task_service()
            
            # 提交异步分析任务
            result = service.submit_analysis(
                code=code,
                report_type=ReportType.from_str(report_type),
                source_message=message
            )
            
            if result.get("success"):
                task_id = result.get("task_id", "")
                return BotResponse.markdown_response(
                    f"✅ **分析任务已提交**\n\n"
                    f"• 股票代码: `{code}`\n"
                    f"• 报告类型: {ReportType.from_str(report_type).display_name}\n"
                    f"• 任务 ID: `{task_id[:20]}...`\n\n"
                    f"分析完成后将自动推送结果。"
                )
            else:
                error = result.get("error", "未知错误")
                return BotResponse.error_response(f"提交分析任务失败: {error}")
                
        except Exception as e:
            logger.error(f"[AnalyzeCommand] 执行失败: {e}")
            return BotResponse.error_response(f"分析失败: {str(e)[:100]}")
