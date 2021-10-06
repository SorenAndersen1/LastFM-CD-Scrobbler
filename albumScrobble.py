# Takes a track and scrobbles it
# Mandatory parameter 1: "artist - track"
# Optional parameter 2: UNIX timestamp. Default: now
# Prerequisites: mylast.py, pyLast

import datetime
import sys
import time
import sensitiveInfo
from mylast import lastfm_network, split_artist_track


testMode = False
if testMode:
    print("Test mode, won't actually scrobble.")
else:
    print("Live mode, can scrobble.")

unix_timestamp = 0

unix_timestamp = time.time()

artist_track = "Not"

def get_last2_tracks():
    recent_tracks = lastfm_network.get_user(sensitiveInfo.username).get_recent_tracks(limit=2)
    return recent_tracks

def scrobble_track(artist_track, unix_timestamp):

    (artist, track) = split_artist_track(artist_track)

    # Validate
    if unix_timestamp == 0:
        # Get UNIX timestamp
        unix_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    print("Timestamp:\t" + str(unix_timestamp))

    # Scrobble it
    if not testMode:
        lastfm_network.scrobble(artist=artist, title=track, timestamp=unix_timestamp)

    # Confirm
    # print("Confirmation from Last.fm:")
    # recent_tracks = lastfm_network.get_user(
    # lastfm_username).get_recent_tracks(limit=1)
    # for track in recent_tracks:
    # unicode_track = unicode(str(track.track), 'utf8')
    # # print_it(track.playback_date + "\t" + unicode_track)
    # print(track.playback_date + "\t" + unicode_track)


def scrobble_album(albumArtist, albumTitle):
    artist = ""
    album = ""
    randAlbum = [artist, album]
    try:
        artist = albumArtist.replace('"','')
        album = albumTitle.replace('"','')
        album = album.replace('\n','')

        randAlbum = [artist, album]
    except:
        print(randAlbum)
    try:
        album = lastfm_network.get_album(randAlbum[0], randAlbum[1])
    except:
        print("FAILURE, COULD NOT FIND ALBUM ", randAlbum)
    albumToScrobble = album.get_tracks()
    length = len(albumToScrobble)
    print(length, " Total Tracks To Be Scrobbled")
    if (length > 0 and length < 30):
        for x in range(0,length):
            lastfm_network.scrobble(albumToScrobble[x].artist, albumToScrobble[x].title, time.time())
            #print(albumToScrobble[x].title)
        last_tracks_played = get_last2_tracks()
        time.sleep(5)
        last_Scrobbled = [albumToScrobble[length - 1].artist, albumToScrobble[length - 1].title]

        artist_Last_Played = [last_tracks_played[0].track.get_artist(), last_tracks_played[1].track.get_artist()]
        track_Last_Played = [last_tracks_played[0].track.get_title(), last_tracks_played[1].track.get_title()]

        if artist_Last_Played[0] == last_Scrobbled[0] or artist_Last_Played[1] == last_Scrobbled[0]:
                print("Success!")
                print("Album Scrobbled: ", randAlbum[1], " By :", randAlbum[0], " With a total of ", length, "tracks") 

        else:
                print("Album Scrobbled Failed, not same Last Artist: ", randAlbum[0], " ",  randAlbum[1], " ")
                print("1.", track_Last_Played[0], " - " , artist_Last_Played[0])
                print("2.", track_Last_Played[1], " - " , artist_Last_Played[1])

    else:
        print("Invalid Track Amt", randAlbum[0], " By :", randAlbum[1], " With a total of ", length)

def album_input():
    if(len(sys.argv[1].split(".")) > 1):
        ##Then its a text file
        albumList = open(sys.argv[1])
        for albumText in albumList:
            albumDetails = albumText.split("-")
            try:
                scrobble_album(albumDetails[0], albumDetails[1])
            except:
                print("Error Scrobbling Album ", albumText)
        albumList.close()
    else:
        try:
            sys.argv[2]
        except:
            print("Album Title Not added!")
        scrobble_album(sys.argv[1],sys.argv[2])

album_input()

# End of file