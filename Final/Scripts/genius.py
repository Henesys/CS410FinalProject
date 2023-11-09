import re
import requests
from io import BytesIO

from lyricsgenius import Genius
from PIL import Image
from textblob import TextBlob

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
import contractions
from autocorrect import Speller

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric

import spacy
from sklearn.linear_model import LogisticRegression
nlp = spacy.load("en_core_web_md")

import credentials

import os
dir = os.path.dirname(__file__)

spell = Speller(lang='en')
genius = Genius(credentials.ACCESS_TOKEN, retries=5)
genius.remove_section_headers = True
top_song_num = 10
stop_words = set(stopwords.words('english'))

"""
Checks if Song Name that is about to be added is already in the Song List.
"""
def check_repeat(song_list, new_song_title):
    song_title = re.sub("\(.*?\)|\[.*?\]","", new_song_title).replace('\u200b', '').strip()
    if song_title in song_list:
        return False, song_title

    return True, song_title

"""
Processes Song Lyrics
-- removes stop words
-- removes punctuation
"""
def process_lyrics(lyrics):
    lyrics_lines = lyrics.split("Lyrics", 1)[1].strip()
    if len(lyrics_lines) < 1:
        lyrics_lines = lyrics
    lyrics_lines = re.sub(r'[^\w\d\s\'\-]+', '', lyrics_lines)
    lyric_tokens = lyrics_lines.split()
    filtered_lyrics = []
    for w in lyric_tokens:
        new_w = (contractions.fix(w)).lower()
        # if there are #s in the word, consider it neutral and skip
        if bool(re.search(r'\d', new_w)):
            continue

        # if there is an apostrophe in the word
        if "'" in new_w:
            new_w = new_w.replace("in'", "ing")
            new_w = new_w.replace("'bout", "about")
            new_w = new_w.replace("'til", "until")
            new_w = new_w.replace("'cause", "because")
            new_w = new_w.replace("'s", "")
        else:
            new_w = spell(new_w)

        # if word is a stop_word, skip
        if new_w in stop_words:
            continue

        filtered_lyrics.append(new_w)
    return filtered_lyrics

"""
Generates Word Cloud
"""
def word_cloud(lyrics):
    token_lyrics = word_tokenize(lyrics)
    pos_lyrics = nltk.pos_tag(token_lyrics)

    lyrics_out = ' '.join([word for (word, pos) in pos_lyrics if pos == 'NN'])

    with open(os.path.join(dir, "./Lists/top100common.txt")) as f:
        common_words = f.read().split()

    stopwords = set(STOPWORDS).union(set(common_words))

    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stopwords,
                    collocations=False,
                    min_font_size = 10).generate(lyrics_out)

    # plot the WordCloud image  
    plt.switch_backend('Agg')                     
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)

    wordcloud_path = os.path.join(dir, "./Figures/word_cloud.png")
    plt.savefig(wordcloud_path)

    im  = Image.open(wordcloud_path)
    return im

"""
Generates Song Subjectivity Distribution
"""
def get_song_subjectivity(subjectivities):
    values, counts = np.unique(subjectivities, return_counts=True)
    # Draw dot plot with appropriate figure size, marker size and y-axis limits
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#00BFFF', '#3591FF', '#6964FF', '#9E36FF', '#D208FF', '#00BFFF', '#3591FF', '#6964FF', '#9E36FF', '#D208FF']

    for value, count in zip(values, counts):
        ax.plot([value]*count, list(range(count)), 'co', c=colors[value - 1], ms=int(200 / max(counts)), linestyle='')

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    ax.yaxis.set_visible(False)
    ax.set_ylim(-0.75, max(counts))
    ax.set_xticks(range(1, 11))
    ax.set_xticklabels(['Objective', '', '', '', '', '', '', '', '', 'Subjective'])
    ax.tick_params(axis='x', length=0, pad=8, labelsize=18)
    #ax.set_title('Song Subjectivity Distribution', fontsize=18)

    subjectivities_path = os.path.join(dir, "./Figures/subjectivities_dist.png")
    plt.savefig(subjectivities_path)

    img_subjectivities  = Image.open(subjectivities_path)

    subjectivity_rating = np.round(np.mean(subjectivities), 1)

    return img_subjectivities, subjectivity_rating

