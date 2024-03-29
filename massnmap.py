#!/usr/bin/python3

from ast import Try
from asyncio.subprocess import DEVNULL, STDOUT
import subprocess
import argparse
import re
import sys, os
from time import sleep
from socket import inet_aton

script_version = "1.1.1"


def args_parse():
    global argparser
    argparser = argparse.ArgumentParser(description="Do not use Masscan/Nmap input/output flags!!! Use Linux output redirect to save results to file.", usage="massnmap <IP/Subnet> <masscan args> --nm <nmap args>")
    argparser.add_argument('--nm', help='Delimeter between masscan and nmap args', required=True, action='store_true')
    argparser.parse_known_args()
    global target_ip
    target_ip = sys.argv[1]
    all_args = list(sys.argv[1:])
    nm_pos = all_args.index('--nm')
    global masscan_args, nmap_args, masscan_list_mode, masscan_args_wo_target
    masscan_args = all_args[0:nm_pos]
    nmap_args = all_args[nm_pos+1:]
    if re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", target_ip):
        masscan_list_mode = 0
        masscan_args_wo_target = all_args[1:nm_pos]
    else:
        masscan_list_mode = 1
        il_pos = all_args.index('-iL')
        il_list_value = all_args[il_pos + 1] 
        masscan_args_wo_target = all_args[0:nm_pos]
        del masscan_args_wo_target[il_pos]
        masscan_args_wo_target.remove(il_list_value)

def args_check():
    print('[INFO] Checking if args are correct...\n')
    try:
        subprocess.check_output(['masscan', '127.0.0.1', *masscan_args_wo_target, '--wait 0'], stderr=STDOUT, timeout=2)
    except subprocess.TimeoutExpired as e:
            print('[INFO] Masscan args are correct')   
    except subprocess.CalledProcessError as error:
        if (re.search(r".*unknown config option.*", (error.output).decode('utf-8')) is not None):
            print('[ERROR] Masscan args are invalid:')
            print(error.output.decode('utf-8'))
            quit()
        else:
            print('[ERROR] Unknown error:')
            print(error.output.decode('utf-8'))
            quit()
    try:
        subprocess.check_output(['nmap', *nmap_args], stderr=STDOUT, timeout=2)
        print('[INFO] Nmap args are correct')
    except subprocess.TimeoutExpired as e:
            print('[INFO] Nmap args are correct')   
    except Exception as error:
        if ((re.search(r".*(unrecognized option|Illegal Argument).*", (error.output).decode('utf-8'))) is not None):
            print('[ERROR] Nmap args are invalid:')
            print((error.output).decode('utf-8'))
            quit()
        else:
            print('[ERROR] Unknown error:')
            print((error.output).decode('utf-8'))
            quit()
        
def masscan_run():
    print("\n============================================================")
    print("Masscan args: ", *masscan_args)
    print("Nmap args: ", *nmap_args)
    print("============================================================\n")
    try:
        nmap_unsorted_input = {}
        masscan_output = subprocess.check_output(['masscan', *masscan_args]).decode('utf-8')
        for line in masscan_output.splitlines():
            ip = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", line).group(0)
            port = re.search("\d{1,5}\/(tcp|udp)", line).group(0)
            if not (ip in nmap_unsorted_input.keys()):
                nmap_unsorted_input[ip] = [port]
            else:
                nmap_unsorted_input[ip].append(port)
        nmap_input = dict(sorted(nmap_unsorted_input.items(), key=lambda item: inet_aton(item[0])))
        print(nmap_input)
        nmap_run(nmap_input)
    except Exception as error:
        print('\n\n [ERROR] Unexcpected Error.')
        print((error.output).decode('utf-8'))
        quit()


def nmap_run(nmap_input):
    delim = ","
    try:
        for line in nmap_input.items():
            port_list = []
            target_ip = line[0]
            ports = line[1]
            for port in ports:
                port = re.search(r"(\d+)", port).group(0)
                port_list.append(port)
            port_list_ready = delim.join(map(str, port_list)) #unpack tuple with delimiter
            print('nmap', target_ip, '-p'+port_list_ready, *nmap_args)
            nmap_output = subprocess.check_output(['nmap', target_ip, '-p'+port_list_ready, *nmap_args], stderr=DEVNULL).decode('utf-8')
            print(nmap_output)
            print('\n----------------------------------------------------\n')
            sleep(1)
    except Exception as error:
        print('\n\n [ERROR] Unexcpected Error.')
        print((error.output).decode('utf-8'))
        quit()
            
             
        # if re.search(r"tcp", ports[0]:
        #     nmap_mode = 'tcp'
        # else:
        #     nmap_mode = 'udp'
        
def main():
    print("\n===============")
    print("Massnmap v" + str(script_version))
    print("===============\n")
    args_parse()
    args_check()
    masscan_run()

if __name__ == '__main__':
    if os.geteuid() != 0:
        print('Root required')
    else:
        main()
        
