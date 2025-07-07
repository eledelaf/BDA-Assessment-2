# AudioPulse Capstone Project Report
## Part 1: Audio Download Pipeline & Logging
The goal of Part 1 is to create a working pipeline that downloads audio from a list of YouTube URLs, extracts the metadata, and logs the process. This has been done in two ways: a serial version and a parallel version.

### Pipeline
For the pipeline part, there is a process that starts with a list of YouTube URLs and goes all the way to downloading the audio, saving the metadata, and logging everything that happens along the way.

Step 1: First the *video_urls.txt* file with 10+ links (one per line), mostly music. The script reads those into a list:
``` python
with open("video_urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]
That gives us a clean list to work with.
```

Step 2: For each URL, the script does three things using the functions *get_video_info()* and *extract_metadata()*:
    1. Downloads the audios using *yt-dlp*.
    2. Extracts the metadata (title, views, tags, uploader, etc.).
    3. Saves it as a *.json* file inside the *audio_output/* folder.

Step 3: After each download, we write a log entry to a file called *download_log.txt* inside a *logs* folder. This tracks whether each URL worked or failed, and adds a timestamp.

Step 4: I built a parallel and a serial way to run the downloads. 
    1. Serial: This one is super simple and very reliable. The script goes through each URL, waits until the download finishes, then moves on to the next.
    2. Parallel: This one uses threads and allows up to 5 downloads running at once. This version was way faster — about 5 to 6 seconds total. I also tested going fully parallel with no thread limit, and that took 3–4 seconds, but it was less stable and risked overloading the system or hitting rate limits from YouTube.


### Serial vs Parallel
The assessment asked to do two different processes to download the data — one serial and one parallel version allowing up to 5 downloads at a time. I did both, and I also tried downloading all at once to test the limits.

There is a big time difference (which can vary slightly depending on the run). The serial version took around 50 to 60 seconds, the fully parallel version took 3 to 4 seconds, and the parallel version with a semaphore (5 threads) took around 5 to 6 seconds.

The good part about the serial approach is that it's reliable and simpler — easier to code and explain. But it's very slow. In this case, we’re only downloading 10 to 15 songs and it’s already long. For bigger datasets, it’s not practical.

Parallel programming is more complex to implement, and if there’s an error, I think it’s harder to trace. But the big advantage is that it’s faster and more scalable.

## Part 2: Audio Data Extraction
The code in this part was provided by the teacher, I only changed the separation when saving the csv file since some of the data had comas inside i was having some problems downloading the data set when using spark. The solution i found was changig this line of code: 
```python 

" df.to_csv("combined_data.csv", index = False)" 
```
to  
```python
"df.to_csv("combined_data.csv", index = False, sep = ';')".
```
What this code does is create a *.csv* document with the information of each video in the list of URLs in *.txt* file.

## Part 3: Data Analysis
For this part, I worked with the *combined_metadata.csv* that we created in Part 2. I used both pandas and Spark to run the required analyses. Since the dataset is relatively small, pandas was quicker and easier to use, but I also used Spark for section 3.1.

### 3.1 Descriptive Statistics
The main tasks in this section where completed by pandas and spark:
1. I calculated the average video duration in seconds using both pandas and Spark.
2. I grouped by the uploader column and counted how often each one appears.
3. Sorted the DataFrame by view_count and selected the top 5.
4. I used groupby() in pandas and groupBy().agg() in Spark.
5. I counted how many rows had a null or missing value in the artist column.

### 3.2 Tag and Content Characteristics
This part focused on tags, content trends and distributions:
1. Visualize the distribution using a histogram.
2. Ranking the results of a query.
3. List the title and its duration. 
4. Present results sorted by a specific column. 
5. Look for a correlation.

### 3.3 Derived Metrics & Custom Analysis
In this section we had to do a few extra calculations for the dataset:
1. Likes per second of duration.
2. Total duration per uploader.
3. Views to likes radio.
