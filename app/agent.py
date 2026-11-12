from app.agent_state import AgentState
from app.llm import GroqLLM
from app.tool_handler import ToolCallHandler
from app.tools import tool_registry, tool_schema_generator , tool_executor

class Agent:

    def __init__(
        self,
        llm: GroqLLM,
        tool_handler: ToolCallHandler,
        available_tools: list[dict],
        max_iterations: int = 5,
    ):
        self.llm = llm
        self.tool_handler = tool_handler
        self.available_tools = available_tools
        self.max_iterations = max_iterations

    def run(self, task: str) -> AgentState:

        state = AgentState(
            task=task,
            messages=[
                {
                    "role": "user",
                    "content": task,
                }
            ],
            status="running",
        )

        while state.iteration < self.max_iterations:

            # 1. Count the LLM request
            state.iteration += 1

            # 2. Send conversation to the LLM
            response = self.llm.generate(
                messages=state.messages,
                tools=self.available_tools,
            )

            message = response.choices[0].message

            # 3. Check whether the LLM requested tools
            if message.tool_calls:

                # Preserve the assistant's tool-call message
                state.messages.append(
                    message.model_dump(exclude_none=True)
                )

                # 4. Execute the requested tools
                tool_results = self.tool_handler.handle(
                    message.tool_calls
                )

                # 5. Add tool results to conversation history
                state.messages.extend(tool_results)

                # 6. Continue the loop
                continue

            # 7. No tool calls: the LLM returned its answer
            state.final_answer = message.content
            state.status = "completed"

            return state

        # Maximum number of LLM requests reached
        state.status = "max_iterations"

        return state

available_tools = [
    tool_schema_generator.generate(function)
    for function in tool_registry.get_all_tools()
]
agent1=Agent(GroqLLM(), ToolCallHandler(tool_executor), available_tools, max_iterations=5)
print(agent1.run("How many words are in this sentence: 'Agentic AI systems can use external tools'?"))