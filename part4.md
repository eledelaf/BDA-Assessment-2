# AudioPulse Capstone Project Report

## Part 1: Audio Download Pipeline & Logging
The goal of Part 1 is to create a working pipeline that downloads audio from a list of Youtube URLs, extracts the metadata, and logs the process. This has been done in two ways, a serial way and a parallel way. 

### Pipeline
For the pipeline part, there is a process that starts with a list of YouTube URLs and goes all the way to downloading the audio, saving the metadata, and logging everything that happens along the way.

Step 1: First the video_urls.txt file with 10+ links (one per line), mostly music. The script reads those into a list:
with open("video_urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]
That gives us a clean list to work with.

Step 2: For each URL, the script does three things using the functions get_video_info() and extract_metadata():
    1. Downliads the audios using yt-dlp
    2. Extracts the metadata (title, views, tags, uploader, etc.)
    3. Saves it as a .json file inside the audio_output/ folder

Step 3: After each download, we wirte a log entry to a file called download_log.txt inside a log document. This tracks whether each URL worked or failed, and adds a timestamp.

Step 4: I built a parallel and a serial way to run the downloads. 
    1. Serial: This one is super simple and very reliable. The script goes through each URL, waits until the download finishes, then moves on to the next.
    2. Parallel: This one uses threads and allows up to 5 downloads running at once. This version was way faster — about 5 to 6 seconds total. I also tested going fully parallel with no thread limit, and that took 3–4 seconds, but it was less stable and risked overloading the system or hitting rate limits from YouTube.


### Serial vs Parallel
The assesment asked to do two different process to download the data, one serial and one parllel extracting 5 songs at the time. I did that and also I wanted to try to extract all of the information at once. 
There is a massive time difference, ofc this changes every time but more or less the serial one will take about 50 to 60 seconds while the parallel process takes 2 to 4 seconds and the one wiht a semaphore will take 5 to 6 seconds. 

The positive notes about the serial approach would be that ise reliable and simpler so is an easier code to code and to explain. But its slow, in this scenario we are only looking into 10 to 15 songs and it takes that much, but if we wanted to use bigger amounts of data it will not be an option.

The parallel programming on the other hand is more complex to program and if there is an error on the process i thing is more difficult to know where the problem is. The good things about this is that is faster and more scalable.

## Part 2: Audio Data Extraction
The code in this part was provided by the teacher, I only changed the separation when saving the csv file since some of the data had comas inside i was having some problems downloading the data set when using spark. The solution i found was changig this line of code: " df.to_csv("combined_data.csv", index = False)" to  "df.to_csv("combined_data.csv", index = False, sep = ';')".
What this code does is create a .csv document with the information of each video in the list of URLs in .txt

## Part 3: Data Analysis
### 3.1 Descriptive Statistics
### 3.2 Tag and Content Characteristics
### 3.3 Derived Metrics & Custom Analysis

