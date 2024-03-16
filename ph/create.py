import os
import datetime
from pathlib import Path
import hashlib
from typing import List, Dict
import sqlite3


def generate_hash_values(
        firstname: str,
        lastname: str,
        tax_id: str,
        password: str) -> List:
    '''
    # The purpose and thought process behind this function is
    # that working with sensitive user data, specificly a value
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

    # Generate epoc time stamp for date_file_epoch used to
    # denote fi# Get the current datetime object
    current_datetime = datetime.datetime.now()
    current_epoch_time = str(current_datetime.timestamp())
    current_epoch_time_str = str(current_epoch_time)
    encoded_current_datetime = current_epoch_time.encode('utf-8')
    encoded_epoch_time_hash = hashlib.sha256()
    encoded_epoch_time_hash.update(encoded_current_datetime)
    hashed_epoch_time = encoded_epoch_time_hash.hexdigest()

    # Generate a sha256 for the tax_id
    encoded_tax_id_hash = hashlib.sha256()
    encoded_tax_id_hash.update(tax_id.encode('utf-8'))
    hashed_tax_id = encoded_tax_id_hash.hexdigest()

    # Generate a sha256 for the password
    encoded_password_hash = hashlib.sha256()
    encoded_password_hash.update(password.encode('utf-8'))
    hashed_password = encoded_password_hash.hexdigest()

    # Generate a sha256 for firstname
    encoded_firstname_hash = hashlib.sha256()
    encoded_firstname_hash.update(firstname.encode('utf-8'))
    hashed_firstname = encoded_firstname_hash.hexdigest()

    # Generate a sha256 for lastname
    encoded_lastname_hash = hashlib.sha256()
    encoded_lastname_hash.update(lastname.encode('utf-8'))
    hashed_lastname = encoded_lastname_hash.hexdigest()

    # Return a list of two dictionaries, the first with the creation time Name,
    # and the second one containing the filename creation time, and the hashed
    #  values from firstname, lastname
    return [
        {"encoded_creation_time": current_epoch_time_str,
         "firstname": firstname,
         "lastname": lastname},
        {"hashed_creation_time": hashed_epoch_time,
            "hashed_tax_id": hashed_tax_id,
            "hashed_password": hashed_password,
            "hashed_firstname": hashed_firstname,
            "hashed_lastname": hashed_lastname}
    ]


def create_ph_hashed_day_file_name(userdata: List) -> List:
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
    encoded_creation_time, firstname, lastname = ph_owner_values.values()

    # Unpack values from ph_owner_hashed_values
    hashed_creation_time, hashed_tax_id, hashed_password, \
        hashed_firstname, hashed_lastname = ph_owner_hashed_values.values()

    # Generate hash from combined hash values of:
    #   * hashed_firstname
    #   * hashed_lastname
    #   * hashed_tax_id
    #   * hashed_creation_time

    # join all the hashed values into a single strim
    file_name_hash_str = ''.join(
        [hashed_firstname,
         hashed_lastname,
         hashed_tax_id,
         hashed_creation_time])

    file_name_hash = hashlib.sha256()
    file_name_hash.update(file_name_hash_str.encode('utf-8'))
    filename = file_name_hash.hexdigest()

    return [filename, userdata]


def create_file(filename: str, userdata: List):
    pass
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
