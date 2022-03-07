#!/usr/bin/python3


import subprocess
import argparse
import sys, os


def arg_parse():
    global argparser
    argparser = argparse.ArgumentParser(description="""
    Usage:
    massnmap [IP] <masscan args> --nm <nmap args>
    """)
    argparser.add_argument('--nm', help='Delimeter between masscan and nmap args', required=True)
    target_ip = sys.argv[1]
    all_args = tuple(sys.argv[1:])
    nm_pos = all_args.index('--nm')
    global masscan_args
    masscan_args = all_args[0:nm_pos]
    print(all_args)
    print(nm_pos)
    print(masscan_args)

def masscan_run():
    try:
        masscan_output = subprocess.check_output(['masscan', *masscan_args ])  
        print(masscan_output)
        
    except:
        print('Masscan error')
        print(argparser.print_help)
    
    

def main():
    arg_parse()
    masscan_run()

    


if __name__ == '__main__':
    if os.geteuid() != 0:
        print('Root required')
    else:
        print(sys.argv[1:]) 
        main()
        
