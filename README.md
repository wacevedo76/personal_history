This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright 2024 William Acevedo


# PERSONAL HISTORY

## Goals
PERSONAL HISTORY is way to quickly and easily journal all personal human activity
that adds verification to all entries.

## Rational
Now you may be wondering, why would anyone ever want to do this.
Other questions and concerns regarding privacy, ethics, and public safty arise. 

Setting these concerns aside for a moment, let me supply some, for what many may
agree is (or should be) a fundamental right of any human being:

* The Right to Free Speach

Many will argue that all speech should not be free, However, there is
particularly one aspect of Free Speech the I would like to focus on:

* That aspect is the Freedom to Share

This Freedom is not being attacted by any government, but by technology.
It is so easy the manipulate video, audio, using modern software, not even 
mentioning text, because mass text manipulation tools have existed not shortly 
after the invention of the microcontroller (not sure, maybe even earlier) but 
now have become even tools a lay person can use.

We now have the technology to map the human face digitally, and use this 
digital information to replicate that person's likeness virtually, on still image and
in video. Grant it, the technology is in its early stages, but with the rise
more powerful machines, and software development, and Artificial Intelligence 
it will no doubt improve exponetially relativly quickly.

There needs to be a quick, effortless, and most importantly, a method 
to what I term "Irrifutable Verification" of tracking aspects of life.

Bind to this need is the Right To Share. 

## The Right To Share

All People like to share. 

How many of us have any sort of social media account?
And even if you don't, have you never shown a photo album of any kind to
another person? Or shared a story? To any other human? Ever?

We all like to share. The motivations behind, or the countless other implications
suggested by this statement aside for a moment, and realize that it is the rare
human who has lived to maturity and never shared a photo, a memory, or story 
or a moment which they found memorable.

Couple with the Right to Free Speech, which includes the right not to be compelled 
to say anything.

## What is Personal History?

The Personal History file is simply a data file where you can quickly record, and
effotlessly save whatever it is you want to share, in a file which you 
completely own. Every set of shared data is then used in conjunction with 
other unique data to generate a hash key that is unique and directly tide 
the data you shared.

If the data is changed or manipuated in any way, the generated key will not only 
not match coresponding data, but also compromising the integrity of all data 
entered thereafter.

The goal is to generate a file, which you keep, like a journal, that  
is secure and contains only data you choose to share.

This makes you, the individual, the owner of your data.

There are so many aspects of this, especially with modern Analytics tools, that
compelled me to start this project. However, the one aspect that excites me 
most is the idea that now, you can be the true owner of what your share
you control whatever narative you wish to project to the world, verifiably.

## Personal History Schema

Here is a rough idea of what the Personal History data file would look like:

```
{"profile": {
    "username": "wacevedo",
    "firstname": "William",
    "lastname": "Acevedo",
    "password": "encrypted_password"
  },
  "years": [
    {
      "year": 2023,
      "year_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
      "months": [
        {
          "month": 12,
          "month_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
          "days": [
            {
              "date": 09,
              "day_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
              "habits": {
                "pushups": {
                  "pushups-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "100"
                },
                "pilaties": {
                  "pilaties-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "wallsits": {
                  "wallsits-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "sqats": {
                  "sqats-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "20"
                },
                "meditation": {
                  "meditation-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "sharable": "true",
                  "completed": "1"
                }
              }
            },
            {
              "date": 08,
              "day_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
              "habits": {
                "pushups": {
                  "pushups-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "100"
                },
                "pilaties": {
                  "pilaties-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "wallsits": {
                  "wallsits-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "sqats": {
                  "sqats-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "20"
                },
                "meditation": {
                  "meditation-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "sharable": "true",
                  "completed": "1"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## How It works:
    Whenever a new Personal History file is created it will generate:
    * A data Set containing:
      * First name, Last name, date, and time
      * two hashed values representing two pieces of unique and private Personal identifying information (e.g., taxid, password)

```
example in python:
    -- example values:

    firstname = "herman", 
    lastname = "munster", 
    tax_id = "8765309", 
    password = "123456789"

    -- example output of function used to generate desired output:
    generate_priliminary_hash_values(firstname, lastname, tax_id, password)
    
    output:
    There are two sets of data created:
    ..* the date and time this data was created, and the first and last name in clear text.
    ..* Hashes created from the firstname, lastname

    [
        {'encoded_creation_time': '1710540432.688816', <- epoch time number converts to 15/03/2024 23:07
         'firstname': 'herman',
         'lastname': 'munster'},

        {'hashed_creation_time': '7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6',
        'hashed_tax_id': '5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919',         
        'hashed_password': '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225',
        'hashed_firstname': '3bf39bf3fe465c0600105b3451f274fa9f05b3c706f022608c0fb28285fe5cbf',
        'hashed_lastname': '7cbd75a33e3f9ceba58eab97dd18cd7866d398f3d56542d64e80a369a36dadab'}
    ]
```

to reiterate:
* The data creation time (epoch) is 1710540432.688816, which converts to 15/03/2024 23:07 **equals** 7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6
* If any part of the date or time is changed, in any form, the original hash number will not match.
* This process of verification can be done with any, and all forms of data (text, images, video, audio)
    
### This data set is saved within the Personal History File, and then this data is used to generate the file name and used as the first hash which identifies the current year.

    '''
    example in python code:

    '''

