#!/usr/bin/env python3
# Tested on windows 10

import os
import subprocess
import time
import pyautogui

import click

# My location D:\SteamLibrary\steamapps\common\Crusader Kings III\binaries\ck3.exe
def start_game(location):
    os.startfile(location)
    
def end_game():
    subprocess.call(["taskkill", "-F", "/IM", "ck3.exe"])   #possibly parametrize the last element of the list

def click_through_the_menu():
    time.sleep(30)
    new_game_button = pyautogui.locateOnScreen('locate_pics/new_game.png', confidence=0.9)
    print(new_game_button)
    while not new_game_button:
        print("New game button not found.Retrying in 1 second")
        time.sleep(5)
        new_game_button = pyautogui.locateOnScreen('locate_pics/new_game.png', confidence=0.9)
    print(f"Success! New game button found! Where? {new_game_button}")
        
        
    

def click_through_new_game_start_menu():  #possibly a country name as a parameter of thhis func
    pass
    

def click_to_the_head_and_neck_panel():
    pass

def click_to_the_character_customization_panel():
    click_through_the_menu()
    click_through_new_game_start_menu()
    click_to_the_head_and_neck_panel()

def click_random_dna():
    pass

def copy_and_save_dna(output_folder, model_name):
    pass

def screenshot_and_save_face(output_folder, model_name):
    face_region = (2,1,3,7)
    pass

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
def main(exec, n, dna_folder, faces_folder):
    start_game(exec)
    
    click_to_the_character_customization_panel()
    for i in range(n):
        model_name = f"{i}"
        click_random_dna()
        copy_and_save_dna(dna_folder, model_name)
        screenshot_and_save_face(faces_folder, model_name)
    
    # time.sleep(15)
    end_game()

if __name__=="__main__":
    main()