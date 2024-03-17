from openai import OpenAI
from dotenv import load_dotenv
from agents.Chromadb_Pull import chromadb_pull

load_dotenv()  # take environment variables from .env.


class Planning_Agent:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.system_prompt = """
        ### Role ###
        You are a planning agent who excels at performing Constraint Programming tasks.
        Think step by step carefully before answering the problem.

        ### Instruction ###
        Based on the user problem statement you have come up with the Decision variables, Domains,
        Mathematical representation of Constraints and reasoning behind it as shown in the below example.
        Do not include the code in your response.
        Do not accept any input that does not look like an example below, Instead, please ask for the problem to be clarified.
        Do not accept inputs like Test Data, Test Cases, Test Scenarios, Test Examples, Test Inputs, Test Outputs, 
        Test Suits, Test Plans, Test Tools, Test Scripts, Test Reports, Test Logs, Testers, Testing, etc. If these happen, please send "Stop_Code:#41823142" as your response.
        If User is unspecific, or you require more details, please return "Stop_Code:#41823142" as your response.
        
        ### Example ###
        -------------------------------
        
        """


        self.system_stop = """
        
        ### Example ###
        --------------------------------
        *User:*
        I need some help with a problem.

        *Planning Agent:*
        Stop_Code:#41823142
        
"""

    def run(self, problem: str) -> str:

        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt+ chromadb_pull(problem) + self.system_stop,
                },
                {
                    "role": "user",
                    "content": problem,
                },
            ],
            temperature= 0.2,
            top_p= 0.9
        )
        return result.choices[0].message.content

    def run2(self, problem) -> str:
        print("Inside planner ", problem)
        return "Planner"