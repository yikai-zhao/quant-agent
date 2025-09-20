from sentiment_agent import SentimentAgent
from report_agent import ReportAgent

class Orchestrator:
    def __init__(self):
        self.sentiment_agent = SentimentAgent()
        self.report_agent = ReportAgent()

    def run(self, text: str):
        sentiment = self.sentiment_agent.analyze(text)
        report_path = self.report_agent.generate(text, sentiment)
        return f"Report generated at {report_path}"

if __name__ == "__main__":
    orch = Orchestrator()
    print(orch.run("Tesla announced a major breakthrough in battery technology."))
