from crewai import Crew, Task
from crewai.flow import Flow, start, listen, and_

from crew_too.agent import create_search_agent


class StockResearchFlow(Flow):
    @start()
    def company_overview(self):
        ticker = self.state["ticker"]

        agent = create_search_agent(topic="general", max_results=5)
        task = Task(
            description=(
                f"Research the company behind stock ticker '{ticker}'. "
                f"Find: what the company does, its sector/industry, key products or services, "
                f"market cap, CEO, and headquarters."
            ),
            expected_output="A concise company profile covering business model, sector, leadership, and scale.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state["overview"] = result.raw
        return result.raw

    @listen("company_overview")
    def recent_news(self):
        ticker = self.state["ticker"]

        agent = create_search_agent(topic="news", max_results=5)
        task = Task(
            description=(
                f"Find the latest news and developments for '{ticker}' from the past week. "
                f"Focus on earnings, product launches, partnerships, regulatory actions, "
                f"and analyst upgrades/downgrades."
            ),
            expected_output="A summary of the most important recent news items with dates and impact assessment.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state["news"] = result.raw
        return result.raw

    @listen("company_overview")
    def financial_analysis(self):
        ticker = self.state["ticker"]

        agent = create_search_agent(topic="finance", max_results=5)
        task = Task(
            description=(
                f"Research the financial health and valuation of '{ticker}'. "
                f"Find: current stock price, P/E ratio, revenue growth, profit margins, "
                f"debt-to-equity, analyst price targets, and recent earnings results."
            ),
            expected_output="A financial snapshot with key metrics, valuation assessment, and analyst consensus.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state["financials"] = result.raw
        return result.raw

    @listen(and_("recent_news", "financial_analysis"))
    def synthesize_report(self):
        ticker = self.state["ticker"]
        overview = self.state.get("overview", "N/A")
        news = self.state.get("news", "N/A")
        financials = self.state.get("financials", "N/A")

        agent = create_search_agent(topic="general", max_results=3)
        task = Task(
            description=(
                f"Synthesize a stock research report for '{ticker}' using these inputs:\n\n"
                f"## Company Overview\n{overview}\n\n"
                f"## Recent News\n{news}\n\n"
                f"## Financial Analysis\n{financials}\n\n"
                f"Create a final investment research report that includes:\n"
                f"1. Executive Summary\n"
                f"2. Business Overview\n"
                f"3. Financial Highlights\n"
                f"4. Recent Developments\n"
                f"5. Key Risks\n"
                f"6. Outlook & Conclusion"
            ),
            expected_output=(
                "A well-structured stock research report with all six sections, "
                "suitable for an investor audience."
            ),
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state["report"] = result.raw
        return result.raw
