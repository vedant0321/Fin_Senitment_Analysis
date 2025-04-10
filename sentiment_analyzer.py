from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

class FinBERTSentimentAnalyzer:
    def __init__(self):
        # Load FinBERT model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        self.labels = ["negative", "neutral", "positive"]
        
    def analyze(self, text):
        """Analyze sentiment of financial text using FinBERT."""
        if not text or len(text.strip()) == 0:
            return {"label": "neutral", "score": 0.0}
            
        # Truncate text if too long
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
            
        # Tokenize and predict
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Get prediction
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=1).detach().numpy()[0]
        predicted_class = np.argmax(probabilities)
        
        return {
            "label": self.labels[predicted_class],
            "score": float(probabilities[predicted_class]),
            "scores": {label: float(prob) for label, prob in zip(self.labels, probabilities)}
        }