# pip install mysql-connector
import mysql.connector

def get_connected():
    return mysql.connector.connect(
        host="db4free.net",
        user="toneyadmin",
        password="qW4rVG58i",
        database="toneysql"
    )

mydb = get_connected() 
mydb.autocommit = True # to znamená že data budou furt aktualizovaný
mycursor = mydb.cursor(dictionary=True) # dictionary=True dělá že v html se to furt může udávat jako např {{ album.albumfile }}

def get_data(table):
    sql = f"SELECT * FROM {table}"
    mycursor.execute(sql)
    return mycursor.fetchall()



def insert_song(id, title, author, album, file, drive_id):
    sql = """
    INSERT INTO SONGS (id, title, author, album, songfile, drive_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """ # %s znamená basically že tam půjde nějaká věc (id, title, author, etc etc)

    data = (id, title, author, album, file, drive_id)
    mycursor.execute(sql, data) # vezme to sql a do těch %s dá data
    mydb.commit()

def delete_song(id):
    sql = """DELETE FROM PLAYLIST_SONG WHERE song_id = %s"""
    mycursor.execute(sql, (id,)) 
    sql = """DELETE FROM SONGS WHERE id = %s"""
    mycursor.execute(sql, (id,)) 
    mydb.commit()


def insert_album(id, title, author, release, file, drive_id):
    sql = """
    INSERT INTO ALBUMS (album_id, title, author, release_date, albumfile, drive_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = (id, title, author, release, file, drive_id)
    mycursor.execute(sql, data) 
    mydb.commit()

def delete_album(album_id):
    sql = """SELECT id FROM SONGS
    WHERE album = %s"""
    mycursor.execute(sql, (album_id,)) 
    myresult = mycursor.fetchall()
    for row in myresult:
        id = row["id"] # tady se to musí brát taktoč jelikož je to dictionary (dictionary=True)
        sql = """DELETE FROM PLAYLIST_SONG WHERE song_id = %s"""
        mycursor.execute(sql, (id,)) 
        sql = """DELETE FROM SONGS WHERE id = %s"""
        mycursor.execute(sql, (id,)) 
    sql = """DELETE FROM ALBUMS WHERE album_id = %s"""
    mycursor.execute(sql, (album_id,)) 
    mydb.commit()



def insert_playlist(id, author, name, description, file, drive_id):
    sql = """
    INSERT INTO PLAYLISTS (id, author, name, description, playlistfile, drive_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = (id, author, name, description, file, drive_id)
    mycursor.execute(sql, data) 
    mydb.commit()

def insert_updated_playlist(name, description, file, drive_id, id):
    sql = """
    UPDATE PLAYLISTS
    SET name = %s, description = %s, playlistfile = %s, drive_id = %s
    WHERE id = %s
    """

    data = (name, description, file, drive_id, id)
    mycursor.execute(sql, data) 
    mydb.commit()

def insert_song_to_playlist(playlist_id, song_id, placement):
    sql = """
    INSERT INTO PLAYLIST_SONG (playlist_id, song_id, song_playlist_placement)
    VALUES (%s, %s, %s)
    """

    data = (playlist_id, song_id, placement)
    mycursor.execute(sql, data)
    mydb.commit()

def delete_playlist(id):
    sql = """DELETE FROM PLAYLIST_SONG WHERE playlist_id = %s"""
    mycursor.execute(sql, (id,)) 
    sql = """DELETE FROM PLAYLISTS WHERE id = %s"""
    mycursor.execute(sql, (id,)) 
    mydb.commit()

def insert_chat(id, user, user2):
    sql = """
    INSERT INTO CHATS (id, user, user2)
    VALUES (%s, %s, %s)
    """

    data = (id, user, user2)
    mycursor.execute(sql, data)
    mydb.commit()

def create_individual_chat(name):
    sql = f"""
    CREATE TABLE {name} (
        id int PRIMARY KEY,
        content VARCHAR(255),
        sender VARCHAR(255)
    )
    """
    mycursor.execute(sql)
    mydb.commit()

def send_chat(id, content, sender, chat_id):
    sql = f"""
    INSERT INTO {chat_id} (id, content, sender)
    VALUES (%s, %s, %s)
    """

    data = (id, content, sender)
    mycursor.execute(sql, data)
    mydb.commit()