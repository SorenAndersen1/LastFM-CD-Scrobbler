# LastFM CD Scrobbler

These few python files are intended to simulate scrobbles outside of LastFM's ability, such as listening on CD or vinyl. randomscrobble.py reads in from a google sheet and randomly selects an album from a list, while albumScrobble.py takes in a command line argument in the format of artist title and scrobbles it to the specified account.

## Getting Started

### Dependencies

* APIs Used
  * LastFM
  * Google Drive/Sheets

* Python Libraries
  * Pylast
  * Pandas
  * oauth2client

* Personal Necesscary files
  * sensitiveInfo.py
  * Generated sheets JSON

### Setup

* Both a Google Drive account as well as a LastFM account is needed.
  * First simply set up LastFM API using the website, I [used this link](https://www.last.fm/api/account/create) to create my API

* Google Drive API
  * Next a Google API account [I used this guide](https://developers.google.com/drive/api/v3/quickstart/python)
  * Unlike the LastFM api this requires a bit more work, and the creation of a file (quickstart.py) in order for a json to be generated for the corresponding Google Sheet.

* Once both the Google Sheets API is pointing to a sheet with one column as "artist" and the next as "album" with coressponding albums for possible desired random scrobbles, all the personal information necessecary needs to be filled in to a sensitiveInfo.py file. 

sensitiveInfo.py format:
```
username = "Insert_Your_LastFM_Username_Here"
password_hash = "Insert_Your_LastFM_Password_Here"
API_KEY = "Insert_Your_LastFM_API_Key_Here"  
API_SECRET = "Insert_Your_LastFM_Secret_Here"
jsonName = 'Insert_Your_Sheets_JSON_Name_Here'
spreadsheetName = 'Insert_Desired_Spreadsheet_Name_Here'
```

### Executing program

```
python3 randomScrobble.py "# of albums to be randomly scrobbled"
EX: python3 randomScrobble.py 3
```
```
python3 albumSrobble.py "artist" "album"
EX: python3 albumScrobble.py Lorde Melodrama
```



## Code Used
https://github.com/pylast/pylast
https://github.com/hugovk/lastfm-tools
