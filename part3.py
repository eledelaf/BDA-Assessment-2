import pandas as pd
import spark 

# Import the data frame
df = pd.read_csv("combined_data.csv")
print(df.head())

## 3.1: Descriptive Statistics
# 1. What is the average duration (in seconds) of all videos in the dataset?
mean_pd = df[["duration_seconds"]].mean()
print(f"The mean in seconds of the durations of the videos is: {round(mean_pd["duration_seconds"], 2)}")
mean_spark = 0

# 2. Which uploader appears most frequently in the dataset?
mode_pd = df["uploader"].mode()
print(f"The most popular uploader is: {mode_pd[0]}")

# 3. Which five videos have the highest number of views? List their titles and view counts.
top_5_pd = df.sort_values(by =["view_count"]).head(5)
print(top_5_pd[["title","view_count"]])

# 4. For each upload year, what is the average number of likes?
df_year_likes = df[["year_uploaded", "like_count"]]
df_year_likes = df_year_likes.groupby(["year_uploaded"]).mean()
print(df_year_likes)

# 5. How many videos are missing artist information?
is_null = df["artist"].isna().sum()
print(is_null)

## 3.2: Tag and Content Characteristics
# 1. How many tags does each video have? Visualize the distribution using a histogram.

# 2. What is the total number of views per uploader? Rank the results in descending order.

# 3. Which video has the longest duration? List the title and its duration.

# 4. How many videos were uploaded in each year? Present the results sorted by year.

# 5. Is there a correlation between the number of views and the number of likes? 
# Feel free to drop or filter rows with missing or zero values before computing correlation.

## 3.3: Derived Metrics & Custom Analysis
# 1. Which video has the highest number of likes per second of duration?

# 2. Which uploader has the longest total duration of all their uploaded videos combined?

# 3. What is the ratio of views to likes for each video?