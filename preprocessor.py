import re
import html
from bs4 import BeautifulSoup

class TextPreprocessor:
    @staticmethod
    def preprocess(text):
        """Clean and preprocess text data."""
        if not text:
            return ""
            
        # Convert to string if not already
        text = str(text)
        
        # Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()
        
        # Unescape HTML entities
        text = html.unescape(text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text