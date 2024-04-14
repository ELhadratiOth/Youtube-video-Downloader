from pytube import  Playlist

playlist = Playlist("https://youtube.com/playlist?list=PLTEenozo5AuE2Bx9BylCKycSu-PtDbFml&si=g89IKPtOM-fZFIif")
print(playlist.last_updated)
