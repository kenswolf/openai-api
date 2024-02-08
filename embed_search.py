""" This is a search based on embed vectors """

from ast import literal_eval
import pandas as pd
import numpy as np

from openai import OpenAI

def get_knowledge_base():
    """Retreives the knowledge base data.  It has already
    been converted to embed vectors.  Additionally it
    transforms the vectors (ie values in the embedding 
    column) from strings (e.g. "[1,2,3]") to lists (e.g. [1,2,3])
    to numpy arrays (e.g. [1,2,3]) """
    df_l = pd.read_csv(DATAFILE_PATH)
    df_l["embedding"] = df_l.embedding.apply(literal_eval).apply(np.array)
    return df_l

def get_embedding(text, model="text-embedding-3-small"):
    """ Determines embedding of target search string so it can
    be compared to stored embeddings of knowledge base content"""
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    """ cosine similarity is a measure of similarity between 
    two non-zero vectors defined in an inner product space. 
    Cosine similarity is the cosine of the angle between the
    vectors; that is, it is the dot product of the vectors 
    divided by the product of their lengths. It follows that 
    the cosine similarity does not depend on the magnitudes 
    of the vectors, but only on their angle. 
    per  https://en.wikipedia.org/wiki/Cosine_similarity """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# search through the reviews for search_text
def search_reviews(dfr, search_text, n=3, pprint=True):
    """ desc of what this does"""

    product_embedding = get_embedding(
        search_text,
        model="text-embedding-3-small"
    )

    dfr["similarity"] = dfr.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        dfr.sort_values("similarity", ascending=False)
        .head(n)
        .combined.str.replace("Title: ", "")
        .str.replace("; Content:", ": ")
    )
    if pprint:
        for r in results:
            print(r[:400])
            print()
    return results

##############################

def main():

    """ Controller logic for application"""

    df = get_knowledge_base()

    search_text = "delicious beans"
    search_reviews(df, search_text, n=3)

    print('-------')

    search_text = "whole wheat pasta"
    search_reviews(df, search_text, n=3)

##############################

DATAFILE_PATH = "data/fine_food_reviews_with_embeddings_1k.csv"

client = OpenAI()

main()
