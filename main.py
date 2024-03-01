from agents.planning_agent import Planning_Agent
from agents.coding_agent import Coding_Agent
from agents.executor_agent import Executor_Agent
import chainlit as cl

execute_code = False
problem = None
working_code = None
input_data = None
chainlit_message = None


async def planner(problem: str) -> str:
    planning_agent = Planning_Agent()
    res = planning_agent.run(problem=problem)
    return res


async def coder(problem: str, instructions: str) -> str:
    coding_agent = Coding_Agent()
    coding_agent_prompt = f"""
    {problem}\n
    {instructions}
    """
    code = coding_agent.run(coding_agent_prompt)
    return code


async def input_taker(problem: str, code: str) -> str:
    executor_agent = Executor_Agent()
    executor_agent_prompt = f"""
    {problem}\n
    {code}
    """
    input_format = executor_agent.input_format(executor_agent_prompt)
    return input_format


@cl.step(type="planner")
async def plan_step(problem: str):
    # Simulate a running task
    instructions = await planner(problem)

    return instructions


@cl.step(type="coder")
async def code_step(problem: str, instructions: str):
    # Simulate a running task
    code = await coder(problem, instructions)

    return code


@cl.step(type="executor")
async def input_step(problem: str, code: str):
    # Simulate a running task
    input_format = await input_taker(problem, code)

    return input_format


@cl.on_message
async def main(message: cl.Message):
    # Call the steps
    global execute_code
    global problem
    global working_code
    global chainlit_message
    if not execute_code:
        problem = message.content
        instructions = await plan_step(message.content)
        code = await code_step(message.content, instructions)
        working_code = code
        input_format = await input_step(message.content, code)
        chainlit_message = input_format

        #     problem = """
        #     In the SMU Professor Timetabling problem, we are given a list of courses to be offered, a list of possible time slots, a list of rooms, and a list of professors to teach those courses. Each course needs to be assigned to one professor, in a room, at a timeslot.

        # For simplicity, assume that every course meets once a week at one of the 15 time slots (that is, Mon to Fri 8:30-11:45am, 12:00-3:15pm, and 3:30-6:45pm), and all rooms are identical.

        # The goal is to generate a weekly timetable showing which course is held at which timeslot and room, and taught by which professor. The timetabling constraints are as follows:

        # 1.	Each professor has a set of courses that he or she is eligible to teach (e.g. Prof Amy can teach CS601, CS602, CS603, CS605, …).
        # 2.	Each professor should teach at most 1 course per day.
        # 3.	Each professor has a teaching load (i.e. the number of courses he/she is allocated to).
        # A professor should be assigned no more than and at least 1 less than the teaching load (e.g. if Amy is allocated to 5 courses, the schedule must assign at most 5 but at least 4 courses to her).
        # 4.	Each room may be assigned to at most one course at a time.

        # Notationally, let the decision variables be the timeslot, room and professor assigned to each course:
        # •	T (i.e. T[x] denotes the time slot assigned to course x, for each course x)
        # •	R (i.e. R[x] denotes the room assigned to course x, for each course x)
        # •	P (i.e. P[x] denotes the professor assigned to course x, for each course x)
        #     """
        #     input_format = await input_step(problem, message.content)
        execute_code = True
    else:
        ## Actual code execution
        input_data = message.content
        # call some method with code and input_data as params [TO DO]
        # print("Inside execute code ", input_data)
        chainlit_message = "Docplex code execution is still work in progress!!!!"

    # Send the final answer.
    await cl.Message(content=chainlit_message).send()
