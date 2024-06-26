from openai import OpenAI
from dotenv import load_dotenv
import re
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import os, sys
import pathlib
import subprocess
import pickle

load_dotenv()  # take environment variables from .env.
WORKING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "extensions")
WIN32 = sys.platform == "win32"
PATH_SEPARATOR = WIN32 and "\\" or "/"


class Executor_Agent:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.history = []
        self.system_prompt = """
        ### Role ###
        You are a Executor agent python developer who excels at understanding python code and logs analyzing for solving mainly 
        Constraint Programming tasks using docplex python package.

        ### Instruction ###
        Based on the given problem and code you have to provide example on how the data should be stored in the pickle file
        that is going to be used as a parameter to the python file while execution.Give appropriate example to explain the 
        format of the input along with the explantion of the parameter.
        Use the below example as a reference.

        ### Example ###
        -------------------------------
        Problem:
        You have 3 tasks (A, B, C) to be completed by 2 resources (X, Y) within 3 time slots. 
        Each task requires a certain amount of time on each resource, and each resource can work on only one task at a time.

        Code:
        python
        ```
        import sys
        import pickle
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
                print("No Solution found)

        if __name__=="__main__":
            with open(sys.argv[1], 'r') as f:
                data = pickle.load(f)
            solve_scheduling_problem(data["tasks"], data["resources"], data["time_requirements"], data["total_time_slots"])
        ```

        *Executor Agent:*

        tasks = List of tasks that needs to be scheduled
        resources = List of resources that are available
        time_requirements = Dictionary of the time requirements to finish a task by using a resource
        total_time_slots = Number of time slots available as an integer

        Please provide your inputs with the above details in pickle file format.
        """

    def input_format(self, code: str) -> str:
        """
        Analyze the code and prompt the user to give input data in a specific format.
        """
        system_msg = {"role": "system", "content": self.system_prompt}
        usr_msg = {"role": "user", "content": code}
        self.history.append(system_msg)
        self.history.append(usr_msg)
        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )
        message_answer = {
            "role": "assistant",
            "content": result.choices[0].message.content,
        }
        self.history.append(message_answer)
        return result.choices[0].message.content

    def execute_code(self, code: str, input_data_path: str, file_name=None):
        """
        Extract the code from the LLM response and execute it for the input provided
        by the user.
        """
        code_pattern = re.compile(r"```([^`]+)```")
        code_blocks = code_pattern.findall(code.replace("python", ""))
        print("Code blocks ", code_blocks)
        # Extract the individual code blocks and languages from the matched groups
        extracted_code = []
        extracted_code = code_blocks[-1]
        print(extracted_code)
        if file_name is None:
            code_hash = md5(code.encode()).hexdigest()
            # create a file with a automatically generated name
            file_name = f"tmp_code_{code_hash}.py"
        original_filename = file_name
        file_path = os.path.join(WORKING_DIR, file_name)
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as fout:
            fout.write(extracted_code)
        cmd = [
            sys.executable,
            f".\\{file_name}" if WIN32 else file_name,
            input_data_path,
        ]
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                subprocess.run,
                cmd,
                cwd=WORKING_DIR,
                capture_output=True,
                text=True,
            )
            try:
                result = future.result()
            except Exception as e:
                print("There is a error while running the code", e)
        if original_filename is None:
            os.remove(file_path)
        if result.returncode:
            logs = result.stderr
            if original_filename is None:
                abs_path = str(pathlib.Path(file_path).absolute())
                logs = logs.replace(str(abs_path), "").replace(file_name, "")
            else:
                abs_path = str(pathlib.Path(WORKING_DIR).absolute()) + PATH_SEPARATOR
                logs = logs.replace(str(abs_path), "")
        else:
            logs = result.stdout
        return result.returncode, logs

    def read_data(self, file_path: str) -> str:
        """
        Reads the user data and returns as a string for coding agent's reference
        """
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        return str(data)

    def logs_analyzer(self, logs: str):
        """
        Analyze the logs and provide the specific error for querying the documentation
        """
        prompt = f"""
        Analyze the below error logs and give me the exact error like AttributeError, TypeError etc
        excluding the line number, file name etc as shown in the below example

        ### Example ###
        Logs:
        'Traceback (most recent call last):\n  File "tmp_code_64f7cb4eb273266054c292edab2b00ae.py", line 49, in <module>   
        solve_sudoku(data)\n  File "tmp_code_64f7cb4eb273266054c292edab2b00ae.py", line 15, in solve_sudoku\n    
        model.add_constraint(model.all_distinct(X[i, j] for j in range(9)))
        AttributeError: \'CpoModel\' object has no attribute \'all_distinct\'\n'

        Answer:
        AttributeError: CpoModel object has no attribute all_distinct

        Your turn:
        {logs}
        
        Answer:
        """
        usr_msg = {"role": "user", "content": prompt}
        self.history.append(usr_msg)
        result = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )
        message_answer = {
            "role": "assistant",
            "content": result.choices[0].message.content,
        }
        self.history.append(message_answer)
        return result.choices[0].message.content
