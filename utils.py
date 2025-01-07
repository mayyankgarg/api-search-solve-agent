import json
from openai import Client, OpenAI
from decouple import config

client = OpenAI(api_key=config('OPENAI_API_KEY'))

def llm_response(
        user_message: str | list,
        system_message: str = None,
        model_name: str = 'gpt-4o-mini',
        **kwargs
    ):
    
    if isinstance(user_message, str):
        messages = [{"role": "user", "content": user_message}]
    
        if system_message:
            if model_name == 'o1-mini' or model_name == 'o1':
                messages.insert(0, {"role": "developer", "content": system_message})
                if kwargs.get('temperature'):
                    kwargs['temperature'] = 1

            else:
                messages.insert(0, {"role": "system", "content": system_message})        
    else:
        messages = user_message

    # Check if json_mode is set and transform it into response_format
    if kwargs.get('json_mode', False):
        kwargs['response_format'] = {"type": "json_object"}
        del kwargs['json_mode']

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        **kwargs 
    )
    # print(response.choices[0])
    if response.choices[0].finish_reason == 'tool_calls':
        return {
            'tool_called': True,
            'response': response.choices[0].message
        }

    return response.choices[0].message.content