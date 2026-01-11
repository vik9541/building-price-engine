"""Image handling utilities."""
import os
import logging
from pathlib import Path
from PIL import Image
from app.config import settings

logger = logging.getLogger(__name__)


class ImageHandler:
    """Handle product images."""
    
    def __init__(self):
        self.storage_path = Path(settings.image_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, image_data: bytes, filename: str) -> str:
        """Save image to storage."""
        try:
            file_path = self.storage_path / filename
            
            # Save image
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            # Verify image
            Image.open(file_path).verify()
            
            logger.info(f"Image saved: {filename}")
            return str(file_path)
        
        except Exception as e:
            logger.error(f"Error saving image {filename}: {str(e)}")
            return None
