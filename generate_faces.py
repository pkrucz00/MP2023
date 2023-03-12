#!/usr/bin/env python3
# Tested on windows 10

import os
import subprocess
import time
import pyautogui
from random import randint

import click
import pyperclip

# My location D:\SteamLibrary\steamapps\common\Crusader Kings III\binaries\ck3.exe
def start_game(location):
    os.startfile(location)
    # time.sleep(45)  #it takes a while until the game starts...
    
def end_game():
    subprocess.call(["taskkill", "-F", "/IM", "ck3.exe"])   #possibly parametrize the last element of the list

def wait_and_click(pic_name, wait_in_sec=0.1, retry_in_sec=1, label=""):
    print(f"Waiting for {wait_in_sec} [s]")
    time.sleep(wait_in_sec)
    button_placement = pyautogui.locateOnScreen(pic_name, confidence=0.9)
    while not button_placement:
        print(f"{pic_name} not found. Retrying in {retry_in_sec} s.")
        time.sleep(retry_in_sec)
        button_placement = pyautogui.locateOnScreen(pic_name, confidence=0.9)
    
    print(f"Clicking {label}")
    button_center = pyautogui.center(button_placement)
    pyautogui.moveTo(button_center.x, button_center.y)
    time.sleep(1)
    pyautogui.click()
    # pyautogui.click(button_center.x, button_center.y)
    

def click_through_the_menu():
    wait_and_click('locate_pics/new_game.png', label="New Game Button", retry_in_sec=5)
        
def click_through_new_game_start_menu():  #possibly a country name as a parameter of thhis func
    wait_and_click('locate_pics/play_as_any_ruler.png', label="Play As Any Ruler Button")
    wait_and_click('locate_pics/poland.png', wait_in_sec=10, retry_in_sec=3, label="Poland")
    wait_and_click('locate_pics/create_ruler.png', label="Create Ruler Button", wait_in_sec=1)

def click_to_the_head_and_neck_panel():
    wait_and_click("locate_pics/change_apperance.png", label="Change Appearance Button")
    wait_and_click("locate_pics/customize_further.png", label="Customize Further", wait_in_sec=0.5)
    wait_and_click("locate_pics/show_hair_and_beard.png", label="Show Hair and Beard")
    wait_and_click("locate_pics/head_and_neck.png", label="Head and Neck")

def click_to_the_character_customization_panel():
    click_through_the_menu()
    click_through_new_game_start_menu()
    click_to_the_head_and_neck_panel()

def click_random_dna():
    wait_and_click("locate_pics/randomize.png", label="Random", wait_in_sec=3)

def copy_and_save_dna(output_folder, model_name):
    output_path=f"{output_folder}/{model_name}-dna.txt"
    wait_and_click("locate_pics/copy.png", label="Copy DNA")
    dna_text = pyperclip.paste()
    with open(output_path, "w", encoding="UTF-8") as out_file:
        out_file.writelines(dna_text)
    print(f"DNA of model {model_name} successfully saved to {output_path}!")

def screenshot_and_save_face(output_folder, model_name):
    output_path=f"{output_folder}/{model_name}.png"
    face_region = (500, 200, 800, 500)
    pyautogui.screenshot(output_path, region=face_region)
    print(f"Face of model {model_name} successfully saved to {output_path}")
    

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
    for _ in range(n):
        model_name = f"{randint(0, 1_000_000)}"
        click_random_dna()
        copy_and_save_dna(dna_folder, model_name)
        screenshot_and_save_face(faces_folder, model_name)
    
    end_game()

if __name__=="__main__":
    main()