from scrape import Scrape
from spotify_apis import Spotify

user_date = input("Which year do you want to travel to? Enter the date in this format YYYY-MM-DD: ")

# Data from billboards
scrape = Scrape(user_date)
data = scrape.scrape_data()
for i in range(len(data)):
    print(f"Song {i+1}: {data[i]}")


# Search songs from spotify
spotify = Spotify()
spotify.authenticate()
user_id = spotify.get_profile()
playlist_id = spotify.create_playlist(playlist_name=f'Billboard\'s hot songs - {user_date}')
uris = []
for song in data:
    uri = spotify.search(song)
    uris.append(f"{uri}")
# uris = uris.split(', ')
print(uris, len(uris))
spotify.add_song_to_list(playlist_id, uris)
