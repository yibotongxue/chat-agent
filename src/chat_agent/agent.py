from .llm.base import BaseLLM
from .utils.types import InputData
from .search.base import BaseSearch

class Agent:
    def __init__(self, llm: BaseLLM, search: BaseSearch, system_prompt: str = "") -> None:
        self.llm = llm
        self.search = search
        self.system_prompt = system_prompt
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def chat(self, text: str, ) -> str:
        messages = self.messages + [{"role": "user", "content": text}]
        input_data = InputData(messages=messages, meta_data={})
        output_data = self.llm.generate(input_data)
        if output_data.is_tool_calling and output_data.search_query:
            query = output_data.search_query
            results = self.search.search(query)
            messages = self.messages + [{"role": "user", "content": text + f"\nSearch Results:\n" + '\n'.join(results)}]
            input_data = InputData(messages=messages, meta_data={})
            output_data = self.llm.generate(input_data)
        self.messages.append({"role": "user", "content": text})
        self.messages.append({"role": "assistant", "content": output_data.response})
        return output_data.response

def main() -> None:
    import os

    from dotenv import load_dotenv
    load_dotenv()

    from .llm.openai_llm import OpenAILLM
    from .search.mock import MockSearch

    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    llm = OpenAILLM(model_cfgs={"api_key": api_key}, inference_cfgs={})
    search = MockSearch(search_cfgs={})
    system_prompt = "你是一个人工智能助手。你可以调用搜索工具，如果你决定调用搜索工具，请在回复的最后用<search_query></query>标签包裹搜索查询。如果决定需要查询，请只返回搜索查询，不要包含其他内容。查询结果将作为用户输入给出，如果用户输入包含了查询结果，请不要再使用搜索工具。"
    agent = Agent(llm=llm, search=search, system_prompt=system_prompt)
    while True:
        user_input = input("User: ")
        if user_input.lower() in {"exit", "quit"}:
            break
        response = agent.chat(user_input)
        print("Agent:", response)

if __name__ == "__main__":
    main()
