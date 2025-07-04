import argparse
import json
from pprint import pprint

from src.agent_runner import AgentRunner


def main():
    parser = argparse.ArgumentParser(description="Run LangGraph agent")
    parser.add_argument("--spec", required=True, help="Path to YAML/JSON spec")
    parser.add_argument("--input", required=True, help="Input text")
    args = parser.parse_args()

    runner = AgentRunner(args.spec)
    result, trace = runner.run(args.input)

    print("Final Result:\n", result)
    print("\nExecution Trace:")
    print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()
