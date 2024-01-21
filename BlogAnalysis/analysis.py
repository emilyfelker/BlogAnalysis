# To do:
# see if chatGPT can write a decent test for data extraction
# can chatGPT detect the presence/absence of certain themes or emotions or tones/moods in posts over time?
# subject matter / themes / topics
# next project: provide a summary/retelling of my life story by month or by year
# then can it write the story of my future? (or rewrite the story of certain years: what if...) predict my job, etc.?
# what can it determine about my personality traits?
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from typing import List, Dict, Union, Any, Tuple

load_dotenv()
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    timeout=6,
)

prompts = {
    "topic": "Your only job is to summarize the topic of the user's message in NO MORE THAN five words",
    "age": "Your only job is to give your best estimate of the age of the writer of the text. "
           "Give JUST the numeral of your estimate, nothing more."
}


def extract_numeral(input_string: str) -> Union[float, None]:
    numerals = re.findall(r'\d+', input_string)
    if not numerals:
        return None
    numerals = [int(num) for num in numerals]
    average = sum(numerals) / len(numerals)
    return average


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def get_gpt(postbody: str, promptkey: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": prompts[promptkey]},
            {"role": "user",
             "content": postbody},
        ],
        model="gpt-3.5-turbo",
        temperature=0,
    )
    return response.choices[0].message.content


def make_features(post: Tuple[str, datetime, str]) -> Dict[str, Any]:
    title, date, body = post
    features = {
        "word_count": len(body.split()),
        "day_of_week": date.strftime("%A"),
        "age_of_emily": (date - datetime(1991, 1, 9).date()).days / 365.25,  # close enough
        "topic": get_gpt(body, "topic"),
        "age_estimate": extract_numeral(get_gpt(body, "age"))
    }
    print(features)
    return features


def add_features_to_dataset(dataset: List[Tuple[str, datetime, str]]):
    dataset_with_features = []
    for post in dataset:
        features = make_features(post)
        post_with_features = (*post, features)
        dataset_with_features.append(post_with_features)
    return dataset_with_features


def preview_features(dataset_with_features: List[Tuple[str, datetime, str, Dict[str, Any]]]) -> None:
    for blogpost in dataset_with_features:
        title, date, content, features = blogpost
        print(f"Title: {title} | Date: {date}")
        print(f"Content: {content[:80].lstrip()}...")
        print("Features:")
        for feature, value in features.items():
            print(f"  {feature}: {value}")
        print()
