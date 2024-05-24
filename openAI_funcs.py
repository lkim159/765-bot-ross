import os
from openai import OpenAI
from pathlib import Path
import openai
import asyncio
import imgbbpy


###Async so remember to call it using "await"
###It is async because the image needs to be uploaded
###These should only be called once per uploaded image to save time

async def get_description(image_path):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    
    img_client = imgbbpy.AsyncClient('d65d28466ce3379f85bf22305662cb0c')
    image_u = await img_client.upload(file=image_path)
    image = image_u.url
    await img_client.close()

    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Please describe the art in the provided image in as much detail as possible. Inject into your response a bit of the way Artist Bob Ross might speak, use variations on his figures of speech and tone, but not too much! Don't mention you are doing a Bob Ross impression! Break down the elements into these sections: emotion, style, skill-level, technique, medium, possible influences, color, form, line, shape, space, texture, scale, proportion, unity, variety, rhythm, mass, shape, space, balance, volume, perspective, depth"},
            {
              "type": "image_url",
              "image_url": {
                "url": image,
              },
            },
          ],
        }
      ],
      max_tokens=1000,
    )
    
    des = response.choices[0].message.content
    return des  

###Async so remember to call it using "await"
###It is async because the image needs to be uploaded
###These should only be called once per uploaded image to save time

async def get_critique(image_path):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    
    img_client = imgbbpy.AsyncClient('d65d28466ce3379f85bf22305662cb0c')
    image_u = await img_client.upload(file=image_path)
    image = image_u.url
    await img_client.close()

    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Please critique the art in the image provided. Inject into your response a bit of the way Artist Bob Ross might speak, use variations on his figures of speech and tone, but not too much! Don't mention you are doing a Bob Ross impression! Format your response into these sections: praise, critcism, constructive feedback, suggested improvements to the whole work, suggested changes to technique, suggested works or artists to be inspired by, reccomended online tutorials, suggested practise exercises, an appropriate challenge for someone of that skill level in art"},
            {
              "type": "image_url",
              "image_url": {
                "url": image,
              },
            },
          ],
        }
      ],
      max_tokens=1000,
    )
    
    des = response.choices[0].message.content
    return des

###Useful helper function to basically google things the bot doesn't know!

def get_more_info(question):
    print ("Called", )
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    
    question = question + " Inject into your response a bit of the way Artist Bob Ross might speak, use variations on his figures of speech and tone, but not too much! Don't mention you are doing a Bob Ross impression!"

    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": question},
          ],
        }
      ],
      max_tokens=1000,
    )
    
    des = response.choices[0].message.content
    return des 

###Optional function to make plain text generated by chatbot more Bob Ross-y

def bob_rossify(response):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    
    question = "Rephase this text:" + response + " If it is a question do not answer it. Rephrase this text by injecting a bit of the way Artist Bob Ross might speak, use variations on his figures of speech and tone, but not too much! Don't mention you are doing a Bob Ross impression!"

    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": question},
          ],
        }
      ],
      max_tokens=1000,
    )
    
    des = response.choices[0].message.content
    return des

###Fun extra function using DALL-E2 to make art based on inputted image

def make_art(description):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

    response = client.images.generate(
      model="dall-e-3",
      prompt="Make a drawing based on the description of the following prompt in the style of Artist Bob Ross:" + description,
      size="1024x1024",
      quality="standard",
      n=1,
    )
        
    des = response.data[0].url
    return des 
    
def testing_func(user_input):
  return f'Yes {user_input}'
