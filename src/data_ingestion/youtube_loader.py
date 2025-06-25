# from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from dotenv import load_dotenv
# import os
# import logging
# import re

# class YouTubeTranscriptLoader:
#     """Loads transcripts of Indian law lecture videos from YouTube and saves them."""
    
#     def __init__(self, base_path=r"C:\Users\bhati\OneDrive\Desktop\my_legal_ai_project\data"):
#         """Initialize with base path, YouTube API, and logging."""
#         load_dotenv()  # Load .env file
#         self.base_path = base_path
#         self.output_path = os.path.join(base_path, r"raw\youtube_transcripts")
#         self.logger = self._setup_logging()
#         os.makedirs(self.output_path, exist_ok=True)
#         self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
#         if not self.youtube_api_key:
#             raise ValueError("YOUTUBE_API_KEY not found in .env file.")
#         self.youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
#         self.search_terms = [
#             "Indian law lecture",
#             "Indian Constitution lecture",
#             "Indian Penal Code lecture",
#             "Indian Contract Act lecture",
#             "Indian Evidence Act lecture",
#             "Indian legal system lecture"
#         ]

#     def _setup_logging(self):
#         """Configure logging for loader execution."""
#         logging.basicConfig(
#             level=logging.INFO,
#             format="%(asctime)s - %(levelname)s - %(message)s",
#             handlers=[
#                 logging.FileHandler(os.path.join(self.base_path, "youtube_loader.log")),
#                 logging.StreamHandler()
#             ]
#         )
#         return logging.getLogger(__name__)

#     def search_videos(self, max_results=10):
#         """Search YouTube for Indian law lecture videos."""
#         video_urls = []
#         for term in self.search_terms:
#             try:
#                 self.logger.info(f"Searching YouTube for: {term}")
#                 request = self.youtube.search().list(
#                     part="id,snippet",
#                     q=term,
#                     type="video",
#                     maxResults=max_results,
#                     videoCaption="closedCaption"  # Only videos with captions
#                 )
#                 response = request.execute()
#                 for item in response["items"]:
#                     video_id = item["id"]["videoId"]
#                     video_url = f"https://www.youtube.com/watch?v={video_id}"
#                     video_urls.append(video_url)
#                 self.logger.info(f"Found {len(response['items'])} videos for term: {term}")
#                 time.sleep(1)  # Respect API rate limits
#             except HttpError as e:
#                 self.logger.error(f"Error searching YouTube for {term}: {str(e)}")
#         return list(set(video_urls))  # Remove duplicates

#     def is_indian_law_related(self, transcript):
#         """Check if transcript contains Indian law-related keywords."""
#         keywords = [
#             "indian law", "constitution of india", "indian penal code", "contract act",
#             "criminal procedure", "evidence act", "civil procedure", "supreme court of india",
#             "high court", "legal system", "indian legislation", "jurisprudence"
#         ]
#         transcript_text = " ".join([entry["text"] for entry in transcript]).lower()
#         return any(keyword in transcript_text for keyword in keywords)

#     def get_video_id(self, url):
#         """Extract video ID from YouTube URL."""
#         try:
#             video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
#             return video_id.group(1) if video_id else None
#         except Exception as e:
#             self.logger.error(f"Invalid URL {url}: {str(e)}")
#             return None

#     def fetch_transcript(self, video_id):
#         """Fetch transcript for a given video ID."""
#         try:
#             transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-IN'])
#             if self.is_indian_law_related(transcript):
#                 return transcript
#             else:
#                 self.logger.info(f"Video {video_id} not related to Indian law")
#                 return None
#         except (NoTranscriptFound, TranscriptsDisabled) as e:
#             self.logger.error(f"No transcript available for video {video_id}: {str(e)}")
#             return None
#         except Exception as e:
#             self.logger.error(f"Error fetching transcript for video {video_id}: {str(e)}")
#             return None

#     def save_transcript(self, transcript, video_id):
#         """Save transcript to file."""
#         try:
#             transcript_text = "\n".join([entry["text"] for entry in transcript])
#             file_path = os.path.join(self.output_path, f"{video_id}.txt")
#             with open(file_path, "w", encoding="utf-8") as f:
#                 f.write(transcript_text)
#             self.logger.info(f"Saved transcript to {file_path}")
#         except Exception as e:
#             self.logger.error(f"Failed to save transcript for {video_id}: {str(e)}")

#     def load_transcripts(self, max_results=10):
#         """Search for Indian law lecture videos and load their transcripts."""
#         self.logger.info("Starting YouTube transcript loading...")
#         video_urls = self.search_videos(max_results)
#         self.logger.info(f"Found {len(video_urls)} unique video URLs")
        
#         for url in video_urls:
#             video_id = self.get_video_id(url)
#             if not video_id:
#                 continue
#             transcript = self.fetch_transcript(video_id)
#             if transcript:
#                 self.save_transcript(transcript, video_id)
#         self.logger.info("Transcript loading completed.")

# if __name__ == "__main__":
#     loader = YouTubeTranscriptLoader()
#     loader.load_transcripts()
