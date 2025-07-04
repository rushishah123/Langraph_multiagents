import math

class Tool:
    name: str

    def run(self, input_text: str) -> str:
        raise NotImplementedError

class WebSearchTool(Tool):
    name = "web_search"

    def run(self, query: str) -> str:
        # Mock search implementation
        return f"[Mocked search results for '{query}']"

class CalculatorTool(Tool):
    name = "calculator"

    def run(self, expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}}, math.__dict__)
        except Exception as e:
            result = f"Error: {e}"
        return str(result)

def load_tool(tool_type: str) -> Tool:
    if tool_type == "web_search":
        return WebSearchTool()
    if tool_type == "calculator":
        return CalculatorTool()
    raise ValueError(f"Unknown tool type: {tool_type}")
