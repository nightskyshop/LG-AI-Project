from mutagen.mp3 import MP3

urls = ['https://gohistory.pythonanywhere.com/media/audios/%EA%B3%A0%EB%8C%80_38%EC%9E%A5_%EC%9D%B4%EC%9D%B8%ED%98%9C.mp3']
end_time = MP3(urls[0]).info.length