import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col
import ast

# Import the data frame
df = pd.read_csv("combined_data.csv", sep = ";")
print(df.head())

## 3.1: Descriptive Statistics (pandas)
print("Descriptive Statistics (pandas)")

# 1. What is the average duration (in seconds) of all videos in the dataset?
mean_pd = df[["duration_seconds"]].mean()
print(f"The mean in seconds of the durations of the videos is: {round(mean_pd["duration_seconds"], 2)}")

# 2. Which uploader appears most frequently in the dataset?
mode_pd = df["uploader"].mode()
print(f"The most popular uploader is: {mode_pd[0]}")

# 3. Which five videos have the highest number of views? List their titles and view counts.
top_5_pd = df[["title","view_count" ]].sort_values(by =["view_count"], ascending = False).head(5)
print(top_5_pd)

# 4. For each upload year, what is the average number of likes?
df_year_likes = df[["year_uploaded", "like_count"]]
df_year_likes = df_year_likes.groupby(["year_uploaded"]).mean().round(2)
print(df_year_likes)

# 5. How many videos are missing artist information?
is_null = df["artist"].isna().sum()
print("The number of missing artist information is: ", is_null)

# 3.1: Descriptive Statistics (spark)
print("Descriptive Statistics (spark)")

spark = SparkSession.builder.appName("Assignment").getOrCreate()
df_sp = spark.read.option("header", True).option("inferSchema", True).option("sep", ';').csv("combined_data.csv")
df_sp.printSchema()
df_sp.show()

# 1. What is the average duration (in seconds) of all videos in the dataset?
print("The average duration in seconds is:")
df_sp.select(avg("duration_seconds")).show()

# 2. Which uploader appears most frequently in the dataset?
top_uploader = df_sp.groupBy("uploader").count().orderBy("count", ascending = False).first()
print("The top uploader is: ", top_uploader["uploader"] )

# 3. Which five videos have the highest number of views? List their titles and view counts.
print("The top 5 videos by views:")
df_sp.select("title", "view_count").orderBy("view_count").show(5)

# 4. For each upload year, what is the average number of likes?
print("Average likes per year:")
df_sp.groupBy("year_uploaded").agg(avg("like_count")).show()

# 5. How many videos are missing artist information?
n_artist_nan = df_sp.filter(col("artist").isNull()).count()
print("The number of artist missing is: ", n_artist_nan)

## 3.2: Tag and Content Characteristics
print("Tag and Content Characteristics")

# 1. How many tags does each video have? Visualize the distribution using a histogram.
plt.ion()
plt.figure(figsize=(8, 5))
plt.hist(df["tag_count"], bins=range(0, df["tag_count"].max() + 2), edgecolor='black')
plt.title("Distribution of tags per video")
plt.xlabel("Number of tags")
plt.ylabel("Number of vídeos")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("tag_distribution_histogram.png")
print("Histogram saved as tag_distribution_histogram.png")


# 2. What is the total number of views per uploader? Rank the results in descending order.
df_views_uploader = df[["uploader", "view_count"]]
df_views_uploader = df_views_uploader.groupby(["uploader"]).sum()
df_views_uploader["rank"] = df_views_uploader["view_count"].rank(method = "max", ascending = False)
print("The total number of views per uploader is:")
print(df_views_uploader)

# 3. Which video has the longest duration? List the title and its duration.
long = df["duration_seconds"].max()
long_row = df[df["duration_seconds"] == long]
long_v = long_row["title"].values[0]
print(f"The longest video is: ", long_v)

# 4. How many videos were uploaded in each year? Present the results sorted by year.
df_year = df[["year_uploaded"]].groupby(["year_uploaded"]).size()
df_year = df_year.sort_index()
print("Videos uploaded per year:")
print(df_year)

# 5. Is there a correlation between the number of views and the number of likes? 
# Feel free to drop or filter rows with missing or zero values before computing correlation.
df_corr = df[["view_count", "like_count"]]
print("Correlation between views and likes:")
print(df_corr.corr())

## 3.3: Derived Metrics & Custom Analysis
print("Derived Metrics & Custom Analysis")

# 1. Which video has the highest number of likes per second of duration?
df["likes/second"] = round(df["like_count"]/df["duration_seconds"],2)
max_likes = df["likes/second"].max()
video_row = df[df["likes/second"] == max_likes]
video = video_row["title"].values[0]
print(f"The video with the highest number of likes per second is : ", video)

# 2. Which uploader has the longest total duration of all their uploaded videos combined?
df_duration = df[["uploader", "duration_seconds"]]
df_duration = df_duration.groupby(["uploader"]).sum()
uploader = df_duration["duration_seconds"].idxmax()
print(f"The uploader with the longest total duration is: ", uploader)

# 3. What is the ratio of views to likes for each video?
df["views/likes"] = round(df["view_count"]/df["like_count"],2)
df_views_likes = df[["title", "views/likes"]]
print("Ratio of views to like per each video")
print(df_views_likes)