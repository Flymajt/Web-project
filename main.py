from flask import Flask, request, render_template, redirect, session, url_for, make_response
import os
import json

app = Flask (__name__)
app.config["SECRET_KEY"] = "123456789"


def zapis_do_json(nazev_souboru, data_na_zapis):
    aktivni_soubor = os.path.dirname(__file__)
    SITE_ROOT = os.path.realpath(aktivni_soubor)
    json_url = os.path.join(SITE_ROOT, "static/data", f"{nazev_souboru}.json")
    UZIVATELE = json.load(open(json_url,"r",encoding="utf-8"))
    UZIVATELE.append(data_na_zapis)
    with open(json_url, "w", encoding="utf-8") as outline:
        json.dump(UZIVATELE, outline)

    return


@app.route('/')
def rozcestnik():
    if "username" in session:
        return redirect(url_for("zobraz_ucet"))
    return redirect(url_for("prihlaseni"))


@app.route('/registrace')
def registrace():
    return render_template("registrace.html")

@app.route('/zpracuj-registraci', methods=["POST"])
def zpracuj_registraci():
    username = request.form.get("username")
    password = request.form.get("password")

    uzivatele = precti_json("users")
    for u in uzivatele:
        if u ["username"] == username:
            return redirect(url_for("prihlaseni"))
        
    novy_uzivatel ={
        "username": username,
        "password": password,
    }
    zapis_do_json("users", novy_uzivatel)

    return redirect(url_for("prihlaseni"))



