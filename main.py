# from agents.planning_agent import Planning_Agent
from agents.planning_agent_gemini import Planning_Agent
from agents.coding_agent import Coding_Agent
from agents.coding_agent_claude import Coding_Agent_Claude
from agents.executor_agent import Executor_Agent
import chainlit as cl
from chroma.chroma import get_relevant_doc, get_chroma_collection

execute_code = False
problem = None
working_code = None
input_data = None
chainlit_message = None
code_retry_count = 1
executor_agent = Executor_Agent()
# coding_agent = Coding_Agent()
coding_agent = Coding_Agent_Claude()


async def planner(problem: str) -> str:
    planning_agent = Planning_Agent()
    res = planning_agent.run(problem=problem)
    return res


async def coder(problem: str, instructions: str) -> str:
    global coding_agent
    coding_agent_prompt = f"""
    {problem}\n
    {instructions}
    """
    code = coding_agent.run(coding_agent_prompt)
    return code


async def input_taker(problem: str, code: str):
    global executor_agent
    executor_agent_prompt = f"""
    {problem}\n
    {code}
    """
    input_format = executor_agent.input_format(executor_agent_prompt)
    return input_format


@cl.step(type="code execution")
async def code_executor(code: str, data_path: str):
    global executor_agent
    return_code, logs = executor_agent.execute_code(code, data_path)
    return return_code, logs


@cl.step(type="code fixing")
async def code_fixing(code: str, error: str, data: str):
    global coding_agent
    global working_code
    docs = await doc_lookup(error)
    code_fix = coding_agent.fix_code(code, error, data, docs)
    working_code = code_fix
    return code_fix


@cl.step(type="planner")
async def plan_step(problem: str):
    instructions = await planner(problem)

    return instructions


@cl.step(type="coder")
async def code_step(problem: str, instructions: str):
    code = await coder(problem, instructions)

    return code


@cl.step(type="executor")
async def input_step(problem: str, code: str):
    input_format = await input_taker(problem, code)

    return input_format


@cl.step(type="documentation_lookup")
async def doc_lookup(logs: str):
    global executor_agent
    exact_error = executor_agent.logs_analyzer(logs)
    collection = get_chroma_collection("docplex_documentation")
    relavant_doc = get_relevant_doc(collection, exact_error, 2)
    return relavant_doc


@cl.on_message
async def main(message: cl.Message):
    # Call the steps
    global execute_code
    global problem
    global working_code
    global chainlit_message
    global executor_agent
    global code_retry_count
    if not execute_code:
        problem = message.content
        instructions = await plan_step(message.content)
        code = await code_step(message.content, instructions)
        working_code = code
        input_format = await input_step(message.content, code)
        chainlit_message = input_format
        execute_code = True
    else:
        files = None
        # Wait for the user to upload a file
        while files == None:
            files = await cl.AskFileMessage(
                content="Please upload the pickle file to run the code!",
                accept=["pk"],
            ).send()
        pickle_file = files[0]
        return_code, logs = await code_executor(working_code, pickle_file.path)
        if return_code != 0:
            input_data = executor_agent.read_data(pickle_file.path)

        while return_code != 0 and code_retry_count <= 3:
            code_fix = await code_fixing(working_code, logs, input_data)
            return_code, logs = await code_executor(code_fix, pickle_file.path)
            code_retry_count += 1
            print("Code count ", code_retry_count)

        chainlit_message = logs
        print("Resetting the values")
        execute_code = False
        code_retry_count = 1

    # Send the final answer.
    await cl.Message(content=chainlit_message).send()
