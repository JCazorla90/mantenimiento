import os
import hashlib
import paramiko
import zipfile

def hash_file(filename):
   h = hashlib.sha256()
   with open(filename,'rb') as file:
      chunk = 0
      while chunk != b'':
         chunk = file.read(1024)
         h.update(chunk)
   return h.hexdigest()

hash_dict = {}
for root, dirs, files in os.walk("/path/to/server/files"):
   for file in files:
      file_path = os.path.join(root, file)
      file_hash = hash_file(file_path)
      hash_dict[file_path] = file_hash

hash_file = "/path/to/hashes.txt"
if os.path.exists(hash_file):
   with open(hash_file, "r") as f:
      old_hashes = f.readlines()
   changed_files = []
   for line in old_hashes:
      file_path, old_hash = line.strip().split()
      if file_path in hash_dict:
         if hash_dict[file_path] != old_hash:
            changed_files.append(file_path)
   if changed_files:
      with open(hash_file, "w") as f:
         for file_path in hash_dict:
            f.write(f"{file_path} {hash_dict[file_path]}\n")
      report = "Changes detected in the following files:\n" + "\n".join(changed_files)
   else:
      with open(hash_file, "w") as f:
         for file_path in hash_dict:
            f.write(f"{file_path} {hash_dict[file_path]}\n")
      report = "No changes detected."
else:
   with open(hash_file, "w") as f:
      for file_path in hash_dict:
         f.write(f"{file_path} {hash_dict[file_path]}\n")
   report = "No previous hashes found. Hashes generated for the first time."

with zipfile.ZipFile("report.zip", "w") as zf:
   zf.writestr("report.txt", report.encode("utf-8"))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("hostname", username="username", password="password")
sftp = ssh.open_sftp()
sftp.put("report.zip", "/path/to/remote/folder/report.zip")
sftp.close()
