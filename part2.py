import pandas as pd
import glob 
import json
from collections import Counter

if __name__ == "__main__":
    
    # Read the .json metadata from the audio_output directory 
    with open("/Users/elenadelafuente/Desktop/MASTER/2 trimestre/Big Data/Assesments/BDA Capstone project/audio_output/Daft Punk - Giorgio By Moroder.json") as file:
        data = json.load(file)
    
    print(data)