# crew-too

CrewAI search agent with two flows: **simple search** and **stock research**.

## Installation

```bash
# clone & enter
cd crew-too

# install deps
crewai install
```

### API Keys

```bash
cp .env.example .env
```

Open `.env` and add your keys:

| Key | Get it at | Required |
|-----|-----------|----------|
| `TAVILY_API_KEY` | [tavily.com](https://app.tavily.com/home) | Yes |
| `OPENROUTER_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) | Yes (or use OpenAI) |
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Only if no OpenRouter key |

If `OPENROUTER_API_KEY` is set, it takes priority. Otherwise falls back to `OPENAI_API_KEY`.

You can override the model via `OPENROUTER_MODEL` or `OPENAI_MODEL` in `.env`.

## Usage

### Simple search

```bash
crewai run search "NVIDIA AI chip demand 2025"
```

### Stock research

Runs a multi-step flow: company overview -> news + financials (parallel) -> synthesized report.

```bash
crewai run stock NVDA
```

### Interactive mode

```bash
crewai run
# prompts: Choose flow (search / stock)
# prompts: Enter search query / Enter stock ticker
```

### Visualize the flow

```bash
crewai flow plot
```

## Project structure

```
src/crew_too/
  agent.py                 # single search agent (Tavily + OpenRouter/OpenAI)
  main.py                  # CLI entry point
  flows/
    simple_search.py       # query -> search -> summary
    stock_research.py      # ticker -> overview -> news + financials -> report
```

## Stock research flow

```
          [company_overview]
               /       \
    [recent_news]   [financial_analysis]    <- parallel
               \       /
         [synthesize_report]
```
