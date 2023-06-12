# Virtual Machines or Clusters

## Azure virtual machine
leuci-flow on azure
```
ssh -i ~/.ssh/rae-flow.pem ralcraft@52.157.153.72
```

## Create an ssh key for gothub if you need to
•   mkdir .ssh
•   cd .ssh
•   ssh-keygen
•   (press enter all 3 times without typing anything)
•   cat id_rsa.pub
•   You can now copy this file
•   go to your github website login page
•   In your Settings/SSH and GPG keys, create one and paste it in

```
git clone git@github.com:RachelAlcraft/leuci-flow.git
```