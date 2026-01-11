"""Obi.ru parser implementation."""
from app.parsers.base_parser import BaseParser
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ObiParser(BaseParser):
    """Parser for Obi.ru."""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.obi.ru"
    
    def parse_products(self) -> List[Dict]:
        """Parse products from Obi.ru."""
        logger.info("Starting Obi.ru parsing")
        # TODO: Implement actual parsing
        return []
    
    def parse_product_details(self, product_url: str) -> Dict:
        """Parse product details from Obi.ru."""
        # TODO: Implement actual parsing
        return {}
