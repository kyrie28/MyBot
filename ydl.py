import youtube_dl
from youtube_search import YoutubeSearch


def download_from_youtube(user_input):
    with youtube_dl.YoutubeDL({"format": "bestaudio"}) as ydl:
        try:
            info = ydl.extract_info(user_input[0], download=False)
            URL = info["formats"][0]["url"]
            return URL
        except:
            kwd_str = "".join(str(s) + " " for s in user_input)[:-1]
            results = YoutubeSearch(kwd_str, max_results=1).to_dict()
            url = "https://www.youtube.com" + results[0]["url_suffix"]
            try:
                info = ydl.extract_info(url, download=False)
                URL = info["formats"][0]["url"]
                return URL
            except:
                return None
