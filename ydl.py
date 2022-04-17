import youtube_dl
from youtube_search import YoutubeSearch


def download_from_youtube(user_input):
    with youtube_dl.YoutubeDL({"format": "bestaudio"}) as ydl:
        try:
            info = ydl.extract_info(user_input, download=False)
            url = info["formats"][0]["url"]
            return url
        except:
            # results = YoutubeSearch(user_input, max_result=1).to_dict()
            return None
