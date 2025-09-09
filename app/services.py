import time
import logging
from google import genai
from .extensions import cache

client = genai.Client()

def call_openai_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=messages
            )

            return response.text
        except Exception as e:
            logging.warning(f"OpenAI API error: {e}, attempt {attempt + 1} of {max_retries}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)

def build_prompt(ingredients, diet, cuisine):
    prompt = f"Suggest 3 simple recipes with these ingredients: {ingredients.strip().lower()}."
    if diet:
        prompt += f" The recipes should be {diet.strip().lower()}."
    if cuisine:
        prompt += f" The recipes should be from {cuisine.strip().lower()} cuisine."
    return prompt

@cache.memoize(timeout=3600)  # Caches for 1 hour
def get_openai_recipes(ingredients, diet, cuisine):
    prompt = build_prompt(ingredients, diet, cuisine)
    response = call_openai_with_retry(prompt)
    return response
