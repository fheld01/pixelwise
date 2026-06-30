# Self-Hosted Git Server
This document describes in detail, how I set up a self-hosted, 
SSH-based bare Git server on the prod VM as an alternative to GitHub,
hosting this PixelWise project on it. 
The procedure follows Pro Git, Chapter 4.4 (Chacon/Straub 2014).

### 1. Create dedicated git user on prod
```bash
sudo adduser --disabled-password --gecos "" git
```
No password login; access is handled via SSH key only

### 2. Create storage location
```bash
sudo mkdir -p /srv/git
sudo chown git:git /srv/git
```

### 3. Create the bare repository
```bash
sudo -u git git init --bare /srv/git/pixelwise.git
```

### 4. Grant SSH access
Since the git user has no password, its SSH access was set up via sudo.
The dev machine's public key (already present in produser's
`authorized_keys`) was copied into the git user's `~/.ssh`, and the
permissions were set so that only the owner can access them. This way
only dev can connect.

```bash
sudo mkdir -p /home/git/.ssh && sudo chmod 700 /home/git/.ssh
sudo cp /home/produser/.ssh/authorized_keys /home/git/.ssh/authorized_keys
sudo chown -R git:git /home/git/.ssh && sudo chmod 600 /home/git/.ssh/authorized_keys
```

### 5. push from dev
```bash
git remote add eigenserver git@192.168.56.11:/srv/git/pixelwise.git
git push eigenserver main
```

### 6. Verify with a clone
```bash
git clone git@192.168.56.11:/srv/git/pixelwise.git test-clone
```
Here a successful clone confirms that push and clone  against self-hosted server works

### Source
Chacon, S. & Straub, B. (2014). Pro Git (2nd ed.). Apress. 
https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server