"""
Generates Song Polarity Distribution
"""
def get_song_polarity(polarities):
    values, counts = np.unique(polarities, return_counts=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#FF0000', '#E32A01', '#C65502', '#AA8004', '#8EAA05', '#71D506', '#55FF07']

    for value, count in zip(values, counts):
        ax.plot([value]*count, list(range(count)), 'co', c=colors[value + 3], ms=int(200 / max(counts)), linestyle='')

    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

    ax.yaxis.set_visible(False)
    ax.set_ylim(-0.75, max(counts))
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels(['---', '--', '-', 'o', '+', '++', '+++'])
    ax.tick_params(axis='x', length=0, pad=8, labelsize=18)
    #ax.set_title('Song Polarity Distribution', fontsize=18)

    polarities_path = os.path.join(dir, "./Figures/polarities_dist.png")
    plt.savefig(polarities_path)

    img_polarities  = Image.open(polarities_path)

    polarity_value = sum(values * counts)
    polarity_verdict = 'o'

    if polarity_value < -30:
        polarity_verdict = '---'
    elif polarity_value < -15:
        polarity_verdict = '--'
    elif polarity_value < 0:
        polarity_verdict = '-'
    elif polarity_value > 30:
        polarity_verdict = '+++'
    elif polarity_value > 15:
        polarity_verdict = '++'
    elif polarity_value > 0:
        polarity_verdict = '+' 

    return img_polarities, polarity_verdict

"""
Generates Song Sentiment Distribution
"""
def get_song_sentiments(all_songs):
    polarities = []
    subjectivities = []
    for song in all_songs:
        blob = TextBlob(song)
        song_polarity = blob.sentiment.polarity
        song_subjectivity = blob.sentiment.subjectivity
        #polarities.append(song_polarity)
        #print(blob.tags)
        #print(blob.noun_phrases)
        #print(blob.sentiment)

        if song_polarity < -0.50:
            polarities.append(-3)
        elif song_polarity < -0.25:
            polarities.append(-2)
        elif song_polarity < -0.05:
            polarities.append(-1)
        elif song_polarity <  0.05:
            polarities.append(0)
        elif song_polarity <  0.25:
            polarities.append(1)
        elif song_polarity <  0.50:
            polarities.append(2)
        else:
            polarities.append(3)

        if song_subjectivity < 0.1:
            subjectivities.append(1)
        elif song_subjectivity < 0.2:
            subjectivities.append(2)
        elif song_subjectivity < 0.3:
            subjectivities.append(3)
        elif song_subjectivity <  0.4:
            subjectivities.append(4)
        elif song_subjectivity <  0.5:
            subjectivities.append(5)
        elif song_subjectivity <  0.6:
            subjectivities.append(6)
        elif song_subjectivity <  0.7:
            subjectivities.append(7)
        elif song_subjectivity <  0.8:
            subjectivities.append(8)
        elif song_subjectivity <  0.9:
            subjectivities.append(9)
        else:
            subjectivities.append(10)

    img_polarities, polarity_verdict = get_song_polarity(polarities)
    img_subjectivities, subjectivity_rating = get_song_subjectivity(subjectivities)
    return img_polarities, polarity_verdict, img_subjectivities, subjectivity_rating

"""
Save a searched artist
"""
def save_artist(artist_name, song_titles, all_songs):
    regex = re.compile('[^a-zA-Z]')
    artist_entry = regex.sub('', artist_name).lower()

    with open(os.path.join(dir, "./../Artists/artists.txt"), 'a', encoding='utf-8') as f:
        f.write(artist_entry + "\n")

    with open(os.path.join(dir,'./../Artists/Titles/' + artist_entry + "_titles.txt"), 'w') as f:
        f.write("\n".join(map(str, song_titles)))
    
    with open(os.path.join(dir, './../Artists/Lyrics/' + artist_entry + "_lyrics.txt"), 'w') as f:
        f.write("\n".join(map(str, all_songs)))

    return

"""
Check if artist lyrics were already processed
"""
def check_artist(query_artist):
    with open(os.path.join(dir, './../Artists/artists.txt'), encoding='utf-8') as f:
        artists = f.read().splitlines()
    
    regex = re.compile('[^a-zA-Z]')
    artist_entry = regex.sub('', query_artist).lower()

    if artist_entry in artists:
        return artist_entry
    
    artist_spelling = genius.search_artist(query_artist, max_songs=1)
    artist_name = regex.sub('', artist_spelling.name).lower()

    if artist_name in artists:
        return artist_name

    return False

"""
Get Artist Lyrics
"""
def get_lyrics(query_artist):
    artist_exists = check_artist(query_artist)

    if artist_exists:
        print("exists!")
        with open(os.path.join(dir, './../Artists/Titles/' + artist_exists + '_titles.txt'), encoding='utf-8') as f:
            song_titles = f.read().splitlines()
        
        with open(os.path.join(dir, './../Artists/Lyrics/' + artist_exists + '_lyrics.txt'), encoding='utf-8') as f:
            all_songs = f.read().splitlines()
    else:
        print("doesn't exist!")
        try:
            artist = genius.search_artist(query_artist, max_songs=20, sort='popularity') #max_songs set for testing efficiency
        except requests.exceptions.Timeout:
            print ("genius execution failed, please rerun program")
            sys.out(1)

        song_list = artist.songs

        song_titles = []
        song_lyrics = []
        for song in song_list:
            is_new, song_title = check_repeat(song_titles, song.title)
            if is_new:
                song_titles.append(song_title)
                lyrics = process_lyrics(song.lyrics)
                song_lyrics.append(lyrics)

        all_songs = [' '.join(lyric) for lyric in song_lyrics]

        save_artist(artist.name, song_titles, all_songs)

    all_lyrics = ' '.join(all_songs)
    #print(song_titles)
    #print(all_lyrics)

    return all_songs, all_lyrics


"""
Get Theme of Song Lyrics
"""
def get_abstract(words):
    classes = ['concrete', 'abstract']

    with open(os.path.join(dir, './Lists/concretenouns.txt'), encoding='utf-8') as f:
        concrete_nouns = f.read().splitlines()
    
    with open(os.path.join(dir, './Lists/abstractnouns.txt'), encoding='utf-8') as f:
        abstract_nouns = f.read().splitlines()

    train_set = [
        concrete_nouns,
        abstract_nouns,
    ]

    X = np.stack([list(nlp(w))[0].vector for part in train_set for w in part])
    y = [label for label, part in enumerate(train_set) for _ in part]
    classifier = LogisticRegression(C=0.1, class_weight='balanced').fit(X, y)

    output = []
    for token in nlp(' '.join(words)):
        if classes[classifier.predict([token.vector])[0]] == 'abstract':
            output.append(str(token))

    return output

def sent_to_words(lyrics):
    yield(gensim.utils.simple_preprocess(str(lyrics), deacc=True))

def get_theme(lyrics):
    out_lyrics = lyrics
    i = 0
    while i < 5:
        token_test = word_tokenize(out_lyrics)
        pos_test = nltk.pos_tag(token_test)
        i += 1

        out_lyrics = ' '.join([word for (word, pos) in pos_test if (pos == 'NN' and 'thing' not in word)])

    lyrics = list(sent_to_words(out_lyrics))

    with open(os.path.join(dir, './Lists/top100common.txt'), encoding='utf-8') as f:
        common_words = f.read().split()

    stopwords = set(STOPWORDS).union(set(common_words))

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) 
                if word not in stopwords] for doc in texts]
    
    data_words = remove_stopwords(lyrics)

    id2word = corpora.Dictionary(data_words)
    texts = data_words
    corpus = [id2word.doc2bow(text) for text in texts]

    num_topics = 20
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)

    lda_topics = lda_model.show_topics(num_words=20)

    topics = []
    filters = [lambda x: x.lower(), strip_punctuation, strip_numeric]

    for topic in lda_topics:
        topics.append(preprocess_string(topic[1], filters))

    themes = get_abstract(topics[0])

    if len(themes) < 1:
        return topics[:3]
    return themes[:3]

"""
Get Genius Lyrics Analysis of Artist Lyrics
"""
def process_artist_lyrics(query_artist):
    all_songs, all_lyrics = get_lyrics(query_artist)
    themes = get_theme(all_lyrics)

    img_wordcloud = word_cloud(all_lyrics)
    img_polarities, polarity_verdict, img_subjectivities, subjectivity_rating = get_song_sentiments(all_songs)

    return all_songs, themes, img_wordcloud, img_polarities, img_subjectivities, subjectivity_rating, polarity_verdict