import pandas as pd
import spark 

# Import the data frame
df = pd.read_csv("combined_data.csv")
print(df.head())

# 3.1: Descriptive Statistics
# 1. What is the average duration (in seconds) of all videos in the dataset?
mean_pd = df["duration_seconds"].mean(axis=1)
mean_spark = 0

# 2. Which uploader appears most frequently in the dataset?

# 3. Which five videos have the highest number of views? List their titles and view counts.

# 4. For each upload year, what is the average number of likes?

# 5. How many videos are missing artist information?

# 3.2: Tag and Content Characteristics