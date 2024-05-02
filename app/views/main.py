from flask import Flask, request, render_template, redirect, session, url_for, make_response
import os
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789"

def precti_json(nazev_souboru):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    UZIVATELE = json.load(open(json_url,"r",encoding="utf-8"))
    return UZIVATELE
def zapis_do_json(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    UZIVATELE = json.load(open(json_url,"r",encoding="utf-8"))
    UZIVATELE.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(UZIVATELE, outline)

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


@app.route('/')
def index():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("index.html")

@app.route('/social')
def social():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("Social.html")

@app.route('/profile')
def profile():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("profile.html")

@app.route('/explore')
def explore():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("explore.html")

@app.route('/library')
def library():
    #if "username" in session:
    #    return redirect(url_for("prihlaseni"))
    return render_template("library.html")


@app.route('/register')
def registrace():
    return render_template("register.html")

@app.route('/zpracuj-registraci', methods=["POST"])
def zpracuj_registraci():
    username = request.form.get("username")
    password = request.form.get("password")

    uzivatele = precti_json("users")
    for u in uzivatele:
        if u ["username"] == username:
            return redirect(url_for("prihlaseni"))
        
    novy_uzivatel = {
        "username": username,
        "password": password,
    }
    zapis_do_json("users", novy_uzivatel)

    return redirect(url_for("prihlaseni"))

@app.route("/zpracuj-prihlaseni", methods=["POST"])
def zpracuj_prihlaseni():
    username = request.form.get("username")
    password = request.form.get("password")

    uzivatele = precti_json("users")
    for u in uzivatele:
        if u["username"] == username:
            return redirect(url_for("profile"))
        return redirect(url_for("registrace"))

@app.route("/login")
def prihlaseni():
    username = request.form.get("username")
    password = request.form.get("password")

    uzivatele = precti_json("users")
    for u in uzivatele:
        if u["username"] == username:
            return render_template("profile.html")
        return render_template("login_test.html")

@app.route("/password-reset")
def password_reset():
    return render_template("passwordreset.html")


@app.route('/add-song')
def add_song():
    return render_template("add_music.html")

@app.route('/zpracuj-song', methods=["POST"])
def zpracuj_song():
    title = request.form.get("title")
    author = request.form.get("author")
    album = request.form.get("album")

    songs = precti_json_songs("songs")
    for u in songs:
        if u ["title"] == title:
            return redirect(url_for("index"))
        
    new_song = {
        "title": title,
        "author": author,
        "album": album
    }
    zapis_do_json_songs("songs", new_song)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

