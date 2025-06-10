# pip install google-api-python-client
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static/data")
SCOPES = ["https://www.googleapis.com/auth/drive"] # basically, co to může dělat (tady to má přístup k google disku)
SERVICE_ACCOUNT_FILE = os.path.join(UPLOAD_FOLDER, "service_account.json")
SONG_FOLDER_ID = "1ddiGTzK0a6XyjzW_RLSepioo_6A3WfG1"
IMAGE_FOLDER_ID = "1-4rc3DS_Q05WNIXHsilNcBjzPN-R4G-D"
IMAGE_PLAYLIST_FOLDER_ID = "1US9Oj9a3yA971KlVvDnnKWJ1LG5oyGf5"
IMAGE_ALBUM_FOLDER_ID = "13n3Dt30QTdLON2q1MIdOYlHMilI4yhkC"
IMAGE_PFPS_FOLDER_ID = "1djsbfHCY_smgAYu-Q2XyCsFQlC7esmt7"

# basically přihlášení skrz přihlašovací údaje a co za má za práva
def auth():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return credentials

def upload_song(filepath, id):
    creds = auth()
    service = build("drive", "v3", credentials=creds)

    filedata = {
        "name": id,
        "parents": [SONG_FOLDER_ID],
        
    }

    media = MediaIoBaseUpload(filepath.stream, mimetype='audio/mpeg')

    file = service.files().create(
        body = filedata,
        media_body = media,
        fields = "id"
    ).execute()

    file_id = file.get("id")

    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"}
    ).execute() 

    song_id = file_id

    return song_id

def upload_image(filepath, id, type):
    creds = auth() # přístupové údaje
    service = build("drive", "v3", credentials=creds) # vytvoří api klienta

    # tady to jen zjišťuje jaký typ obrázku to má být
    if type == "playlist":
        path = [IMAGE_PLAYLIST_FOLDER_ID]
    elif type == "album":
        path = [IMAGE_ALBUM_FOLDER_ID]
    elif type == "pfp":
        path = [IMAGE_PFPS_FOLDER_ID]
    else:
        path = [IMAGE_FOLDER_ID]


    filedata = {
        "name": id, # jméno souboru
        "parents": path, # kam uložit
        
    }

    # basically co za typ souboru to nahraje, filepath.stream je obrázek co to vezme z toho formu na stránce
    media = MediaIoBaseUpload(filepath.stream, mimetype="image/png")

    # vytvoří soubor
    file = service.files().create(
        body = filedata,
        media_body = media,
        fields = "id" # prostě vrátí jen id, je to rychlejší
    ).execute()

    file_id = file.get("id") # sebere id souboru

    # udělá soubor veřejný, jinak by to nešlo zobrazovat
    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"}
    ).execute() 

    # id pro obrázek
    image_id = file_id

    return image_id

def delete_file(id):
    creds = auth()
    service = build("drive", "v3", credentials=creds)

    # asi nemusím vysvětlovat, ale just in case, tohle to smaže
    service.files().delete(
        fileId=id
    ).execute()
