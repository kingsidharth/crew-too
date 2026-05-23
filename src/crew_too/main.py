import sys

from dotenv import load_dotenv

load_dotenv()

from crew_too.flows import SimpleSearchFlow, StockResearchFlow


def kickoff():
    """Entry point for `crewai run` / `crewai flow kickoff`.

    Usage:
        crewai run                          # prompts for flow choice
        python -m crew_too.main search "AI" # direct CLI
        python -m crew_too.main stock AAPL
    """
    args = sys.argv[1:]

    if not args or args[0] not in ("search", "stock"):
        flow_type = input("Choose flow (search / stock): ").strip().lower()
        if flow_type == "search":
            query = input("Enter search query: ").strip()
            _run_search(query)
        elif flow_type == "stock":
            ticker = input("Enter stock ticker: ").strip()
            _run_stock(ticker)
        else:
            print(f"Unknown flow: {flow_type}. Use 'search' or 'stock'.")
            sys.exit(1)
        return

    command = args[0]
    arg = " ".join(args[1:])

    if not arg:
        print(f"Missing argument for '{command}'")
        sys.exit(1)

    if command == "search":
        _run_search(arg)
    elif command == "stock":
        _run_stock(arg)


def _run_search(query: str):
    print(f"\n{'='*60}")
    print(f"Simple Search: {query}")
    print(f"{'='*60}\n")

    flow = SimpleSearchFlow()
    flow.kickoff(inputs={"query": query})

    print(f"\n{'='*60}")
    print("RESULT:")
    print(f"{'='*60}")
    print(flow.state["result"])


def _run_stock(ticker: str):
    print(f"\n{'='*60}")
    print(f"Stock Research: {ticker.upper()}")
    print(f"{'='*60}\n")

    flow = StockResearchFlow()
    flow.kickoff(inputs={"ticker": ticker.upper()})

    print(f"\n{'='*60}")
    print("FINAL REPORT:")
    print(f"{'='*60}")
    print(flow.state["report"])


def plot():
    """Visualize the stock research flow."""
    flow = StockResearchFlow()
    flow.plot()


if __name__ == "__main__":
    kickoff()
