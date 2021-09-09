# Takes a track and scrobbles it
# Mandatory parameter 1: "artist - track"
# Optional parameter 2: UNIX timestamp. Default: now
# Prerequisites: mylast.py, pyLast
import gspread
import random
import pandas as pd
import datetime
import sys
import time
import sensitiveInfo
from oauth2client.service_account import ServiceAccountCredentials

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


#scrobble_track(artist_track, unix_timestamp)
def get_random_album():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(sensitiveInfo.jsonName, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open(sensitiveInfo.spreadsheetName)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    random_seed = random.randrange(2, len(sheet_instance.get_all_values()), 1)

    records_data = sheet_instance.row_values(random_seed)
    print(records_data)

    return records_data
    # view the data
def scrobble_random_album():
    randAlbum = get_random_album()

    try:
        album = lastfm_network.get_album(randAlbum[0], randAlbum[1])
    except:
        print("FAILURE, COULD NOT FIND ALBUM ", randAlbum)
    
    #album = lastfm_network.get_album("Lorde", "The Love Club EP")
    try:
        albumToScrobble = album.get_tracks()
    except:
        print("FAILURE, COULD NOT FIND ALBUM ", randAlbum)

    length = 0
    length = len(albumToScrobble)
    print(length, " Total Tracks To Be Scrobbled")
    if (length > 0 and length < 30):
        for x in range(0,length):
            lastfm_network.scrobble(albumToScrobble[x].artist, albumToScrobble[x].title, time.time())
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
if(sys.argv[1]):
    scrobbleAlbumsAmt = int(sys.argv[1])
    for x in range(0, scrobbleAlbumsAmt):
        scrobble_random_album()
    
    # End of file