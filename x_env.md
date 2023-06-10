# Creating and using a python environment

This is assuming use of linux or WSL in windows

## Create the environment by calling:
```
python3 -m venv .venv
```

## Activate the envirnment valling:
```
source .venv/bin/activate
```

## Update the envirnment - pip installs
```
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

## Adding to the envirnment

You can do a pip install as a one off if you want to try something, otehrwise add the library to the list and call the above pip install of the requirements.txt file. You can specify explicit versions of you need to.

## Check you python and next flow versions
```
nextflow -v
python --version
```