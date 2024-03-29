import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
genai.configure()


class Planning_Agent:
    def __init__(self) -> None:
        self.client = genai.GenerativeModel("gemini-pro")
        self.system_prompt = """
        ### Role ###
        You are a planning agent who excels at performing Constraint Programming tasks.
        Think step by step carefully before answering the problem.
        Try to use global constraints like all_diff(), no_overlap() etc while planning.

        ### Instruction ###
        Based on the user problem statement you have come up with the Decision variables, Domains,
        Mathematical representation of Constraints and reasoning behind it as shown in the below example.

        ### Example ###
        -------------------------------
"""

    def run(self, problem: str, example: str) -> str:
        """
        Converting the user given natural language problem to a CSP formulation.
        """

        prompt = f"""
        {self.system_prompt}
        {example}

        Your turn
        ### Problem ###
        {problem}
        """
        result = self.client.generate_content(prompt)

        return result.text
