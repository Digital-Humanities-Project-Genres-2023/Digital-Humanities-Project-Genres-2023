"""
Functions to read in and deal with files which are located in Puhti genre project folder.
"""

import pandas as pd
import json

def readme():
    "Prints the included readme. Also returns readme if needed."
    
    with open("/scratch/project_2007227/genre_data/readme.txt", "r") as f:
        readme = f.read()
        print(readme)
        
    return readme

def labels_to_dict():
    "Read label mapping to a dictionary"
    
    with open("/scratch/project_2007227/genre_data/labels_set.json", "r") as f:
        labels = json.load(f)
    
    return labels


def read_text_file(document_id):
    "Read in book text based on document id"
    
    #Not sure if folder "ecco_subset" is needed for anything
    
    # Construct the path to the .txt file based on the document_id
    file_path = '/scratch/project_2007227/genre_data/ecco_source/' + document_id + '.txt'

    # Read the contents of the .txt file into a string
    with open(file_path, 'r') as file:
        file_contents = file.read()
        
    return file_contents

def genre_data_to_pandas(data="dev"):
    "Read the genre data with book ids to pandas. Either dev, test or train."
    
    dtypes = {
        "document_id": str,
        "work_id": str,
        "main_category": int,
        "sub_category":int
    }
    
    df = pd.read_csv(
        f"/scratch/project_2007227/genre_data/{data}.csv",
        sep=",",
        dtype=dtypes
    )
    
    print(f"Read in dataset {data}.csv. Set param 'data' to 'dev', 'test' or 'train' if you want another dataset.")
    
    return df

def ecco_metadata_to_pandas():
    "Read ecco metadata to pandas"
    
    dtypes = {
        "document_id_octavo": str,
        "publication_year": str, #Could be int but doesn't support N/A values
        "gatherings": str,
        "total_price": float,
        "publication_place": str,
        "author_id": str,
        "other_actors": str
    }
    
    df = pd.read_csv(
        "/scratch/project_2007227/genre_data/ecco_metadata.tsv",
        sep="\t",
        dtype=dtypes
    )
    
    return df