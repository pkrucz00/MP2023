#!/usr/bin/env python3
# Tested on windows 10

import os
import subprocess
import time

import click

# My location D:\SteamLibrary\steamapps\common\Crusader Kings III\binaries\ck3.exe
def start_game(location):
    os.startfile(location)
    
def end_game():
    subprocess.call(["taskkill", "-F", "/IM", "ck3.exe"])

@click.command()
@click.option("--exec",
              type=click.Path(dir_okay=False, file_okay=True, exists=True),
              help="Path to the CK III game",
              required=True)
@click.option("-n", default=10, help="Number of output pictures")
@click.option("--dna_folder", type=click.Path(dir_okay=True, file_okay=False),
                default="dna",
                help="Output folder for generated faces")
@click.option("--faces_folder", type=click.Path(dir_okay=True, file_okay=False),
                default="faces",
                help="Output folder for generated faces")
def hello(exec, n, dna_folder, faces_folder):
    print(exec, n, dna_folder, faces_folder)
    start_game(exec)
    time.sleep(15)
    end_game()

if __name__=="__main__":
    hello()