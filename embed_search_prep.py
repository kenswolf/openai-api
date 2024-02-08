"""Playing with Open AI 'embed'."""

import tiktoken
import pandas as pd
from openai import OpenAI

def load_data():
    """ load & inspect dataset """ 
    df_load = pd.read_csv(INPUT_DATAPATH, index_col=0)
    df_load = df_load[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]
    df_load = df_load.dropna()
    df_load["combined"] = (
        "Title: " + df_load.Summary.str.strip() + "; Content: " + df_load.Text.str.strip()
    )
    return df_load


def get_embedding(text, model="text-embedding-3-small"):
    """ get embed vector for provided text """
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def scrub_data(df_scrub):
    """ first cut to first 2k entries, assuming less than half will be filtered out """
    df_scrub = df_scrub.sort_values("Time").tail(TOP_N * 2)

    df_scrub.drop("Time", axis=1, inplace=True)

    encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)

    # omit reviews that are too long to embed
    df_scrub["n_tokens"] = df_scrub.combined.apply(lambda x: len(encoding.encode(x)))
    df_scrub = df_scrub[df_scrub.n_tokens <= MAX_TOKENS].tail(TOP_N)
    print(len(df_scrub))
    print(df_scrub.head(2))
    return df_scrub

##############################

def main():
    """ Controller logic for application"""

    df = load_data()
    df = scrub_data(df)

    # generate embed vector for each entry in data
    # This may take a few minutes
    df["embedding"] = df.combined.apply(lambda x: get_embedding(x, model=EMBEDDED_MODEL))

    df.to_csv("data/fine_food_reviews_with_embeddings_1k.csv")

##############################

EMBEDDED_MODEL = "text-embedding-3-small"
EMBEDDING_ENCODING = "cl100k_base"
MAX_TOKENS = 8000  # the maximum for text-embedding-3-small is 8191
INPUT_DATAPATH = "data/fine_food_reviews_1k.csv"  # to save space, we provide a pre-filtered dataset
TOP_N = 1000 # subsample to 1k most recent reviews and remove samples that are too long

client = OpenAI()

main()

print('done')
