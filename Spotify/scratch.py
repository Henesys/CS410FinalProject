def get_artist_info():
    artist_name = artist_entry.get()
    
    try:
        artist = sp.search(q=artist_name, type='artist', limit=1)['artists']['items'][0]
        artist_id = artist['id']
        top_tracks = sp.artist_top_tracks(artist_id)

        top_track_info = ""
        for track in top_tracks['tracks']:
            track_name = track['name']
            track_popularity = track['popularity']
            lyrics = get_lyrics(artist_name, track_name)
            sentiment_score = analyze_sentiment(lyrics)

            top_track_info += f"Track: {track_name}\n"
            top_track_info += f"Popularity: {track_popularity}\n"
            top_track_info += f"Sentiment Score: {sentiment_score}\n\n"

        info_text.config(state=tk.NORMAL)
        info_text.delete('1.0', tk.END)
        info_text.insert(tk.END, top_track_info)
        info_text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", str(e))