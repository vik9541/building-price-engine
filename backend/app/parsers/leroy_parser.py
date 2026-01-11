"""Leroy Merlin parser implementation."""
from app.parsers.base_parser import BaseParser
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class LeroyParser(BaseParser):
    """Parser for Leroy Merlin."""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.leroymerlin.ru"
    
    def parse_products(self) -> List[Dict]:
        """Parse products from Leroy Merlin."""
        logger.info("Starting Leroy Merlin parsing")
        # TODO: Implement actual parsing
        return []
    
    def parse_product_details(self, product_url: str) -> Dict:
        """Parse product details from Leroy Merlin."""
        # TODO: Implement actual parsing
        return {}
