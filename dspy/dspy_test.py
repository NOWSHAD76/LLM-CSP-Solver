import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

# Set up the LM
turbo = dspy.OpenAI(model='gpt-3.5-turbo-instruct', max_tokens=250)
dspy.settings.configure(lm=turbo)

# Load math questions from the GSM8K dataset
gms8k = GSM8K()
gsm8k_trainset, gsm8k_devset = gms8k.train[:10], gms8k.dev[:10]