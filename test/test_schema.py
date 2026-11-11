from pprint import pprint

from app.tools import (
    tool_registry,
    tool_schema_generator,
)

function = tool_registry.get_tool("count_words")

schema = tool_schema_generator.generate(function)

pprint(schema)