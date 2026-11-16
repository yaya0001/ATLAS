# ATLAS

## Overview

ATLAS is an experimental autonomous research agent. It sends a task to a Groq-hosted
language model, exposes tools the model can call, and returns the model's final
response. Its built-in tools retrieve the current UTC date and time, count words,
and search the web through Tavily.

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- API keys for [Groq](https://console.groq.com/keys) and
  [Tavily](https://app.tavily.com/)

### Installation

Clone the repository, enter its directory, and install the project and its
dependencies:

```bash
uv sync
```

Create a local environment file from the example:

```bash
cp .env.example .env
```

Edit `.env` and replace the example values with your API keys:

```dotenv
GROQ_API_KEY=your_groq_api_key
Tavily_API_KEY=your_tavily_api_key
```

The model can also be configured with `model_name`; it defaults to
`openai/gpt-oss-120b`. The settings loader reads `.env` from the project
directory. Keep real API keys private and do not commit `.env`.

## Usage

Start the command-line interface:

```bash
uv run python -m app.main
```

Enter a prompt when asked. ATLAS will respond after processing the task. The
agent can call its registered tools while working, with a maximum of five model
iterations by default.

The tools are:

- `get_current_date`: return the current date and time in UTC.
- `count_words`: count whitespace-separated words in text.
- `web_search`: search the web with Tavily (1–10 results per request).

## Development

Install the development dependencies as well:

```bash
uv sync --group dev
```

The repository includes pytest and Ruff as development dependencies. The files
under `test/` are currently standalone example/integration scripts; some make
live API requests and therefore require the corresponding API keys.

## Contributing

Contributions are welcome. Please keep changes focused, describe the motivation
and behavior in your pull request, and run the relevant checks before submitting.

## License

No license is currently specified in this repository.
