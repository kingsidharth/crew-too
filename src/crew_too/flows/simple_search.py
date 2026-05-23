from crewai import Crew, Task
from crewai.flow import Flow, start

from crew_too.agent import create_search_agent


class SimpleSearchFlow(Flow):
    @start()
    def search(self):
        query = self.state["query"]

        agent = create_search_agent(topic="general", max_results=5)

        task = Task(
            description=f"Search for: {query}\n\nProvide a comprehensive summary of the findings.",
            expected_output="A clear, well-structured summary of search results with key facts and sources.",
            agent=agent,
        )

        crew = Crew(agents=[agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state["result"] = result.raw
        return result.raw
