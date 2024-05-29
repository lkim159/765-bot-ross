import os

import imgbbpy
from openai import OpenAI

import sentiment_analysis


# Function to upload image using asynchronous client
async def upload_image_async(image_path):
    img_client = imgbbpy.AsyncClient('d65d28466ce3379f85bf22305662cb0c')
    image_u = await img_client.upload(file=image_path)
    await img_client.close()
    return image_u.url


def summarise_context(context):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )
    question = "Summarise the text provided here, prioritising verbs and nouns as key words, don't worry about forming grammatically correct sentences:" + context

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


# Async so remember to call it using "await"
# It is async because the image needs to be uploaded
# These should only be called once per uploaded image to save time

async def get_description(image_url):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Please describe the art in the provided image in as much detail as possible. Break down the elements into these sections: emotion, style, skill-level, technique, medium, possible influences, color, form, line, shape, space, texture, scale, proportion, unity, variety, rhythm, mass, shape, space, balance, volume, perspective, depth"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    des = response.choices[0].message.content
    return des


# Async so remember to call it using "await"
# It is async because the image needs to be uploaded
# These should only be called once per uploaded image to save time

async def get_critique(image_url):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Please critique the art in the image provided. Format your response into these sections: praise, critcism, constructive feedback, suggested improvements to the whole work, suggested changes to technique, suggested works or artists to be inspired by, reccomended online tutorials, suggested practise exercises, an appropriate challenge for someone of that skill level in art"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=1000,
    )

    des = response.choices[0].message.content
    return des


# Useful helper function to basically google things the bot doesn't know!

def get_more_info(summary, question, image_url):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    limit = str(len(question) * 20)

    # Sentiment analysis. Gets the user sentiment weighted against the three most recent sentiment scores.
    user_sentiment = sentiment_analysis.get_sentiment(question)
    print("User sentiment", user_sentiment)
    neg = str(user_sentiment["neg"])
    neu = str(user_sentiment["neu"])
    pos = str(user_sentiment["pos"])

    question = (
            "With respect to the following context: "
            + summary
            + ". Answer this in only one paragraph "
            + question
            + ". Along with answering the question, consider the current sentiment of my text input in your response; my text input has a negative sentiment of "
            + neg
            + ", a neutral sentiment of "
            + neu
            + " and a positive sentiment of "
            + pos
            + ". Based on this mix of scores, interpret my mood and respond in a way to cheer me up if you feel my overall mood is generally negative."
            + " Keep your response concise. Your reply must be at most "
            + limit
            + " characters long! End your response with a new question for the user based on the context you were provided and their question, presented on a new line"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            },
        ],
        max_tokens=1000,
    )

    des = response.choices[0].message.content
    return des


# Optional function to make plain text generated by chatbot more Bob Ross-y

def bob_rossify(response):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )

    question = "Rephase the following text to sound like Bob Ross without altering its word count by more than 1.5 times:" + response

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


# Fun extra function using DALL-E2 to make art based on inputted image

def make_art(description):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )

    response = client.images.generate(
        model="dall-e-3",
        prompt="Make a drawing based the following prompt in the style of  Bob Ross:" + description,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    des = response.data[0].url
    return des
