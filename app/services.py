import time
import logging
from openai import OpenAI
from .extensions import cache

client = OpenAI()

def call_openai_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7,
            )
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
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    response = call_openai_with_retry(messages)
    recipes_text = response.choices[0].message.content.strip()
    recipes = [line.strip() for line in recipes_text.split('\n') if line.strip()]
    return recipes
