from openai import OpenAI
import os
import json
from datetime import datetime
from .utils import clean_json_tags
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


ROOT_SYS_PROMPT = """
用户会输入一段文字，会包含todo-list相关的多个指令。你的职责是：判断用户的意图，明确区分出每一个指令，并输出一个 JSON 指令列表。
注意：日程安排是todo-list的一部分。不要单独区分日程安排。
输出格式必须严格符合以下规范（不要输出多余文字）：
```json
[
    {
        "用户的输入": "用户输入的原始文字",
        "用户意图": "修改todo-list"/"查询todo-list"/"普通聊天",
        "指令或提问": "指令/提问/其他",
        "待办事项具体与否": "是/否",
        "原因说明": "简短说明你是如何分析用户意图的"    
    },
    ...
]
```
"""


INFO_EXTRACTION_SYS_PROMPT = """
你是信息提取助手，负责从用户的自然语言输入中提取出事项的核心信息，并以 JSON 格式输出。
```json
{
    "事项名称": "提取用户输入的事项中最核心的任务或动作",
    "备注": "用于补充附加信息，如时间、地点、人物、条件、原因等。如果输入中没有额外说明，可留空字符串。"
}
```
"""

READ_TODO_SYS_PROMPT = f"""
你是信息提取助手，遵从用户指令，从下面todo-list中提取信息给用户。

整个用户的todo-list如下：\n
"""

class RootAgent:
    def __init__(self):
        # self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.json_file = "todos.json"
        if not os.path.exists(self.json_file):
            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)
        self.function_calls = {
            "write_todo": self.write_todo,
            "read_todo": self.read_todo
        }

    def recognize_intent(self, user_content):
        root_messages = [{"role": "system", "content": ROOT_SYS_PROMPT}]
        root_messages.append({"role": "user", "content": user_content})
        yield "思考用户的意图..."
        response_message = self.get_generation(root_messages)
        content = clean_json_tags(response_message.content)
        print(content)
        # yield "反思一遍..."
        # reflection_messages = [{"role": "system", "content": REFLECTION_SYS_PROMPT}]
        # reflection_messages.append({"role": "user", "content": content})
        # reflection_message = self.get_generation(reflection_messages)
        # content = clean_json_tags(reflection_message.content)
        items = json.loads(content)
        for item in items:
            result_message = None
            if item["用户意图"] == "修改todo-list":
                result_message = self.write_todo(item["用户的输入"])
            elif item["用户意图"] == "查询todo-list":
                result_message = self.read_todo(item["用户的输入"])
            else:
                result_message = self.normal_chat(item["用户的输入"])
            yield result_message

    def get_generation(self, messages):
        response = self.client.chat.completions.create(
        # model="deepseek-chat",
        model="gpt-4o-mini",
        messages=messages
        )    
        return response.choices[0].message

    def write_todo(self, user_content):

        delete_phrases = [
            "把所有待办都删掉",
            "清除全部任务",
            "删除所有事项",
            "把待办列表清空",
            "全部日程都不要了",
            "把待办清一清",
            "把之前的任务全去掉",
            "清理一下所有待办内容",
            "把所有事项都移除",
            "删光所有待办事项",
            "清空todo-list"
        ]
        for phrase in delete_phrases:
            if similar(user_content, phrase) > 0.6:
                with open(self.json_file, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4, ensure_ascii=False)
                return "所有待办事项已清空。\n当前todo-list为空。"

        info_extraction_messages = [{"role": "system", "content": INFO_EXTRACTION_SYS_PROMPT}]
        info_extraction_messages.append({"role": "user", "content": user_content})
        response_message = self.get_generation(info_extraction_messages)
        info = clean_json_tags(response_message.content)
        info_extraction_messages.append({"role": "assistant", "content": info})

        json_todo_item = json.loads(info)
        json_todo_item["创建时间"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_todo_item["完成状态"] = False

        with open(self.json_file, "r", encoding="utf-8") as f:
            try:
                todo_list = json.load(f)
            except json.JSONDecodeError:
                todo_list = []

        todo_list.append(json_todo_item)

        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(todo_list, f, indent=4, ensure_ascii=False)

        return f"事项：{json_todo_item['事项名称']}，备注：{json_todo_item['备注']}，已记录完成"

    def read_todo(self, user_content):

        with open(self.json_file, "r", encoding="utf-8") as f:
            read_todo_messages = [{"role": "system", "content": READ_TODO_SYS_PROMPT + f.read()}]
        read_todo_messages.append({"role": "user", "content": user_content})
        response_message = self.get_generation(read_todo_messages)
        return response_message.content


    def normal_chat(self, user_content):
        return f"和用户正在普通聊天"
    # def store_todo(self, user_content):
    #     # use the user_content to create a new todo item
    #     # save the todo item to json file

    #     new_dummy_todo = {
    #         "id": 37261,
    #         "title": "Read react tutorial",
    #         "description": "Read the react tutorial to learn the basics of react",
    #         "completed": False,
    #         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }
        
    #     todos = []
    #     if os.path.exists(self.json_file):
    #         with open(self.json_file, "r") as f:
    #             try:
    #                 todos = json.load(f)
    #             except json.JSONDecodeError:
    #                 todos = []

    #     todos.append(new_dummy_todo)

    #     with open(self.json_file, "w") as f:
    #         json.dump(todos, f, indent=4, ensure_ascii=False)
    #     return "Todo stored successfully"