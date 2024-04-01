# LLM-CSP-Solver
Using LLM to solve CSP

### Introduction & Motivations
In numerous industries, particularly within Small to Medium Enterprises (SMEs), the challenge of effectively addressing complex Constraint Satisfaction Problems (CSP) or Planning tasks is prevalent. SMEs often lack the resources to hire specialized data science professionals or invest in expensive solver tools, leading to inefficiencies in operations and compromised competitiveness. The emergence of Large Language Models (LLMs) offers a promising solution by democratizing access to specialized knowledge and code generation capabilities.

### Project Objectives
The primary objective of this project is to develop an industry-agnostic solution for constraint planning that can be easily decoded and executed by non-technical users. Unlike traditional approaches that require specialized expertise or tailored solutions for specific problems, this project leverages LLMs to generate code segments and plans across various domains. By providing a user-friendly interface, even individuals with minimal coding or planning experience can utilize the solution effectively, enhancing operational efficiency and competitiveness across diverse sectors.

### System Architecture

![System Architecture](https://github.com/NOWSHAD76/LLM-CSP-Solver/assets/37472101/2f2d4b97-9620-4648-a74a-094c86769782)

### How to run
1. Create a .env file in the root directory with your OPENAI_API_KEY like shown below
    ```
    OPENAI_API_KEY=XXXX
    ANTHROPIC_API_KEY=XXXX
    GOOGLE_API_KEY=XXX
    ```
2. Create a conda or virtual environment if required and run below commands. Do not add -w at the end as it refreshes the page whenever a new code is generated
    ```
    pip install -r requirements.txt
    python chroma/chroma.py # To create chroma collections
    chainlit run main.py
    ```

### Evaluation
| Problem difficulty  | Problem Examples | Ability to Solve | Reliability |
| ------------- |-------------|-------------|-------------|
| Easy      | Sudoku     | Yes | High |
| Easy      | Map Coloring     | Yes | High |
| Easy      | N-Queens     | Yes | High |
| Medium      | Exam Scheduling     | Yes | High |
| Medium      | Job Scheduling     | Yes | High |
| Medium      | Project Management Plan (Hard Constraints)     | Yes | High |
| Medium      | Project Management Plan (Soft Constraints)     | No | - |
| Hard      | Time table scheduling (complex constraints)     | No | - |

#### Acknowledgements
This project was developed as a part of the CS 606 AI Planning and Decision Making module offered by the Singapore Management University (SMU) under the MITB coursework.

Professor : [LAU Hoong Chuin](https://faculty.smu.edu.sg/profile/lau-hoong-chuin-631)

Group members :
* [Nowshad Shaik](https://www.linkedin.com/in/nowshadshaik/)
* [Nayan Rokhade](https://www.linkedin.com/in/nayan-rokhade/)
* [Derek Cho](https://www.linkedin.com/in/derek-cho-3a6100b8/)
* [Ming Bing Ng](https://www.linkedin.com/in/ming-bing-ng/)

#### References
* AhmadiTeshnizi, A., Gao, W., & Udell, M. (2024, Feb 15). OptiMUS: Scalable Optimization Modeling with (MI)LP Solvers and Large Language Models. Retrieved from arxiv.org: https://arxiv.org/pdf/2402.10172.pdf
* Chan Hee Song, Wu, J., Washington, C., Sadler, B. M., Chao, W., & Sui, Y. (2022). LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models. ArXiv (Cornell University). https://doi.org/10.48550/arxiv.2212.04088
