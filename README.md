## Connect 4 Agents

An arena for letting LLMs play Connect 4 against each other.

### Features
- Play Red vs Yellow using multiple hosted models via OpenRouter (Gemini 2.5, GPT-5 nano/OSS-120B, Claude Haiku 4.5, Grok 4.1 fast, Qwen3 235B, Kimi K2, DeepSeek v3.2 exp).
- Included the idea of [Visualization-of-Thought](https://arxiv.org/abs/2404.03622).

### Setup (uv)
1) Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2) Install deps: `uv sync`
3) Run the app: `uv run app.py` (launches browser by default).

### Required config
Create a `.env` in the project root with:
```
OPENROUTER_API_KEY=sk-...
```
You can optionally filter available models by setting `MODELS` to a comma-separated list matching the OpenRouter identifiers above.

### How it works
- `app.py` builds the Gradio interface.
- `arena/player.py` defines prompts and handles LLM outputs with JSON format.
- `arena/llm.py` routes all model calls through a single OpenRouter-backed `OpenAI` client.
