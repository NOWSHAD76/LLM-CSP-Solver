from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Executor_Agent:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.system_prompt = """
        ### Role ###
        You are a Executor agent python developer who excels at understanding python code solving mainly 
        Constraint Programming tasks using docplex python package.

        ### Instruction ###
        Based on the given problem and code you have to generate the arguments that are passed to the python 
        function and give appropriate example to explain the format of the input along with the explantion of the parameter.
        Use the below example as a reference.

        ### Example ###
        -------------------------------
        Problem:
        You have 3 tasks (A, B, C) to be completed by 2 resources (X, Y) within 3 time slots. 
        Each task requires a certain amount of time on each resource, and each resource can work on only one task at a time.

        Code:
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

        *Executor Agent:*

        tasks = List of tasks that needs to be scheduled
        resources = List of resources that are available
        time_requirements = Dictionary of the time requirements to finish a task by using a resource
        total_time_slots = Number of time slots available as an integer

        Please provide your inputs in below JSON format as an example
        {
            "tasks" : ['A', 'B', 'C'],
            "resources" : ['X', 'Y'],
            "time_requirements" : {
                ('A', 'X'): 1, ('A', 'Y'): 2,
                ('B', 'X'): 2, ('B', 'Y'): 1,
                ('C', 'X'): 1, ('C', 'Y'): 1
            },
            "total_time_slots" : 3
        }
        """

    def input_format(self, code: str) -> str:
        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": code,
                },
            ],
        )
        return result.choices[0].message.content
