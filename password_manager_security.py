import hashlib
import os
import json
from encryption_handler import encrypt_data , decrypt_data
#password hashing function
def hash_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

#functions for checking if there is a master password or not by checking if there is a json file named master.json
def load_master_password():
    if not os.path.exists("master.json"):
        return None
    
    try:
        with open("master.json" , "r") as f:
            data = json.load(f)
            return data.get("master")
    except:
        return None

#function to save the master password in the json file
def save_master_password(hashed):
    data = {"master" : hashed}
    with open("master.json" , "w") as f:
        json.dump(data , f)

Vault_file = "vault.json"

def load_password():
    if not os.path.exists(Vault_file):
        return []
    try:
        with open(Vault_file , "r") as f:
            return json.load(f)
    except:
        return []
    
def save_password(data):
    with open(Vault_file , "w") as f:
        json.dump(data,f,indent=4)

def save_vault(data , key):
    json_data=json.dumps(data)

    encrypted = encrypt_data(key , json_data)

    with open("vault.enc" , "wb") as f:
        f.write(encrypted)

def load_vault(key):
    if not os.path.exists("vault.enc"):
        return []
    
    with open("vault.enc","rb") as f:
        encrypted = f.read()
    
    decrypted = decrypt_data(key,encrypted)

    return json.loads(decrypted)