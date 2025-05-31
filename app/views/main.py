from flask import Flask, request, render_template, redirect, session, url_for, make_response, jsonify, abort
import uuid
import os
import json

from argon2 import PasswordHasher
from werkzeug.utils import secure_filename

from googledrive import upload_song, upload_image, delete_file
from googleapiclient.errors import HttpError

from sql import insert_song, insert_album, insert_playlist, insert_song_to_playlist, insert_updated_playlist, get_data, delete_song, delete_album, delete_playlist

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/data")
ALLOWED_EXTENSIONS = {"png", "jpg", "jfif", "jpeg", "gif", "webp", "mp3", "wav"}
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "tajnyklic"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def precti_json(nazev_souboru):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    return USERS
def zapis_do_json(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    USERS.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(USERS, outline, indent=2)

    return

def vytvor_json(nazev_souboru):
    data_na_zapis = []
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data/chats", f"{nazev_souboru}.json")

    with open(json_url, 'w', encoding="utf-8") as outfile:
        json.dump(data_na_zapis, outfile)

    return

def generate_id():
    return str(uuid.uuid4())


def precti_json_chats(nazev_souboru):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data/chats", f"{nazev_souboru}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    return USERS
def zapis_do_json_chats(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data/chats", f"{nazev_souboru}.json")
    USERS = json.load(open(json_url,"r",encoding="utf-8"))
    USERS.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(USERS, outline)

    return

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

# --- Social ---

@app.route('/social')
def social():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    username = session.get("uzivatel")

    posts = precti_json("posts")

    chats = precti_json("chats")

    return render_template("Social.html", username=username, posts=posts, chats=chats)

@app.route('/zpracuj-post', methods=["POST"])
def zpracuj_post():
    username = session.get("uzivatel")
    content = request.form.get("post_content")
    attachment = request.files["post_attachment"]

    print(attachment.filename)

    if(attachment.filename != ""):
        attachment.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/attachments", attachment.filename))

    post_id = 0

    posty = precti_json("posts")
    for p in posty:
        if p["code"] == post_id:
            post_id += 1

    novy_post = {
        "username": username,
        "content": content,
        "attachment": attachment.filename,
        "code": post_id,
    }
    zapis_do_json("posts", novy_post)
    # note to self: jde jich dysplaynout max 5 + ten hard coded
    return redirect(url_for("social"))

@app.route('/zpracuj-chat', methods=["POST"])
def zpracuj_chat():
    username = session.get("uzivatel")
    username2 = request.form.get("chat_person")

    post_id = 0

    posty = precti_json("chats")
    for p in posty:
        if p["code"] == post_id:
            post_id += 1

    novy_post = {
        "username": username,
        "username2": username2,
        "code": post_id,
    }
    zapis_do_json("chats", novy_post)
    chat_json = "chat_"+str(post_id)
    vytvor_json(chat_json)
    # note to self: jde jich dysplaynout max 5 + ten hard coded
    return redirect(url_for("social"))

@app.route('/social/chat_url/<int:number>', methods=['GET'])
def get_chat(number):
    # Construct the file name
    print("hledání souboru")
    filename = f'static/data/chats/chat_{number}.json'
    print("soubor nalezen")
    
    # Check if the file exists
    if not os.path.exists(filename):
        abort(404)  # Return a 404 error if the file does not exist
    
    filename = f'chat_{number}'
    chats = precti_json_chats(filename)
    username = session.get("uzivatel")

    return render_template("Chats.html", chats=chats, username=username)

@app.route("/posli_chat", methods=["POST"])
def posli_chat():
    username = session.get("uzivatel")
    username2 = request.form.get("chat_person")
    chat = request.form.get("chat_number")

    filename = f'chat_{chat}'

    print(filename)

    post_id = 0

    posty = precti_json_chats(filename)
    for p in posty:
        if p["code"] == post_id:
            post_id += 1

    novy_post = {
        "username": username,
        "content": username2,
        "code": post_id,
    }
    zapis_do_json_chats(filename, novy_post)
    # note to self: jde jich dysplaynout max 5 + ten hard coded
    return redirect(url_for("get_chat", number=chat))

# --- Profile ---

@app.route("/profile", methods=["POST", "GET"])
def profile():
    if "uzivatel" in session:
        jmeno = session["uzivatel"]
        userColor = request.cookies.get("userBgColor", None)

        if request.method == "POST":
            pozadi = request.form.get("setbgcolor")
            userColor = pozadi or request.cookies.get("userBgColor") or "#ffffff"  # fallback barva
            resp = make_response(render_template("profile.html", jmeno=jmeno, userColor=userColor))

            if pozadi:
                resp.set_cookie("userBgColor", pozadi)

            if "userpfp" in request.files:
                file = request.files["userpfp"]
                if file and allowed_file(file.filename):
                    filename = secure_filename(f"{jmeno}_{file.filename}")
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    file.save(file_path)
                    session["pfp_filename"] = filename

            return resp

        return render_template("profile.html",
                               jmeno=jmeno,
                               userColor=userColor,
                               pfp_filename=session.get("pfp_filename", ""))

    else:
        return redirect(url_for("prihlaseni"))

# --- Explore ---

@app.route('/explore')
def explore():
    songs = get_data("SONGS")
    albums = get_data("ALBUMS")
    return render_template("explore.html", albums=albums, songs=songs)

@app.route("/album/<album_id>")
def albums(album_id):
    albums = get_data("ALBUMS")
    songs = get_data("SONGS")
    user = session["uzivatel"]
    playlists = get_data("PLAYLISTS")

    #tohle projede alba aby to našlo to id
    album = next((album for album in albums if album['album_id'] == album_id), None)

    if album == None:
        return render_template("404.html") 

    return render_template("album.html", album=album, songs=songs, user=user, playlists=playlists)

# --- Library ---

@app.route('/library')
def library():
    if "uzivatel" in session:
        user = session["uzivatel"]
        playlists = get_data("PLAYLISTS")
        return render_template("library.html", user=user, playlists=playlists)
    else:
        return redirect(url_for("prihlaseni"))

@app.route("/playlist/<playlist_id>")
def playlists(playlist_id):
    playlists = get_data("PLAYLISTS")
    songs = get_data("SONGS")
    playlist_songs = get_data("PLAYLIST_SONG")
    user = session["uzivatel"]
    
    #tohle projede playlisty aby to našlo to id
    playlist = next((playlist for playlist in playlists if playlist['id'] == playlist_id), None)

    songs_in_playlist = [song['song_id'] for song in playlist_songs if song['playlist_id'] == playlist['id']]

    if playlist == None:
        return render_template("404.html") 
    
    return render_template("playlist.html", playlist=playlist, user=user, songs=songs, playlists=playlists, songs_in_playlist=songs_in_playlist)

@app.route('/add-to-playlist', methods=["POST"])
def add_to_playlist():
    playlist_id = request.form.get("playlist")
    song_id = request.form.get("song")

    playlists = get_data("PLAYLISTS")

    insert_song_to_playlist(playlist_id, song_id)

    for playlist in playlists:
        if playlist.get("playlist_id") == playlist_id:
            playlist["songs"].append(song_id)
            break

    with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/playlists.json'), 'w') as file:
        json.dump(playlists, file, indent=2)

    return redirect(request.referrer)

@app.route('/zpracuj-playlist', methods=["POST"])
def zpracuj_playlist():
    name = request.form.get("name")
    author = session.get("uzivatel")
    description = request.form.get("description")

    playlist_id = generate_id()

    playlistfile = request.files["playlistfile"]
    if playlistfile.filename.endswith((".png", ".jpg",".jpeg")):
        image = upload_image(playlistfile, playlist_id, "playlist")
    else:
        image = "1_h26EkMgjuLXFqwe_fMh7goQH2zDL2Ff"

    if name == "" or name.isspace():
        name = author + "'s playlist"

    file = f"https://lh3.googleusercontent.com/d/{image}"

    new_playlist = {
    "playlist_id": playlist_id,
    "author": author,
    "name": name,
    "description": description,
    "playlistfile": file,
    "drive_id": image,
    "songs": []
    }

    insert_playlist(playlist_id, author, name, description, file, image)
    zapis_do_json("BACKUP/playlists", new_playlist)

    return redirect(url_for("library"))

@app.route('/update-playlist', methods=["POST"])
def update_playlist():
    playlist_id = request.form.get("playlist")
    name = request.form.get("name")
    author = session.get("uzivatel")
    description = request.form.get("description")

    playlistfile = request.files["playlistfile"]


    if name == "" or name.isspace():
        name = author + "'s playlist"

    playlists = get_data("PLAYLISTS")

    for playlist in playlists:
        if playlist.get("id") == playlist_id:
            new_name = name
            new_description = description
            if playlistfile.filename.endswith((".png", ".jpg",".jpeg")):
                if playlist["drive_id"] != "1_h26EkMgjuLXFqwe_fMh7goQH2zDL2Ff":
                    try:
                        delete_file(playlist["drive_id"])
                    except HttpError as error:
                        if error.resp.status == 404:
                            pass
                        if error.resp.status == 403:
                            pass
                        else:
                            raise
                image = upload_image(playlistfile, playlist_id, "playlist")
                new_file = f"https://lh3.googleusercontent.com/d/{image}"
                new_drive_id = image
            else:
                new_file = playlist["playlistfile"]
                new_drive_id = playlist["drive_id"]
            insert_updated_playlist(new_name, new_description, new_file, new_drive_id, playlist_id)
            break

    with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/playlists.json'), 'w') as file:
        json.dump(playlists, file, indent=2)

    return redirect(request.referrer)

@app.route('/del-playlist', methods=["POST"])
def del_playlist():
    id = request.args.get("id")

    playlists = get_data("PLAYLISTS")
    delete_playlist(id)

    updated_playlists = [playlist for playlist in playlists if playlist.get("id") != id]

    for playlist in playlists:
        if "id" in playlist and playlist["id"] == id:
            drive_id = playlist.get("drive_id")
            if drive_id:
                try:
                    delete_file(drive_id)
                except HttpError as error:
                    if error.resp.status == 403:
                        pass
                    else:
                        raise


            with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/playlists.json'), 'w') as file:
                json.dump(updated_playlists, file, indent=2)
            break

    return redirect(url_for("library"))

# --- Song Manager ---

@app.route('/manage-song')
def manage_song():
    if "uzivatel" in session:
        role = session["role"]
    
        if role == "admin":
            albums = get_data("ALBUMS")
            albums = sorted(albums, key=lambda x: x["title"])
            songs = get_data("SONGS")
            songs = sorted(songs, key=lambda x: x["title"])
            return render_template("add_music.html", albums=albums, songs=songs)
        
    else:
        return redirect(url_for("index"))

@app.route('/zpracuj-song', methods=["POST"])
def zpracuj_song():
    title = request.form.get("title")
    author = request.form.get("author")
    album = request.form.get("album")

    songs = get_data("SONGS")
    for u in songs:
        if u ["title"] == title:
            return redirect(url_for("index"))

    songfile = request.files["songfile"]
    if songfile.filename.endswith(".mp3"):
        song_id = generate_id()
        
        song = upload_song(songfile, song_id)
        songfile_url = f"https://drive.google.com/uc?export=download&id={song}"

        new_song = {
        "song_id": song_id,
        "title": title,
        "author": author,
        "album": album,
        "songfile": f"https://drive.google.com/uc?export=download&id={song}",
        "drive_id": song
    }
        insert_song(song_id, title, author, album, songfile_url, song)
        zapis_do_json("BACKUP/songs", new_song)

        return redirect(url_for("explore"))
    else:
        return redirect(url_for("manage_song"))
    
@app.route('/del-song', methods=["POST"])
def del_song():
    id = request.form.get("id")

    songs = get_data("SONGS")
    delete_song(id)

    updated_songs = [song for song in songs if song.get("song_id") != id]

    for song in songs:
        if "song_id" in song and song["song_id"] == id:
            songfile = os.path.join(app.config['UPLOAD_FOLDER'] + "/BACKUP/songs", song.get('songfile', ''))
            if os.path.exists(songfile):
                os.remove(songfile)

            drive_id = song.get("drive_id")
            if drive_id:
                try:
                    delete_file(drive_id)
                except HttpError as error:
                    if error.resp.status == 403:
                        pass
                    else:
                        raise


            with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/songs.json'), 'w') as file:
                json.dump(updated_songs, file, indent=2)
            break

    return redirect(url_for("explore"))

@app.route('/zpracuj-album', methods=["POST"])
def zpracuj_album():
    title = request.form.get("title")
    author = request.form.get("author")
    release = request.form.get("release")

    albums = get_data("ALBUMS")
    for u in albums:
        if u ["title"] == title:
            return redirect(url_for("index"))

    albumfile = request.files["albumfile"]
    if albumfile.filename.endswith((".png", ".jpg",".jpeg")):
        album_id = generate_id()
        
        image = upload_image(albumfile, album_id, "album")
        file = f"https://lh3.googleusercontent.com/d/{image}"

        new_album = {
        "album_id": album_id,
        "title": title,
        "author": author,
        "release": release,
        "albumfile": file,
        "drive_id": image
    }
        
        insert_album(album_id, title, author, release, file, image)
        zapis_do_json("BACKUP/albums", new_album)

        return redirect(url_for("explore"))
    else:
        return redirect(url_for("manage_song"))
    
@app.route('/del-album', methods=["POST"])
def del_album():
    id = request.form.get("id")

    songs = get_data("SONGS")
    albums = get_data("ALBUMS")

    delete_album(id)

    updated_songs = [song for song in songs if song.get("album") != id]
    updated_albums = [album for album in albums if album.get("album_id") != id]

    for album in albums:
        if "album_id" in album and album["album_id"] == id:
                albumfile = os.path.join(app.config['UPLOAD_FOLDER'] + "/BACKUP/albums", album.get('albumfile', ''))
                if os.path.exists(albumfile):
                    os.remove(albumfile)

                drive_id = album.get("drive_id")
                if drive_id:
                    try:
                        delete_file(drive_id)
                    except HttpError as error:
                        if error.resp.status == 404:
                            pass
                        if error.resp.status == 403:
                            pass
                        else:
                            raise


                with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/albums.json'), 'w') as file:
                    json.dump(updated_albums, file, indent=2)
                break
        for song in songs:
            if "album" in song and song["album"] == id:
                songfile = os.path.join(app.config['UPLOAD_FOLDER'] + "/BACKUP/songs", song.get('songfile', ''))
                if os.path.exists(songfile):
                    os.remove(songfile)

                drive_id_song = song.get("drive_id")
                if drive_id_song:
                    try:
                        delete_file(drive_id_song)
                    except HttpError as error:
                        if error.resp.status == 404:
                            pass
                        if error.resp.status == 403:
                            pass
                        else:
                            raise

                with open(os.path.join(UPLOAD_FOLDER, 'BACKUP/songs.json'), 'w') as file:
                    json.dump(updated_songs, file, indent=2)
                break

    return redirect(url_for("explore"))

# --- Login ---

@app.route('/register', methods=["POST", "GET"])
def registrace():
    if "uzivatel" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        id = generate_id()
        isArtist = request.form.get("isArtist")

        if isArtist == "on":
            role = "artist"
        else:
            role = "user"

        uzivatele = precti_json("users")
        for u in uzivatele:
            if u["email"] == email:
                return redirect(url_for("prihlaseni"))

        novy_uzivatel = {
            "username": username,
            "email": email,
            "password": password,
            "id": id,
            "role": role
        }
        zapis_do_json("users", novy_uzivatel)
        return redirect(url_for("prihlaseni"))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def prihlaseni():
    if "uzivatel" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username_or_email = request.form.get("username_or_email")
        password = request.form.get("password")

        uzivatele = precti_json("users")
        for u in uzivatele:
            if u["username"] == username_or_email or u["email"] == username_or_email and u["password"] == password:
                session["uzivatel"] = u["username"]
                session["role"] = u["role"]
                return redirect(url_for("profile"))

        return render_template("login_test.html", error="Neplatné uživatelské jméno nebo heslo")

    return render_template("login_test.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "uzivatel" in session:
        session.pop("uzivatel", None)
        session.pop("role", None)
    return redirect(url_for("index"))


@app.route("/password-reset")
def password_reset():
    return render_template("passwordreset.html")


@app.route("/profile/feedback", methods=["POST", "GET"])
def feedback():
    return render_template("feedback.html")

if __name__ == "__main__":
    app.run(debug=True)