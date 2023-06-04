"""
See: https://github.com/anthropics/anthropic-sdk-python/tree/main/examples
"""
import anthropic
import os
from dotenv import load_dotenv

def main(max_tokens_to_sample: int = 200):
    anth = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
    prompt = open('prompt.txt').read()
    print(prompt)
    confirm = input('>> Enter "y" to continue, with the above prompt: ')
    if confirm != 'y':
        return
    response = anth.completion_stream(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
        stop_sequences=[anthropic.HUMAN_PROMPT],
        max_tokens_to_sample=max_tokens_to_sample,
        model="claude-v1",
        stream=True,
    )
    for data in response:
        print(data['completion'])


if __name__ == "__main__":
    load_dotenv()
    main()
