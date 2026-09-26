import inspect
from collections import defaultdict

from core.modules.tools.base import Tool, ToolFunction
from core.modules.tools.events import Event


def load_tools(tools: dict[str, type[Tool]]) -> dict[Event, list[ToolFunction]]:
    loaded_tools: defaultdict[Event, list[ToolFunction]] = defaultdict(list)
    for tool in tools.values():
        tool_class = tool()
        for _, method in inspect.getmembers(tool_class, inspect.ismethod):
            if hasattr(method, "__event_name__"):
                loaded_tools[method.__event_name__].append(method)
    return dict(loaded_tools)
