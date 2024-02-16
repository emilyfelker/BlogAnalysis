import re
import os
import hashlib
from datetime import datetime
from time import sleep
from dotenv import load_dotenv
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)
from typing import List, Dict, Union, Any, Tuple
from BlogAnalysis.data import get_database, get_response_from_database, add_to_database


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


# Look up hash of postbody and prompt in database
def get_gpt(postbody: str, promptkey: str, model="gpt-3.5-turbo") -> str:
    conn = get_database()
    response = get_response_from_database(conn, calculate_md5(postbody, promptkey), model)
    if response is not None:  # i.e., response was already present in database
        return response
    else:
        print("getting from api")
        response = get_gpt_from_api(postbody, promptkey, model)  # need to make API call
        return response


@retry(wait=wait_fixed(60), stop=stop_after_attempt(1))
def get_gpt_from_api(postbody: str, promptkey: str, model="gpt-3.5-turbo") -> str:

    sleep(20.1)  # to deal with rate-limit of 3 requests per minute

    # make API call
    response = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": prompts[promptkey]},
            {"role": "user",
             "content": postbody},
        ],
        model=model,
        temperature=0,
    )
    # save response from API call
    response_to_save = response.choices[0].message.content

    # save response to database
    conn = get_database()
    add_to_database(conn, calculate_md5(postbody, promptkey), model, response_to_save)

    return response_to_save


def calculate_md5(postbody: str, promptkey: str) -> str:
    combined_string = ''.join([postbody, prompts[promptkey]])
    md5_hash = hashlib.md5(combined_string.encode()).hexdigest()
    return md5_hash


def make_features(post: Tuple[str, datetime, str]) -> Dict[str, Any]:
    title, date, body = post
    features = {
        "word_count": len(body.split()),
        "day_of_week": date.strftime("%A"),
        "age_of_emily": (date - datetime(1991, 1, 9).date()).days / 365.25,  # close enough
        "topic": get_gpt(body, "topic"),
        "age_estimate": extract_numeral(get_gpt(body, "age"))
    }
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


def show_summaries(dataset_with_features):
    for blogpost in dataset_with_features:
        title, date, content, features = blogpost
        print(features["topic"])
