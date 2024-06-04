from flask import Flask, request, render_template, redirect, session, url_for, make_response, jsonify, abort
import os
import json

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/data")

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
        json.dump(USERS, outline)

    return

def precti_json_songs(nazev_souboru):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    SONGS = json.load(open(json_url,"r",encoding="utf-8"))
    return SONGS
def zapis_do_json_songs(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    SONGS = json.load(open(json_url,"r",encoding="utf-8"))
    SONGS.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(SONGS, outline)

    return

def precti_json_albums(nazev_souboru):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    ALBUMS = json.load(open(json_url,"r",encoding="utf-8"))
    return ALBUMS
def zapis_do_json_albums(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    ALBUMS = json.load(open(json_url,"r",encoding="utf-8"))
    ALBUMS.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(ALBUMS, outline)

    return

def vytvor_json(nazev_souboru):
    data_na_zapis = []
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data/chats", f"{nazev_souboru}.json")

    with open(json_url, 'w', encoding="utf-8") as outfile:
        json.dump(data_na_zapis, outfile)

    return

@app.route('/')
def index():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("index.html")

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
    
    filename = f'chats/chat_{number}'
    chats = precti_json(filename)

    return render_template("Chats.html", chats=chats)

@app.route("/posli_chat", methods=["POST"])
def posli_chat(chat):
    username = session.get("uzivatel")
    username2 = request.form.get("chat_person")

    filename = f'chats/chat_{chat}'

    post_id = 0

    posty = precti_json(filename)
    for p in posty:
        if p["code"] == post_id:
            post_id += 1

    novy_post = {
        "username": username,
        "content": username2,
        "code": post_id,
    }
    zapis_do_json("chats", novy_post)
    chat_json = "chat_"+str(post_id)
    vytvor_json(chat_json)
    # note to self: jde jich dysplaynout max 5 + ten hard coded
    return redirect(url_for("social"))

@app.route("/profile")
def profile():
    if "uzivatel" in session:
        jmeno = session["uzivatel"]
        return render_template("profile.html", jmeno=jmeno)
    else:
        return redirect(url_for("prihlaseni"))

@app.route('/explore')
def explore():
    songs = precti_json_songs("songs")
    albums = precti_json_albums("albums")
    return render_template("explore.html", albums=albums, songs=songs)

@app.route('/library')
def library():
    if "uzivatel" in session:
        jmeno = session["uzivatel"]
        return render_template("library.html", jmeno=jmeno)
    else:
        return redirect(url_for("prihlaseni"))


@app.route('/register', methods=["POST", "GET"])
def registrace():
    if "uzivatel" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        uzivatele = precti_json("users")
        for u in uzivatele:
            if u["email"] == email:
                return redirect(url_for("prihlaseni"))

        novy_uzivatel = {
            "username": username,
            "email": email,
            "password": password,
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
                return redirect(url_for("profile"))

        return render_template("login_test.html", error="Neplatné uživatelské jméno nebo heslo")

    return render_template("login_test.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "uzivatel" in session:
        session.pop("uzivatel", None)
    return redirect(url_for("index"))

@app.route("/password-reset")
def password_reset():
    return render_template("passwordreset.html")


@app.route('/add-song')
def add_song():
    if "uzivatel" in session:
        username = session["uzivatel"]
    
        if username == "admin":
            albums = precti_json_songs("albums")
            albums = sorted(albums, key=lambda x: x["title"])
            return render_template("add_music.html", albums=albums)
        
    else:
        return redirect(url_for("index"))

@app.route('/zpracuj-song', methods=["POST"])
def zpracuj_song():
    title = request.form.get("title")
    author = request.form.get("author")
    album = request.form.get("album")

    songs = precti_json_songs("songs")
    for u in songs:
        if u ["title"] == title:
            return redirect(url_for("index"))

    songfile = request.files["songfile"]
    if songfile.filename.endswith(".mp3"):
        songfile.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/songs", songfile.filename))
        
        new_song = {
        "title": title,
        "author": author,
        "album": album,
        "songfile": songfile.filename
    }
        zapis_do_json_songs("songs", new_song)

        return redirect(url_for("index"))
    else:
        return redirect(url_for("add_song"))

@app.route('/zpracuj-album', methods=["POST"])
def zpracuj_album():
    title = request.form.get("title")
    author = request.form.get("author")
    release = request.form.get("release")

    albums = precti_json_albums("albums")
    for u in albums:
        if u ["title"] == title:
            return redirect(url_for("index"))

    albumfile = request.files["albumfile"]
    if albumfile.filename.endswith((".png", ".jpg",".jpeg")):
        albumfile.save(os.path.join(app.config["UPLOAD_FOLDER"] + "/albums", albumfile.filename))
        
        new_album = {
        "title": title,
        "author": author,
        "release": release,
        "albumfile": albumfile.filename
    }
        zapis_do_json_albums("albums", new_album)

        return redirect(url_for("index"))
    else:
        return redirect(url_for("add_song"))

@app.route("/album/<int:index>")
def albums(index):
   albums = precti_json_albums("albums")
   songs = precti_json_songs("songs")
   if index not in range(len(albums)):
       return "Searched album has not been found", 404
   return render_template("album.html", album=albums[index], songs=songs)

    
if __name__ == "__main__":
    app.run(debug=True)