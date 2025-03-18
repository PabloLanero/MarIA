from ollama import chat

messages = [
  {
    'role': 'user',
    'content': '',
  },
  {
    'role': 'assistant',
    'content': "",
  },
]

while True:
  user_input = input('Chat with history: ')
  response = chat(
    'deepseek-r1:1.5b',
    messages=messages
    + [
      {'role': 'user', 'content': user_input},
    ],
  )

  # Add the response to the messages to maintain the history
  messages += [
    {'role': 'user', 'content': user_input},
    {'role': 'assistant', 'content': response.message.content},
  ]
  print(response.message.content + '\n')