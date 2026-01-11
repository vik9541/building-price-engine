"""Base parser class."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import logging
from requests import Session
from app.config import settings

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """Base class for competitor parsers."""
    
    def __init__(self):
        self.session = Session()
        self.session.headers.update({
            'User-Agent': settings.parser_user_agent
        })
        self.timeout = settings.parser_timeout
        self.retries = settings.parser_retries
    
    @abstractmethod
    def parse_products(self) -> List[Dict]:
        """Parse products from competitor site."""
        pass
    
    @abstractmethod
    def parse_product_details(self, product_url: str) -> Dict:
        """Parse product details from specific page."""
        pass
    
    def close(self):
        """Close session."""
        self.session.close()
