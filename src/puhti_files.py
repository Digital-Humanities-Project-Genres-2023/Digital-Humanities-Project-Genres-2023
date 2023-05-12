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

def labels_to_dict(invert=False):
    "Read label mapping to a dictionary"
    
    with open("/scratch/project_2007227/genre_data/labels_set.json", "r") as f:
        labels = json.load(f)
    
    if invert:
        labels['main2id'] = {value: key for key, value in labels['main2id'].items()}
        labels['sub2id'] = {value: key for key, value in labels['sub2id'].items()}
    
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

def labels_to_genre_data(df, better_subcat_names=False):
    "English labels to dataframe genre data"
    
    labels = labels_to_dict(invert=True)
    if better_subcat_names:
        sub_cat_names = sub_categories_better_names()
        labels["sub2id"] = {key: sub_cat_names[value] for key, value in labels["sub2id"].items()}
    
    
    df["main_category_label"] = df["main_category"].apply(lambda x: labels["main2id"][x])
    df["sub_category_label"] = df["sub_category"].apply(lambda x: labels["sub2id"][x])
    
    return df

def genre_data_to_pandas(data="dev", add_labels=False, merge_ecco=False, better_subcat_names=False):
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
    
    if add_labels:
        df = labels_to_genre_data(df, better_subcat_names)
        
    if merge_ecco:
        df = merge_ecco_metadata(df)
    
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

def merge_ecco_metadata(df):
    "Merges ecco metadata to genre dataset. Results in some documents having multiple rows."
    
    ecco_metadata = ecco_metadata_to_pandas()
    df = df.merge(ecco_metadata, left_on='document_id', right_on='document_id_octavo', how='left')
    df.drop('document_id_octavo', axis=1, inplace=True)
    
    return df

def sub_categories_better_names():
    """
    Returns mapping for better sub category names.
    Follows naming from 'Detecting Sequential...' paper.
    """
    
    sub_cat_map = {
        'artstheatreplaysopera': "Theatre, plays, opera",
        'artsmusichymnssongsetc': "Music, hymns, songs",
        'artsfineartandaesthetics': "Fine Arts and Aesthetics",
        
        'scientificimprovementlanguages': "Languages",
        'scientificimprovementgeographycartographyastronomyandnavigation': "Geography, cartography, astronomy and navigation",
        'scientificimprovementnaturalphilosophy': "Natural philosophy",
        'scientificimprovementmedicineandanatomy': "Medicine and anatomy",
        'scientificimprovementagricultureanimalhusbandry': "Agriculture and animal husbandry",
        'scientificimprovementpracticaltradesmechanicsengineering': "Practical trades, mechanics, engineering",
        'scientificimprovementnaturalhistory': "Natural history",
        'scientificimprovementeconomyandtrade': "Economics and trade",
        'scientificimprovementmathematics': "Mathematics",
        
        'politicspoliticalessaysplans': "Political essays",
        'politicsintelligence': "Intelligence",
        'politicsparliamentaryspeeches': "Parliamentary speeches",
        
        'historygeneral': "General History",
        'historybiographicalhistory': "Biographical History",
        
        'literaturedrama': "Drama",
        'literaturepoetry': "Poetry",
        'literatureotherfiction': "Other fiction",
        'literaturetravel': "Travel",
        'literatureperiodicals': "Periodicals",
        'literaturecollectedworks': "Collected Works",
        'literaturenovels': "Novels",
        'literaturecriticism': "Critisism",
        'literatureclassics': "Classics",
        
        'religionsermons': "Sermons",
        'religiontheology': "Theology",
        
        'lawacts': "Acts, proclamations",
        'lawtrialaccounts': "Trial accounts",
        'lawcollectionsbills': "Collected bills",
        'lawessays': "Legal essays",
        'lawappeals': "Appeals",
        'lawproclamations': "Proclamations",
        
        'educationgeneral': "General Education",
        'educationadviceliterature': "Advice literature",
        'educationinstructionalbooks': "Instructional books",
        'educationhobbiesgames': "Hobbies & Games",
        'educationrecipebooks': "Recipe Books",
        
        'salecataloguesalmanacsdirectoriesetc': "Sales catalogues, almanacs, directories etcetera",
        
        'philosophymoralphilosophy': "Moral Philosophy",
        'philosophypoliticalphilosophy': "Political philosophy",
        'philosophyhumanunderstandinglogicmetaphysicsetc': "Human understanding, metaphysics",
    }
    
    return sub_cat_map
    
    
    
    
