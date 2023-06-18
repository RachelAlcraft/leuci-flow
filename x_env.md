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
https://github.com/almarklein/pyelastix/issues/18
On Linux, one needs to set ELASTIX_PATH to full path to elastix binary (.../elastix-4.9.0-linux/bin/elastix).
Also, the distributed libraries must be available from the common locations (e.g. /usr/lib). Alternatively, set/add to LD_LIBRARY_PATH the path to lib directory of elastix (.../elastix-4.9.0-linux/lib/).

```
export ELASTIX_PATH=~/phd/leuci-async/leuci-flow/bin/elastix-5.1.0-linux/bin/elastix
export LD_LIBRARY_PATH=~/phd/leuci-async/leuci-flow/bin/elastix-5.1.0-linux/lib
export PATH etc to bashrc
source ~/.bashrc
```