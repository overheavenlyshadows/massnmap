## Requirements

- Python 3.7+
- Installed Nmap and Masscan

## Description

Massnmap is the wrapper for masscan and nmap scripts. Massnmap makes scan using masscan on inputed target and gets output with IP:Ports pairs. Then, nmap runs on discovered services with inputed args. ez pezy.


## Usage

### Using Script

```
sudo massnmap.py <IP/Subnet> <masscan args> --nm <nmap args>
sudo massnmap.py -iL file.txt <masscan args> --nm <nmap args>
```

### Using Docker

```
docker build -t massnmap .  

docker run massnmap <IP/Subnet> <masscan args> --nm <nmap args>

//targets from file
docker run -d -it --name massnmap -v /root/tmp/:/tmp/ massnmap -iL /tmp/targets -p- --rate 8000 --nm -Pn -T4 -A > /tmp/nmap_res
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
