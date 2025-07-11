import yt_dlp
import certifi
import os
import json
import time 
import multiprocessing as mp 
from datetime import datetime 

OUTPUT_DIR = "audio_output"
LOG_DIR = "logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.environ["SSL_CERT_FILE"] = certifi.where()

def get_video_info(url: str, download: bool = True) -> dict:
    """Extract video info and optionally download the audio without warnings."""
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,          # suppress general output
        'no_warnings': True,    # suppress warnings
        'skip_download': not download,
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=download)
    
def extract_metadata(info: dict) -> dict:
    """Filter and return relevant metadata fields, including derived values."""
    upload_date = info.get("upload_date")
    tags = info.get("tags") or []

    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "uploader_id": info.get("uploader_id"),
        "channel": info.get("channel"),
        "track": info.get("track"),
        "artist": info.get("artist"),
        "album": info.get("album"),
        "description": info.get("description"),
        "tags": tags,  # Ensure it's a list
        "duration_seconds": info.get("duration"),
        "upload_date": upload_date,
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "webpage_url": info.get("webpage_url"),

        # Derived fields
        "year_uploaded": int(upload_date[:4]) if upload_date else None,
        "tag_count": len(tags),
    }

def save_metadata_to_file(metadata: dict, title: str) -> str:
    """Save metadata as a JSON file and return the path."""
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
    file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    return file_path

def logging(url: str, download: bool):
    """ After each download writes a log to the "download_log.txt" file """
    log_path = os.path.join(LOG_DIR, "download_log.txt")
    #with open("download_log.txt", "a") as file: # "a" = append
    with open(log_path, "a") as file: # "a" = append
        timestamp = datetime.now().isoformat(timespec = "seconds")
        d = {"timestamp": timestamp, 
             "url": url,
             "download": download}
        file.write(json.dumps(d))
        file.write("\n")
    
def download_youtube_audio_with_metadata(url: str):
    """Main function to download audio and save metadata."""
    print(f"\n🎵 Downloading: {url}")
    try:
        info = get_video_info(url)
        metadata = extract_metadata(info)
        json_path = save_metadata_to_file(metadata, metadata["title"])
        print(f"✅ Done: {metadata['title']}\n📄 Metadata: {json_path}")
        logging(url, True)
    except Exception as e:
        print(f"❌ Failed to download: {url}\n   Error: {e}")
        logging(url, False)

def download_sem(url, semaphore):
    """ Main function to download audio and save metadata using the semaphore method."""
    with semaphore:
        print(f"\n🎵 Downloading: {url}")
        try:
            info = get_video_info(url)
            metadata = extract_metadata(info)
            json_path = save_metadata_to_file(metadata, metadata["title"])
            print(f"✅ Done: {metadata['title']}\n📄 Metadata: {json_path}")
            logging(url, True)
        except Exception as e:
            print(f"❌ Failed to download: {url}\n   Error: {e}")
            logging(url, False)

def parallel_runner(l_urls):
    # I used the code from the lab class 
    start = time.time()
    processes = []
    for urls  in l_urls:
        p = mp.Process(target = download_youtube_audio_with_metadata, args = [urls])
        p.start()
        processes.append(p)
    for process in processes:
        process.join()
    end = time.time()
    t = end-start
    print(f"Runing a parallel process took {round(t,2)} seconds")

def parallel_runner_sem(l_urls, n=5):
    start = time.time()
    
    manager = mp.Manager()
    semaphore = manager.Semaphore(n)

    processes = []
    for urls  in l_urls:
        p = mp.Process(target = download_sem, args = (urls, semaphore))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    end = time.time()
    t = end-start
    print(f"Runing a parallel process with semaphore took {round(t,2)} seconds")
    
if __name__ == "__main__":
    with open("video_urls.txt", mode = "r") as urls:
        youtube_urls = [linea.rstrip() for linea in urls]

    start = time.time()
    for url in youtube_urls:
        download_youtube_audio_with_metadata(url)
    end = time.time()
    print(f"Runing a serial process took {round(end-start,2)} seconds")

    parallel_runner(youtube_urls)

    parallel_runner_sem(youtube_urls)
