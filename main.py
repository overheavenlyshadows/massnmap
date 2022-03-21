#!/usr/bin/python3

from ast import Try
from asyncio.subprocess import STDOUT
import subprocess
import argparse
import re
import sys, os


def args_parse():
    global argparser
    argparser = argparse.ArgumentParser(description="""
    Usage:
    massnmap <IP/Range or args for list> <masscan args> --nm <nmap args>
    """)
    argparser.add_argument('--nm', help='Delimeter between masscan and nmap args', required=True, action='store_true')
    argparser.parse_known_args()
    global target_ip
    target_ip = sys.argv[1]
    all_args = tuple(sys.argv[1:])
    nm_pos = all_args.index('--nm')
    global masscan_args, nmap_args
    masscan_args = all_args[1:nm_pos]
    nmap_args = all_args[nm_pos+1:]
    print(nmap_args)
    # print(all_args)
    # print(nm_pos)
    # print(masscan_args)


def args_check():
    try:
        subprocess.check_output(['masscan', *masscan_args], stderr=STDOUT)
    except Exception as log:
        if (re.search(r".*unknown config option.*", (log.output).decode('utf-8')) is not None):
            print('Masscan args are invalid:')
            print(log.output.decode('utf-8'))
            quit()
    try:
        subprocess.check_output(['nmap', *nmap_args], stderr=STDOUT)
    except Exception as log:
        if (re.search(r".*unrecognized option.*", (log.output).decode('utf-8')) is not None):
            print('Nmap args are invalid:')
            print(log.output.decode('utf-8'))
            quit()

        
def masscan_run():
    # try:
        nmap_input = {}
        masscan_output = subprocess.check_output(['masscan', target_ip, *masscan_args]).decode('utf-8')
        for line in masscan_output.splitlines():
            ip = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", line).group(0)
            port = re.search("\d{1,5}\/(tcp|udp)", line).group(0)
            if not (ip in nmap_input.keys()):
                nmap_input[ip] = [port]
            else:
                nmap_input[ip].append(port)
        nmap_run(nmap_input)


def nmap_run(nmap_output):
    delim = ","
    for line in nmap_output.items():
        port_list = []
        target_ip = line[0]
        ports = line[1]
        for port in ports:
            port = re.search(r"(\d+)", port).group(0)
            port_list.append(port)
        port_list_ready = delim.join(map(str, port_list)) #unpack tuple with delimiter
        print('nmap', target_ip, '-p'+port_list_ready, *nmap_args)
        nmap_output = subprocess.check_output(['nmap', target_ip, '-p'+port_list_ready, *nmap_args]).decode('utf-8')
        print(nmap_output)
             
        # if re.search(r"tcp", ports[0]:
        #     nmap_mode = 'tcp'
        # else:
        #     nmap_mode = 'udp'
        
def main():
    args_parse()
    args_check()
    masscan_run()

    


if __name__ == '__main__':
    if os.geteuid() != 0:
        print('Root required')
    else:
        main()
        
