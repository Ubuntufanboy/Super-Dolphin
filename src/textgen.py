import os
import google.generativeai as genai

# Access your API key as an environment variable.
with open("secrets.txt") as f:
    key = f.read()
    key = key.replace("\n", "")
genai.configure(api_key=key) # TODO: use env instead
# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = "Please generate 10 calculus questions in this format Question: <the-actual-question> Answer: <the-actual-answer>. Do not provide explainations for the questions or any text that is not the questions and answers."
response = model.generate_content(prompt)

print(response.text)
os.system("rm response.txt") # Only works on UNIX systems
with open("response.txt") as f:
    f.write(response.txt)
