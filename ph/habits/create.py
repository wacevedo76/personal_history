import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict
from . import config

def generate_hash_values(
        firstname: str,
        lastname: str,
        tax_id: str,
        password: str) -> Dict:
    """
    The purpose and thought process behind this function is
    that working with sensitive user data, specifically a value
    similar to tax id and password is that that data should
    be hashed before using sensitive personal user data in
    all preceding functions

    The Return value for this function is a dictionary containing
    the following key/value pairs:
    {
        "user_data":
            {"creation_time": current_epoch_time_readable,
             "epoch_time": current_epoch_time_str,
             "firstname": firstname,
             "lastname": lastname},
        "user_hashes":
            {"hashed_firstname": hashed_firstname,
             "hashed_lastname": hashed_lastname,
             "hashed_creation_time": hashed_epoch_time,
             "hashed_tax_id": hashed_tax_id,
             "hashed_password": hashed_password,
             "userdata_hashes": filehash}
    }
    """

    """Helper function for generating hash strings"""
    def _hash_generator(raw_data):
        hashed_data = hashlib.sha256()
        hashed_data.update(raw_data.encode('utf-8'))
        data_hash = hashed_data.hexdigest()

        return data_hash

    """Helper function for converting epoch time stamp to readable time"""
    def _certs(epochtime):    # (c)onvert (e)poch (t)o (r)readable (s)tring
        dtobj = datetime.fromtimestamp(epochtime)
        return dtobj.strftime("%A, %B, %d, %Y %H:%M:%S")


    # Get the current datetime object and convert epoch time to an integer (no decimal)
    current_datetime = datetime.now()
    current_epoch_time = int(current_datetime.timestamp())  # Convert to integer to remove decimal
    current_epoch_time_readable = _certs(current_epoch_time)
    current_epoch_time_str = str(current_epoch_time)
    hashed_epoch_time = _hash_generator(current_epoch_time_str)

    # Generate a sha256 hash for tax_id
    hashed_tax_id = _hash_generator(tax_id)

    # Generate a sha256 hash for password
    hashed_password = _hash_generator(password)

    # Generate a sha256 hash for firstname
    hashed_firstname = _hash_generator(firstname)

    # Generate a sha256 hash for lastname
    hashed_lastname = _hash_generator(lastname)

    #  Generate filehash from the joined hashed values of:
    #    hashed_firstname
    #    hashed_lastname
    #    hashed_epoch_time
    #    hashed_tax_id
    #    hashed_password
    userdata_hashes_string = ''.join(
        [hashed_firstname,
         hashed_lastname, 
         hashed_epoch_time,
         hashed_tax_id,
         hashed_password
        ]
    )
    userdata_hash = _hash_generator(userdata_hashes_string)

    # Return a list of two dictionaries, the first with the creation time and names,
    # and the second with the hashed values
    return {
        "user_data":
            {"creation_time": current_epoch_time_readable,
             "epoch_time": current_epoch_time_str,
             "firstname": firstname,
             "lastname": lastname},
        "user_hashes":
            {"hashed_firstname": hashed_firstname,
             "hashed_lastname": hashed_lastname,
             "hashed_creation_time": hashed_epoch_time,
             "hashed_tax_id": hashed_tax_id,
             "hashed_password": hashed_password,
             "userdata_hash": userdata_hash}
    }


def create_ph_filename(userdata: Dict) -> Dict:
    """This function goes about creating the name for the Personal History 
       Date (PHD) file name.
       The idea befind this function is:
         * to create the file name that is unique but easily 
           identifyable without including constantly changing data

       The rational behind this being that the create_ph_filename stores
       the habits in a database prior to a sync.

       The term SYNC in this context being that manipulating collumns in
       a database is much easier and much more time efficient.
       collecting rows for a table and parsing the returnd data (being the
       entire table) into JSON, the giving us the data to sink with
       the Personal_Life Repository

       the Return value for create_ph_filename:

       {
         "user_raw_data": {
             "creation_time": creation_time,
             "epoch_time": epoch_time,
             "firstname": firstname,
             "lastname": lastname,
         },
         "user_hashes": {
             "hashed_firstname": hashed_firstname,
             "hashed_lastname": hashed_lastname,
             "hashed_creation_time": hashed_creation_time,
             "hashed_tax_id": hashed_tax_id,
             "hashed_password": hashed_password,
             "userdata_hash": userdata_hash
         },
         "filename": filename
       }
    """

    # Unpack userdata
    ph_owner_values, ph_owner_hashed_values = userdata["user_data"], userdata["user_hashes"]

    # Unpack values from ph_owner_values
    creation_time, epoch_time, firstname, lastname = ph_owner_values.values()

    # Unpack values from ph_owner_hashed_values
    hashed_firstname, hashed_lastname, hashed_creation_time, hashed_tax_id, \
    hashed_password, userdata_hash = ph_owner_hashed_values.values()

    # Create filename from:
    #    <firstname>_<lastname>-<epoch_time>
    filename = ''.join([firstname, '_', lastname, '-', epoch_time])

    return {
        "user_raw_data": {
            "creation_time": creation_time,
            "epoch_time": epoch_time,
            "firstname": firstname,
            "lastname": lastname,
        },
        "user_hashes": {
            "hashed_firstname": hashed_firstname,
            "hashed_lastname": hashed_lastname,
            "hashed_creation_time": hashed_creation_time,
            "hashed_tax_id": hashed_tax_id,
            "hashed_password": hashed_password,
            "userdata_hash": userdata_hash
        },
        "filename": filename
    }


def create_file(userdata: Dict, directory_path=config.PY_FILE_LOCATION):
    """ Create file  
        Args:
            userdata - a dictionary containing three keys, containing various other dictionaries:
                ["user_raw_data"]:
                    - ["creation_time"]             -> String value for epoch time
                    - ["epoch_time"],               -> epoch time of data creation
                    - ["firstname"],                -> first name of created user
                    - ["lastname"]                  -> last name of created user
                ["user_hashes"]:
                    - ["hashed_firstname"],
                    - ["hashed_lastname"],
                    - ["hashed_creation_time"],
                    - ["hashed_tax_id"],
                    - ["hashed_password"],
                    - ["userdata_hash"]
                ["filename"]
    """

    """Create file with user data if it doesn't already exist."""
    user_raw_data, user_hashes, filename = (
        userdata["user_raw_data"], 
        userdata["user_hashes"], 
        userdata["filename"]
    )

    # Ensure the directory exists
    target_dir = Path(directory_path)
    target_dir.mkdir(parents=True, exist_ok=True)

    # Add .json extension to filename
    file_path = target_dir / f"{filename}.json"

    if file_path.exists():
        print(f"Warning: {file_path} already exists. No file was created.")
        return None  # Or return some error/info if needed

    # Construct file data in specified order
    profile = {
        "epoch_time": user_raw_data["epoch_time"],
        "creation_time": user_raw_data["creation_time"],
        "firstname": user_raw_data["firstname"],
        "lastname": user_raw_data["lastname"],
        "hashed_firstname": user_hashes["hashed_firstname"],
        "hashed_lastname": user_hashes["hashed_lastname"],
        "hashed_creation_time": user_hashes["hashed_creation_time"],
        "hashed_tax_id": user_hashes["hashed_tax_id"],
        "hashed_password": user_hashes["hashed_password"],
        "userdata_hash": user_hashes["userdata_hash"]
    }

    file_data = {
        "profile": profile
    }

    # Write data to file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(file_data, f, indent=2)

    print(f"File created: {file_path}")
    return str(file_path)
