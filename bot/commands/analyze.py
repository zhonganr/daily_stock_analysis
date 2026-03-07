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
    Stock Analysis Command
    
    Analyze specified stock code and generate AI analysis report.
    
    Usage:
        /analyze 600519       - Analyze Moutai (simple report)
        /analyze 600519 full  - Analyze and generate full report
    """
    
    @property
    def name(self) -> str:
        return "analyze"
    
    @property
    def aliases(self) -> List[str]:
        return ["a", "analyze", "analysis"]
    
    @property
    def description(self) -> str:
        return "Analyze specified stock"
    
    @property
    def usage(self) -> str:
        return "/analyze <stock_code> [full]"
    
    def validate_args(self, args: List[str]) -> Optional[str]:
        """Validate arguments"""
        if not args:
            return "Please provide a stock code"
        
        code = args[0].upper()

        # Validate stock code format: HK, US, Euronext, Forex
        # HK: 0+4 digits+.HK
        # US: 1-5 uppercase letters+.+2 suffix letters
        # Euronext: 1-6 letters+.+market suffix(PA|AS|BR|DU|LI)
        # Forex: 6 letters(e.g. EURCNY) or 6 letters+X suffix(e.g. EURCNY=X)
        
        # Use imported validation functions
        from data_provider import is_global_stock, is_forex_pair
        
        # Check if it's a US index (exclude)
        from data_provider import is_us_index_code
        if is_us_index_code(code):
            return f"US index codes not supported: {code} (please provide specific stock code)"
        
        # Check if it's a valid global stock or forex pair
        if is_global_stock(code):
            return None
        
        return f"Invalid stock code: {code} (supported: HK 0000.HK / US stocks / Euronext / Forex)"
    
    def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
        """Execute analysis command"""
        code = canonical_stock_code(args[0])
        
        # Check if full report is needed (default simple, pass full/complete/detailed to switch)
        report_type = "simple"
        if len(args) > 1 and args[1].lower() in ["full", "complete", "detailed"]:
            report_type = "full"
        logger.info(f"[AnalyzeCommand] Analyzing stock: {code}, report type: {report_type}")
        
        try:
            # Call analysis service
            from src.services.task_service import get_task_service
            from src.enums import ReportType
            
            service = get_task_service()
            
            # Submit async analysis task
            result = service.submit_analysis(
                code=code,
                report_type=ReportType.from_str(report_type),
                source_message=message
            )
            
            if result.get("success"):
                task_id = result.get("task_id", "")
                return BotResponse.markdown_response(
                    f"✅ **Analysis Task Submitted**\n\n"
                    f"• Stock Code: `{code}`\n"
                    f"• Report Type: {ReportType.from_str(report_type).display_name}\n"
                    f"• Task ID: `{task_id[:20]}...`\n\n"
                    f"Results will be automatically sent when analysis is complete."
                )
            else:
                error = result.get("error", "Unknown error")
                return BotResponse.error_response(f"Failed to submit analysis task: {error}")
                
        except Exception as e:
            logger.error(f"[AnalyzeCommand] Execution failed: {e}")
            return BotResponse.error_response(f"Analysis failed: {str(e)[:100]}")
