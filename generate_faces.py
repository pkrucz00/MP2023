#!/usr/bin/env python3
# Tested on windows 10

import os
import shutil
import subprocess
import time

from datetime import datetime
from pathlib import Path

import click
import pyautogui
import pyperclip

LOC_PICS_FOLDER = "locate_pics"
ETHNICITY_FOLDER = Path(LOC_PICS_FOLDER, "ethnicity")
SEX_FOLDER = Path(LOC_PICS_FOLDER, "sex")


def start_game(location):
    # My location D:\SteamLibrary\steamapps\common\Crusader Kings III\binaries\ck3.exe
    os.startfile(location)
    time.sleep(60)  #it takes a while until the game starts...
    
def end_game():
    subprocess.call(["taskkill", "-F", "/IM", "ck3.exe"])   #possibly parametrize the last element of the list


def safe_create_path(path: str) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_all_png_from_folder(folder_path):
    return [path for path in os.listdir(folder_path) if path.endswith(".png")]


def archive_folder(folder_name):
    # folder_stem = Path(folder_name).stem
    # output_filename = f"{folder_stem}"
    something = shutil.make_archive(base_name=folder_name, format="zip")
    print(something)


def find_button(pic_name, retry_in_sec=1):
    confidence = 0.9
    
    button_placement = pyautogui.locateOnScreen(pic_name, confidence=confidence)
    while not button_placement:
        print(f"{pic_name} not found. Retrying in {retry_in_sec} s.")
        time.sleep(retry_in_sec)
        button_placement = pyautogui.locateOnScreen(pic_name, confidence=confidence)
    
    return pyautogui.center(button_placement)


def safe_click(coords, label=""):
    wait_time = 0.0001
    if (label): print(f"Clicking {label}")
    
    pyautogui.moveTo(coords.x, coords.y)
    time.sleep(wait_time)
    pyautogui.click()


def find_button_and_click(pic_name, retry_in_sec=1, label=""):
    button_center = find_button(pic_name, retry_in_sec=retry_in_sec)
    safe_click(button_center, label=label)
    

def click_through_the_menu():
    find_button_and_click('locate_pics/new_game.png', label="New Game Button", retry_in_sec=5)
        
        
def click_through_new_game_start_menu():
    wait_after_play_as_any_ruler = lambda: time.sleep(10)
    wait_after_choosing_country = lambda: time.sleep(1)
    
    find_button_and_click('locate_pics/play_as_any_ruler.png', label="Play As Any Ruler Button")
    wait_after_play_as_any_ruler()
    find_button_and_click('locate_pics/poland.png', retry_in_sec=3, label="Poland")
    wait_after_choosing_country()
    find_button_and_click('locate_pics/create_ruler.png', label="Create Ruler Button")


def click_to_the_character_customization_panel():
    click_through_the_menu()
    click_through_new_game_start_menu()
    
    
def click_change_appearance():
    find_button_and_click("locate_pics/change_appearance.png", label="Change Appearance Button")
    time.sleep(0.05)
   
    
def click_customize_further():
    find_button_and_click("locate_pics/customize_further.png", label="Customize Further")    


def click_to_head_and_neck_panel():
    find_button_and_click("locate_pics/show_hair_and_beard.png", label="Show Hair and Beard")
    find_button_and_click("locate_pics/head_and_neck.png", label="Head and Neck")

def click_sex(sex_path: str):
    find_button_and_click(f"{SEX_FOLDER}/{sex_path}")
    
    
def click_ethnicity(ethnicity_path: str):
    find_button_and_click(f"{ETHNICITY_FOLDER}/{ethnicity_path}")
    

def click_back():
    find_button_and_click(f"{LOC_PICS_FOLDER}/back.png")


def click_random_dna(random_data_button_placement):
    safe_click(random_data_button_placement)

def copy_and_save_dna(output_folder, model_name, copy_button_placement):
    output_path=f"{output_folder}/{model_name}.txt"
    safe_click(copy_button_placement)
    dna_text = pyperclip.paste()
    with open(output_path, "w", encoding="UTF-8") as out_file:
        out_file.writelines(dna_text)


def screenshot_and_save_face(output_folder, model_name):
    output_path=f"{output_folder}/{model_name}.png"
    face_region = (666, 315, 280, 430)
    
    pyautogui.screenshot(output_path, region=face_region)
    
    
def generate_faces_and_dna(n, results_folder):
    random_dna_button_placement = find_button("locate_pics/randomize.png")
    copy_button_placement = find_button("locate_pics/copy.png")
    
    dna_folder = safe_create_path(f"{results_folder}/dna")
    faces_folder = safe_create_path(f"{results_folder}/faces")
    
    for _ in range(n):
        model_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S%f')}"
        click_random_dna(random_dna_button_placement)
        copy_and_save_dna(dna_folder, model_name, copy_button_placement)
        screenshot_and_save_face(faces_folder, model_name)
        
    
def generate_all_ethnicities(number_of_faces_per_ethnicity, output_folder):
    ethnicities = get_all_png_from_folder(ETHNICITY_FOLDER)
    for ethnicity in ethnicities:
        click_ethnicity(ethnicity)
        ethnicity_stem = Path(ethnicity).stem
        
        click_customize_further()
        click_to_head_and_neck_panel()
        generate_faces_and_dna(n=number_of_faces_per_ethnicity, results_folder=f"{output_folder}/{ethnicity_stem}")
        click_back()
    pass
    
    
def generate_all_faces(number_of_faces_per_ethnicity_and_sex, output_folder):
    start = time.time()
    
    sexes = get_all_png_from_folder(SEX_FOLDER)
    for sex in sexes:
        click_sex(sex)
        sex_stem = Path(sex).stem
        click_change_appearance()
        generate_all_ethnicities(number_of_faces_per_ethnicity_and_sex, f"{output_folder}/{sex_stem}")    
        click_back()
    
    stop = time.time()
    print(f"Generating items done! Time of generation: {round(stop - start, 3)} [s]")
    

@click.command()
@click.option("--exec",
              type=click.Path(dir_okay=False, file_okay=True, exists=True),
              help="Path to the CK III game")
@click.option("-n", default=10, help="Number of output pictures per ethnicity and per sex")
@click.option("--out", type=click.Path(dir_okay=True, file_okay=False),
                default="results",
                help="Output folder for generated faces and dna files")
@click.option("--zip", is_flag=True, default=False, help="Zip the results")
def main(exec, n, out, zip):
    if (exec): start_game(exec)
    
    click_to_the_character_customization_panel()
    generate_all_faces(n, out)
    if (zip): archive_folder(out)
    
    if (exec): end_game()

if __name__=="__main__":
    main()