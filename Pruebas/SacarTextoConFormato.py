from pydantic import BaseModel

from ollama import chat


# Define the schema for the response
class FriendInfo(BaseModel):
  name: str
  age: int


class FriendList(BaseModel):
  friends: list[FriendInfo]


# schema =  'required': ['friends']}
response = chat(
  model='deepseek-r1:1.5b',
  messages=[{'role': 'user', 'content': ''}],
  format=FriendList.model_json_schema(),  # Use Pydantic to generate the schema or format=schema
  options={'temperature': 0},  # Make responses more deterministic
  
)

# Use Pydantic to validate the response
friends_response = FriendList.model_validate_json(response.message.content)
print(friends_response)