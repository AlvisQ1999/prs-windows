import re

from robot.llm_process import llm_interaction


try:
    result = llm_interaction('What model is using now?')
    print('LLM response:', repr(result))
except Exception as error:
    message = re.sub(r'sk-[A-Za-z0-9_-]+', '<redacted-api-key>', repr(error))
    print('LLM test failed:', type(error).__name__)
    print(message)
    raise
