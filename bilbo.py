import hashlib
import os

def hash_file(filename):
    """Calculate the SHA-256 hash of a file."""
    with open(filename, 'rb') as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

def get_file_hashes(path):
    """Get a dictionary of filenames and their hashes for all files in a directory."""
    file_hashes = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = hash_file(file_path)
    return file_hashes

def save_hashes(file_hashes, file_path):
    """Save the file hashes to a file."""
    with open(file_path, 'w') as f:
        for file, hash in file_hashes.items():
            f.write("{} {}\n".format(hash, file))

def main():
    path = "/path/to/server/files"
    hash_file = "/path/to/hashes.txt"

    file_hashes = get_file_hashes(path)
    save_hashes(file_hashes, hash_file)

if __name__ == '__main__':
    main()
