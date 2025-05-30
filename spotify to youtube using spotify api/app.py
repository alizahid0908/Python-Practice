import imp
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, url_for, session, request, redirect
import json
import time
import pandas as pd

from .downloadmp3 import DownloadVideosFromTitles

app = Flask(__name__)


app.secret_key = "OnGfrfrfrjlt123456789"

app.config["SESSION_COOKIE_NAME"] = "My Cookie"
TOKEN_INFO = "token_info"


@app.route("/")
def login():
    sp_oauth = createSpotifyOauth()
    authUrl = sp_oauth.get_authorize_url()
    return redirect(authUrl)


@app.route("/redirect")
def redirectPage():
    sp_oauth = createSpotifyOauth()
    session.clear()
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True))


@app.route("/getTracks")
def getTracks():
    # return "Fist Fight Music"
    session[TOKEN_INFO], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect("/")
    sp = spotipy.Spotify(auth=session.get(TOKEN_INFO).get("access_token"))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)["items"]
        for idx, item in enumerate(curGroup):
            track = item["track"]
            val = track["name"] + " - " + track["artists"][0]["name"]
            results += [val]
        if len(curGroup) < 50:
            break

    df = pd.DataFrame(results, columns=["song names"])
    df.to_csv("songs.csv", index=False)
    return "done"


# Checks to see if token is valid and gets a new token if not
def get_token():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get("token_info", False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get("token_info").get("expires_at") - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        sp_oauth = createSpotifyOauth()
        token_info = sp_oauth.refresh_access_token(
            session.get("token_info").get("refresh_token")
        )

    token_valid = True
    return token_info, token_valid


def createSpotifyOauth():
    return SpotifyOAuth(
        client_id="d9e173cea53e4b69aa6e19a6a1bc23c2",
        client_secret="efc95a3ecde7421aace0caab97329147",
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-library-read",
    )
