from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAgent:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
        self.model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
        self.labels = ["positive", "negative", "neutral"]

    def analyze(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        values = probs.detach().cpu().numpy()[0]
        result = {label: float(val) for label, val in zip(self.labels, values)}
        return result

if __name__ == "__main__":
    agent = SentimentAgent()
    print(agent.analyze("The company reported record earnings this quarter."))
