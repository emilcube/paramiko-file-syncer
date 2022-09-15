# paramiko-file-syncer
Synchronization files using python (paramiko library) to sync files with folder in os Windows and Linux via SFTP

Programms sync files in two folders: local - "basePath1" and remote - "basePath2" every "sleep_time" seconds.
Note: programm sync only files (without sync directories)
Synchronization is being done by copying files.

# settings:
sleep_time = 20 # parameter of periodic synchronizations - sync every 20 secs
basePath1 = "local_path",
basePath2 = "remote_path"

Change remote server settings (in function get_sftp_instance):
host,
port,
password,
username
