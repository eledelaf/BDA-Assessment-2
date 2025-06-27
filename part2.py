import pandas as pd
import glob 
import json
from collections import Counter

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
    df.to_csv("combined_data.csv", index = False)
