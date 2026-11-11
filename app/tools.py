from datetime import datetime, timezone
from typing import Any, Callable, get_type_hints
from inspect import signature, Parameter

from pydantic import BaseModel, ConfigDict, create_model


# -------------------------
# Tool Functions
# -------------------------

def get_current_date() -> str:
    """Get the current date and time in UTC."""
    return datetime.now(timezone.utc).isoformat()


def count_words(text: str) -> int:
    """Count the number of words in a given text."""
    return len(text.split())


# -------------------------
# Tool Registry
# -------------------------

class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, Callable] = {}

    def register(self, function: Callable) -> None:

        if not callable(function):
            raise TypeError("Tool must be callable.")

        name = function.__name__

        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered.")

        if not function.__doc__:
            raise ValueError(f"Tool '{name}' must have a docstring.")

        self._tools[name] = function

    def get_tool(self, name: str) -> Callable:

        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered.")

        return self._tools[name]
    def get_all_tools(self) -> list[Callable]:
        return list(self._tools.values())

# -------------------------
# Argument Validator
# -------------------------

class ToolValidator:

    def __init__(self):
        self._models: dict[str, type[BaseModel]] = {}
        #the dict will store the models for each tool function, where the key is the function name and the value is the corresponding Pydantic model class.
    def get_validation_model(
        self,
        function: Callable
    ) -> type[BaseModel]:
        #function: A callable (function) for which we want to create a validation model.
        name = function.__name__

        if name in self._models:
            return self._models[name]

        sig = signature(function)
        # Get the signature of the function, which contains information about its parameters including types and defaults and return type.
        type_hints = get_type_hints(function)
        #get_type_hints retrieves the type hints (annotations) for the function's parameters and return type. It returns a dictionary where keys are parameter names and values are their corresponding types.
        fields = {}

        for param_name, param in sig.parameters.items():

            if param.kind not in (
                Parameter.POSITIONAL_OR_KEYWORD,
                Parameter.KEYWORD_ONLY,
            ):
                # If the parameter is not of type POSITIONAL_OR_KEYWORD or KEYWORD_ONLY, it raises a TypeError indicating that the parameter type is unsupported.
                #def x (a, b, /, c, *, d) -> None:  # a and b are positional-only, c is positional or keyword, d is keyword-only
                #def x (*args, **kwargs) -> None:  # args is variable positional and kwargs is keyword arguments
                # we need it this wat because LLM will return a dictionary of arguments and we will use it to call the function, so we need to make sure that the function can accept keyword arguments.
                raise TypeError(
                    f"Unsupported parameter type: {param_name}"
                )

            annotation = type_hints.get(param_name)

            if annotation is None:
                raise TypeError(
                    f"Parameter '{param_name}' needs a type annotation."
                )

            default = (
                param.default
                if param.default is not Parameter.empty
                else ...
            )
            # the 3 dots (...) are called "Ellipsis" and are used to indicate that the parameter is required and does not have a default value. In Pydantic, this is used to specify that a field is mandatory and must be provided when creating an instance of the model.
            # this is requi
            fields[param_name] = (annotation, default)
        #Dynamic Model Generation
        model = create_model(
            f"{name.title().replace('_', '')}Arguments",
            __config__=ConfigDict(
                extra="forbid",
                strict=True,
            ),
            **fields,
        )

        self._models[name] = model

        return model

    def validate(
        self,
        function: Callable,
        arguments: dict[str, Any]
    ) -> dict[str, Any]:

        model = self.get_validation_model(function)

        validated = model.model_validate(arguments)

        return validated.model_dump()


# -------------------------
# Tool Executor
# -------------------------

class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
        validator: ToolValidator,
    ):
        self.registry = registry
        self.validator = validator

    def execute(
        self,
        name: str,
        arguments: dict[str, Any]
    ) -> Any:

        function = self.registry.get_tool(name)

        validated_arguments = self.validator.validate(
            function,
            arguments,
        )

        return function(**validated_arguments)
class ToolSchemaGenerator:

    def __init__(self, validator: ToolValidator):
        self.validator = validator

    def generate(self, function: Callable) -> dict:

        model = self.validator.get_validation_model(function)

        return {
            "type": "function",
            "function": {
                "name": function.__name__,
                "description": function.__doc__.strip(),
                "parameters": model.model_json_schema(),
            },
        }


# -------------------------
# Initialization
# -------------------------

tool_registry = ToolRegistry()
tool_validator = ToolValidator()
tool_schema_generator = ToolSchemaGenerator(validator=tool_validator)

tool_registry.register(get_current_date)
tool_registry.register(count_words)

tool_executor = ToolExecutor(
    registry=tool_registry,
    validator=tool_validator,
)
