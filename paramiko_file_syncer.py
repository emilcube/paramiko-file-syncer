import paramiko
import os
from os import walk
import time
from stat import S_ISDIR, S_ISREG
from datetime import datetime

sleep_time = 20
basePath1 = "local_path"
basePath2 = "remote_path"

def get_sftp_instance():
    host = "144.144.144.144"
    port = 22
    password = "abc"
    username = "abc"
    IsNotCorrect = False
    for i in range(60):
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            IsNotCorrect = True
            break
        except Exception as e:
            print("get_sftp_instance error", datetime.now())
            time.sleep(i) # i max 60 -> summ sleep is 1830 sec
    if not IsNotCorrect:
        print("IsNotCorrect error", datetime.now())
        exit(666)
    else:
        print("Connected successful", datetime.now())
    return sftp

if __name__ == '__main__':
    print(f"Sync started with sleep_time={sleep_time}", datetime.now())
    sftp = get_sftp_instance()
    d1 = {}
    d2 = {}
    while True:
        try:
            filenames1 = set(next(walk(basePath1), (None, None, []))[2])
            filenames2 = set()  # sftp.listdir(basePath2) #'/home/ubuntu/Test')

            for entry in sftp.listdir_attr(basePath2):
                mode = entry.st_mode
                if S_ISREG(mode):
                    filenames2.add(entry.filename)

            if filenames1 != filenames2: # If new file is created in either server
                s1 = filenames1 - filenames2
                s2 = filenames2 - filenames1
                for s in s1:
                    sftp.put(basePath1 + s, basePath2 + s)
                for s in s2:
                    sftp.get(basePath2 + s,basePath1 + s)
                filenames1 = set(next(walk(basePath1), (None, None, []))[2])
                filenames2 = set()
                for entry in sftp.listdir_attr(basePath2):
                    mode = entry.st_mode
                    if S_ISREG(mode):
                        filenames2.add(entry.filename)
            elif (d1 != d2): # If any file is updated
                for key in d1:
                    if d1[key] == d2[key]:
                        pass
                    elif d1[key] < d2[key]:
                        sftp.get(basePath2 + key, basePath1 + key)
                    else:
                        sftp.put(basePath1 + key, basePath2 + key)

            s1 = filenames1 - filenames2
            s2 = filenames2 - filenames1
            for f in filenames1:
                tmp = os.path.getsize(basePath1 + f)
                d1[f] = tmp
            for f in filenames2:
                tmp = sftp.stat(basePath2 + f).st_size
                d2[f] = tmp
            #print("sleep")
            time.sleep(sleep_time)
        except Exception as e:
            print("Error", datetime.now())
            sftp = get_sftp_instance()
            d1 = {}
            d2 = {}
            continue
    print("Everething is really bad", datetime.now())


