import anthropic
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class Coding_Agent_Claude:
    def __init__(self) -> None:
        self.client = anthropic.Anthropic()
        self.history = []
        self.system_prompt = """
        ### Role ###
        You are a Coding Agent python developer who excels at solving Constraint Programming tasks using docplex python package.
        Think step by step carefully before writing the code.

        ### Instruction ###
        Based on the user problem statement and mathematical instructions provided you have to write the python code
        using docplex package to solve the problem as shown in the below example.
        Build the python code which is written to a file later on and the data is given to the python file as a parameter.
        The code should be able to read the pickle data file and has to print the solution at the end.

        ### Note ###
        Note that your response should only contain python code without any explanation or run command is needed.
        You can try to use global constraints like all_diff(), no_overlap() etc

        ### Example ###
        -------------------------------
        """

    def run(self, instruction: str, example: str) -> str:
        """
        Generate the docplex code based on the planning agents response
        """
        prompt = f"""
        {self.system_prompt}
        {example}

        Question:
        {instruction}

        Note: Double check your code for syntax errors before responding.
        """
        self.history.append({"role": "user", "content": prompt})
        result = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=self.history,
        )
        self.history.append({"role": "assistant", "content": result.content[0].text})
        return result.content[0].text

    def fix_code(self, code: str, error: str, data: str, docs: str) -> str:
        """
        Fixing the code based on the error, data and documentation reference
        """
        prompt = f"""
        ### Code ###
        {code}

        The above code is throwing the below error while executing.
        ### Error ###
        {error}

        The data provided by the user is below
        
        {data}

        Below is the python docplex library documentation which you can use to fix the above error
        {docs}

        Based on the above error, data provided by the user and documentation,rewrite the code to fix the issue and 
        return the entire python code.
        Think step by step carefully before writing the code to avoid the same mistake.
        """
        self.history.append({"role": "user", "content": prompt})
        result = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=self.history,
        )
        self.history.append({"role": "assistant", "content": result.content[0].text})
        return result.content[0].text
