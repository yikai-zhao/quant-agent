import datetime

class ReportAgent:
    def __init__(self, output_path="examples/sample_report.md"):
        self.output_path = output_path

    def generate(self, text: str, sentiment: dict):
        now = datetime.datetime.now().strftime("%%Y-%%m-%%d %%H:%%M:%%S")
        lines = []
        lines.append("# Investment Sentiment Report\n")
        lines.append(f"Date: {now}\\n")
        lines.append(f"Text Analyzed: {text}\\n")
        lines.append("## Sentiment Analysis\\n")
        lines.append(f"- Positive: {sentiment['positive']}\\n")
        lines.append(f"- Negative: {sentiment['negative']}\\n")
        lines.append(f"- Neutral: {sentiment['neutral']}\\n")
        lines.append("## Conclusion\\n")
        lines.append(f"The sentiment analysis suggests that the overall market tone is {max(sentiment, key=sentiment.get)}.")
        report = "\n".join(lines)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(report)
        return self.output_path
