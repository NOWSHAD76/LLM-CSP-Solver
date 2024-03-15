import autogen
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Code_Execution_Agent:
    def __init__(self) -> None:
        # self.config_list = [{"model": "gpt-3.5-turbo"}]
        self.assistant = autogen.AssistantAgent(
            name="code analyzer",
            llm_config={"config_list": [{"model": "gpt-3.5-turbo"}]},
            # the default system message of the AssistantAgent is overwritten here
            # system_message="""
            # You are a helpful AI assistant.
            # You will be given a python code and input parameters to a function present in the code.
            # Pass this information after parsing for another AI assistant to execute and give the results.
            # Finally, inspect the execution result. If the execution is wrong, analyze the error and suggest a fix.
            # """,
        )
        self.proxy_user = autogen.UserProxyAgent(
            name="code executioner",
            max_consecutive_auto_reply=0,  # terminate without auto-reply
            human_input_mode="NEVER",
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,
            },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        )

    def run(self, message: str):
        chat_res = self.proxy_user.initiate_chat(
            self.assistant,
            message=message,
            # summary_method="reflection_with_llm",
        )
        # print(chat_res.chat_history)
        return chat_res.chat_history
