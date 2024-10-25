import os
from datetime import datetime
from pathlib import Path
import hashlib
from typing import List, Dict
import sqlite3

# Helper functions

def generate_hash_values(
        firstname: str,
        lastname: str,
        tax_id: str,
        password: str) -> List:
    '''
    # The purpose and thought process behind this function is
    # that working with sensitive user data, specifically a value
    # similar to tax id and password is that that data should
    # be hashed before using sensitive personal user data in
    # all preceding functions

    # The Return value for this function is a list containing
    # the following values:
    #
    #    [
    #        {"encoded_creation_time": current_epoch_time_str,
    #         "firstname": firstname,
    #         "lastname": lastname},
    #        {"hashed_creation_time": hashed_epoch_time,
    #            "hashed_tax_id": hashed_tax_id,
    #            "hashed_password": hashed_password,
    #            "hashed_firstname": hashed_firstname,
    #            "hashed_lastname": hashed_lastname}
    #    ]
    '''
    def _hash_generator(raw_data):
        hashed_data = hashlib.sha256()
        hashed_data.update(raw_data.encode('utf-8'))
        data_hash = hashed_data.hexdigest()

        return data_hash

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

    # Generate filehash from the joined hashed values of:
    # hashed_firstname
    # hashed_lastname
    # hashed_epoch_time
    # hashed_tax_id
    # hashed_password
    userdata_hashes_string = ''.join(
        [hashed_firstname,
         hashed_lastname, 
         hashed_epoch_time,
         hashed_tax_id,
         hashed_password
        ]
    )
    filehash = _hash_generator(userdata_hashes_string)

    # Return a list of two dictionaries, the first with the creation time and names,
    # and the second with the hashed values
    return [
        {"creation_time": current_epoch_time_readable,
         "encoded_creation_time": current_epoch_time_str,
         "firstname": firstname,
         "lastname": lastname},
        {"hashed_firstname": hashed_firstname,
         "hashed_lastname": hashed_lastname,
         "hashed_creation_time": hashed_epoch_time,
         "hashed_tax_id": hashed_tax_id,
         "hashed_password": hashed_password,
         "userdata_hash": filehash}
    ]


def create_ph_hashed_day_file_name(userdata: List) -> str:
    '''This function goes about creating the name for the Personal History 
    Date (PHD) file name.
       The idea befind this function is:
         * to create the file name that is unique but easily 
           identifyable without including constantly changing data

       The rational behind this being that the create_ph_day_file stores
       the habits in a database prior to a sync.

       The term SYNC in this context being that manipulating collumns in
       a database is much easier and much more time efficient.
       collecting rows for a table and parsing the returnd data (being the
       entire table) into JSON, the giving us the data to sink with
       the Personal_Life Repository'''

    # Unpack userdata
    ph_owner_values, ph_owner_hashed_values = userdata[0], userdata[1]

    # Unpack values from ph_owner_values
    creation_time, encoded_creation_time, firstname, lastname = ph_owner_values.values()

    # Unpack values from ph_owner_hashed_values
    hashed_firstname, hashed_lastname, hashed_creation_time, hashed_tax_id, \
    hashed_password = ph_owner_hashed_values.values()

    # Generate hash from combined hash values of:
    #   * hashed_firstname
    #   * hashed_lastname
    #   * hashed_tax_id
    #   * hashed_creation_time

    # join all the hashed values into a single string
    # for the pupose of creating the very first hash value for the personal 
    # history file
    userdata_hash_value = ''.join(
        [hashed_firstname,
         hashed_lastname,
         hashed_tax_id,
         hashed_creation_time])

    init_file_name_hash = hashlib.sha256()
    file_name_hash.update(file_name_hash_str.encode('utf-8'))
    init_hashstring = file_name_hash.hexdigest()

    return filename


def create_file(filename: str, userdata: List, directory_path):
    """Create file  
        Args: 
            filename: The hashed filename generated by create_ph_hashed_day_file_name (1st argument).
            userdata: The list of hashes generated by generate_hash_values and passed into and outfrom create_ph_hashed_day_file_name (2nd argument)
            directory_path: Location to where the file is to be saved
            """
    # Verify that target directory exist
    dir_path = Path(directory_path)
    if dir_path.exists() and dir_path.is_dir():
        # Verify that the file within the path does not exist
        file_path = dir_path / filename
        if not file_path.exists():
            # This is the point at which an actual file is created it
            # and this being so, it is the place where default information
            # is added to the initial file creation.
            #
            # Proposal:
            # the file is created with all of the data generated from
            # generate_hash_values. which would alow verefication between
            # other iot devices.
            file_path.touch()
        else:
            print(f"{file_path} already exists")
    else:
        print(f"{dir_path} does not exists")
