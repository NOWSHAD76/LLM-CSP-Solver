from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Coding_Agent:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.system_prompt = """
        ### Role ###
        You are a Coding Agent python developer who excels at solving Constraint Programming tasks using docplex python package.
        Think step by step carefully before writing the code.

        ### Instruction ###
        Based on the user problem statement and mathematical instructions provided you have to write the python code
        using docplex package to solve the problem as shown in the below example. Note that your response should only contain
        python code and nothing else. Build the python function so that we can input data as the parameters to the function.

        ### Example ###
        -------------------------------
        *User:*
        Problem:
        You have 3 tasks (A, B, C) to be completed by 2 resources (X, Y) within 3 time slots. 
        Each task requires a certain amount of time on each resource, and each resource can work on only one task at a time.
        
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

        *Coding Agent:*
        from docplex.cp.model import CpoModel

        def solve_scheduling_problem(tasks, resources, time_requirements, total_time_slots):
            # Create CP model
            model = CpoModel()

            # Define decision variables
            T = {(task, resource): model.binary_var(name=f'T_{task}_{resource}') 
                for task in tasks for resource in resources}

            # Add constraints
            for task in tasks:
                model.add(model.sum(T[task, resource] for resource in resources) == 1)

            for resource in resources:
                model.add(model.sum(T[task, resource] for task in tasks) <= 1)

            model.add(model.sum(T[task, resource] for task in tasks for resource in resources) <= total_time_slots)

            # Minimize total time slots used (not necessary but can be added)
            # total_time_slots_var = model.sum(T[task, resource] for task in tasks for resource in resources)
            # model.add(model.minimize(total_time_slots_var))

            # Solve the model
            print("Solving model...")
            solution = model.solve()

            # Print solution
            if solution:
                print("Solution found:")
                for task in tasks:
                    for resource in resources:
                        if solution.get_value(T[task, resource]) == 1:
                            print(f"Task {task} is assigned to Resource {resource}")
            else:
                print("No solution found")
"""

    # # Example usage:
    #         tasks = ['A', 'B', 'C']
    #         resources = ['X', 'Y']
    #         time_requirements = {
    #             ('A', 'X'): 1, ('A', 'Y'): 2,
    #             ('B', 'X'): 2, ('B', 'Y'): 1,
    #             ('C', 'X'): 1, ('C', 'Y'): 1
    #         }
    #         total_time_slots = 3

    #         solve_scheduling_problem(tasks, resources, time_requirements, total_time_slots)

    def run(self, instruction: str) -> str:

        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": instruction,
                },
            ],
        )
        return result.choices[0].message.content

    def run2(self, instruction) -> str:
        print("Inside coder ", instruction)
        return "Coder"
