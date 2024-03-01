# LLM-CSP-Solver
Using LLM to solve CSP

### How to run
1. Create a .env file in the root directory with your OPENAI_API_KEY like shown below
    ```
    OPENAI_API_KEY=XXXX
    ```
2. Create a conda or virtual environment if required and run below commands
    ```
    pip install -r requirements.txt
    chainlit run main.py -w
    ```