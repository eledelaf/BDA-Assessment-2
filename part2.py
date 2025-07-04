import pandas as pd
import glob 
import json
from collections import Counter
import spark 

if __name__ == "__main__":
    PATH = "/Users/elenadelafuente/Desktop/MASTER/2 trimestre/Big Data/Assesments/BDA Capstone project/audio_output"
    # This code is on the assessment codebook 
    json_files = glob.glob("/Users/elenadelafuente/Desktop/MASTER/2 trimestre/Big Data/Assesments/BDA Capstone project/audio_output/*.json")

    # Read the .json metadata from the audio_output directory 
    df = pd.DataFrame()

    for file in json_files:
        with open(file, "r", encoding="utf-8") as file:
            data = json.load(file)
            records = data if isinstance(data, list) else [data]
            df = pd.concat([df, pd.DataFrame(records)], ignore_index=True)
    
    print(df.head())

    # Extract the needed fields:
    l_fields = ["id", "title", "uploader", "artist", "tags", 
                "duration_seconds", "upload_date", "view_count", 
                "like_count", "year_uploaded", "tag_count"]
    df = df[l_fields]
    print(df.head())
    #print(df.shape)
    #print(df["title"])
    df.to_csv("combined_data.csv", index = False, sep = ';')
