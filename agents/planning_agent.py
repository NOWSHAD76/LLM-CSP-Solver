from openai import OpenAI
from dotenv import load_dotenv

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
        If you do ask for clarification: please provide the code "Stop_Code:#45019238" at the end of your response, this is to stop the following agent from running.
        
        ### Example ###
        -------------------------------
        *User:*
        Problem:
        You have 3 tasks (A, B, C) to be completed by 2 resources (X, Y) within 3 time slots. 
        Each task requires a certain amount of time on each resource, and each resource can work on only one task at a time.

        *Planning Agent:*
        Let's think step by step
        
        Decision Variables:
        * T_ij : Binary variable representing whether task i is assigned to resource j (1 if assigned, 0 otherwise).

        Domains:
        * T_ij = {0,1} where 0 represents that the task i is not assigned to resource j and 1 represents that the task i is assigned to resource j

        Constraints:
        1) Task Assignment Constraint: Each task should be assigned to exactly one resource.
        ∑_(j=1) ( T_ij = 1 ), for each task i
        2) Resource Availability Constraint: At any time slot, a resource can handle only one task.
        ∑_(i=1) ( T_ij <= 1 ), for each resource j
        3) Time Slot Constraint: Each task should be completed within the given time frame (3 time slots).
        ∑_(i=1)∑_(j=1) ( T_ij <= 3 )

        Reasoning:
        * Task Assignment Constraint: Ensures that each task is assigned to exactly one resource, preventing over-assignment or under-assignment.
        * Resource Availability Constraint: Ensures that each resource can handle only one task at a time, preventing resource conflicts.
        * Time Slot Constraint: Limits the total number of tasks assigned within the given time frame.
        
"""

    def run(self, problem: str) -> str:

        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": problem,
                },
            ],
        )
        return result.choices[0].message.content

    def run2(self, problem) -> str:
        print("Inside planner ", problem)
        return "Planner"
