## Requirements

- Python 3.7+
- Installed Nmap and Masscan

## Description

Massnmap is the wrapper for masscan and nmap scripts. Massnmap makes scan using masscan on inputed target and gets output with IP:Ports pairs. Then, nmap runs on discovered services with inputed args. ez pezy.


## Usage

### Using Script

```
sudo masscan <IP/Subnet> <masscan args> --nm <nmap args>
sudo masscan -il file.txt <masscan args> --nm <nmap args>
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



## Version info
### v1.1.1
- Sorted output added (Now Python 3.7+ required)
### v1.1
- Target list input feature was added
- Some minor fixes
### v1.0
- Script added
