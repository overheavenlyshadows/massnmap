# Description

Massnmap is the wrapper for masscan and nmap scripts. Massnmap makes scan using masscan on inputed target and gets output with IP:Ports pairs. Then, nmap runs on discovered services with inputed args. ez pezy.


## Usage

### Using Script

```
sudo masscan <IP/Subnet> <masscan args> --nm <nmap args>
```

### Using Docker

```
docker build -t massnmap .  

docker run massnmap <IP/Subnet> <masscan args> --nm <nmap args>
```

## Important

**❗️Root required**

**❗️Do not use Masscan/Nmap output args!!!**

**❗️For saving results use linux output redirection**



## Problems

❗️Script do not support input args for masscan (hope i will fix it for flexibility)

❗️Sometimes nmap has no result for host which has ports. Have no idea why, hope will fix it.
