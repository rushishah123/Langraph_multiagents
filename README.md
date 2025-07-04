# LangGraph Multi-Agent Runner

This project shows how to build a simple multi step AI agent using
Python. Even if you are a beginner or a young coder you can follow the
steps below to run the example.

## Folder Layout

```
examples/        # example YAML and JSON agent specs
src/             # Python code for the agent runner and tools
run_agent.py     # command line program to run the agent
requirements.txt # Python packages you need to install
```

## Setup

1. **Install Python** – Make sure Python 3.10 or newer is on your
   computer. In PyCharm you can create a new project with this code.
2. **Install packages** – Open a terminal and run:

```bash
pip install -r requirements.txt
```

(If you do not have an OpenAI API key the program will use mocked
responses.)

## Running the Example

Inside the `examples` folder there are two config files: `config.yaml`
and `config.json`. They describe a tiny agent with three steps:

1. **think** – the agent first thinks about the user input.
2. **search** – it then calls a mock web search tool.
3. **summarize** – finally it summarizes what it found.

Run the agent with:

```bash
python run_agent.py --spec examples/config.yaml --input "2+2"
```

You will see the final answer and a JSON trace of everything the agent
did.

If you have an OpenAI API key set the environment variable
`OPENAI_API_KEY` to let the agent talk to the real API:

```bash
export OPENAI_API_KEY="sk-..."
```

## Adding Your Own Tools

You can create new tools inside `src/tools.py`. Each tool is a small
Python class with a `run` method that accepts a string and returns a
string. Update the YAML/JSON spec to reference your tool by name and the
`AgentRunner` will load it automatically.

## How It Works

The `AgentRunner` class reads the YAML or JSON file, validates it using
pydantic and then executes each step. Prompts for the language model are
chosen based on the step `role`. When a tool is specified the output of
the previous step is passed to the tool instead of the LLM. Every action
is stored in the trace.

Have fun experimenting and building your own agents!
