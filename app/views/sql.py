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

def insert_song_to_playlist(playlist_id, song_id):
    sql = """
    INSERT INTO PLAYLIST_SONG (playlist_id, song_id)
    VALUES (%s, %s)
    """

    data = (playlist_id, song_id)
    mycursor.execute(sql, data)
    mydb.commit()

