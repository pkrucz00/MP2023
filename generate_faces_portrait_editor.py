#!/usr/bin/env python

import os
import sys
import shutil
import subprocess
import time

from datetime import datetime
from pathlib import Path
from random import randint

import click
import pyautogui
import pydirectinput
import pyperclip

MALE_TMP = "male_tmp.txt"
FEMALE_TMP = "female_tmp.txt"


def start_game(location):
    # My location C:\Users\pawel\Documents\STUDIA\magisterka\ck3_debug.exe.lnk
    os.startfile(location)
    time.sleep(20)  #it takes a while until the game starts...
    find_button("locate_pics/main_logo.png", 10)
    
    
def end_game():
    subprocess.call(["taskkill", "-F", "/IM", "ck3.exe"])   #possibly parametrize the last element of the list


def safe_create_path(path: str) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def archive_folder(folder_name):
    something = shutil.make_archive(base_name=folder_name, format="zip")
    print(f"Results archived and saved in {something}")
    

def safe_click(coords, label=""):
    wait_time = 0.0001
    if (label): print(f"Clicking {label}")
    
    pyautogui.moveTo(coords.x, coords.y)
    time.sleep(wait_time)
    pyautogui.click()
    

def find_button(pic_name, retry_in_sec=1, max_iter=10):
    confidence = 0.95
    
    button_placement = pyautogui.locateOnScreen(pic_name, confidence=confidence)
    i = 0
    while not button_placement and i < max_iter:
        print(f"{pic_name} not found. Retrying in {retry_in_sec} s.")
        time.sleep(retry_in_sec)
        button_placement = pyautogui.locateOnScreen(pic_name, confidence=confidence)
        i+=1
    
    return pyautogui.center(button_placement) if i < max_iter else False

    
def find_button_and_click(pic_name, retry_in_sec=1, label=""):
    button_center = find_button(pic_name, retry_in_sec=retry_in_sec)
    if not button_center: 
        return
    
    safe_click(button_center, label=label)


def save_dna(dna_text, out_path):
    with open(out_path, "w", encoding="UTF-8") as out_file:
        out_file.write(dna_text)
    

def copy_and_save_dna(output_path, copy_button_placement):
    safe_click(copy_button_placement)
    save_dna(pyperclip.paste(), output_path)
        

def activate_ck3_window():
    title = "Crusader Kings III"
    ck3_windows = pyautogui.getWindowsWithTitle(title)
    if ck3_windows:
        ck3_win = ck3_windows[0]
        if ck3_win.isActive: return
        
        try:
            ck3_win.activate()
        except:
            ck3_win.minimize()
            ck3_win.maximize()
            
    ck3_win.activate()
    
    assert pyautogui.getActiveWindow().title == title, f"The {title} is not active"


def click_to_the_portrait_mode(): 
    activate_ck3_window()
    print(f"Active window: {pyautogui.getActiveWindow().title}")
    pydirectinput.press('`')
    find_button_and_click('locate_pics/portrait_editor.png', label="Portrait Editor", retry_in_sec=0.1)
    pydirectinput.press("`")  # close debug panel 


def stabilize_heads(): #use value "1" in torso state input
    find_button_and_click("locate_pics/torso_state.png", label="Torso_state")
    pydirectinput.write("1")
    

def copy_text_to_clipboard(path):
    with open(path, 'r') as file:
        text = file.read().rstrip('\n')
    pyperclip.copy(text)


def prepare_initial_dna(genes_sample):
    def load_genes():
        copy_text_to_clipboard(genes_sample)
        find_button_and_click("locate_pics/paste_persistent_dna.png", label="Paste persistent DNA")
        
    load_random = lambda: find_button_and_click("locate_pics/randomize_dna.png", label="Random DNA")
    
    if genes_sample:
        load_genes()
    else:
        load_random()
    
    male_copy_dna_pos = find_button("locate_pics/copy_persistent_dna_male.png")
    female_copy_dna_pos = find_button("locate_pics/copy_persistent_dna_female.png")
    
    print(f"male {male_copy_dna_pos}")
    print(f"female {female_copy_dna_pos}")
    
    copy_and_save_dna(MALE_TMP, male_copy_dna_pos)
    copy_and_save_dna(FEMALE_TMP, female_copy_dna_pos)
    
       
def prepare(genes_sample):
    click_to_the_portrait_mode()
    stabilize_heads()     
    prepare_initial_dna(genes_sample)        


def read_lines_of_file(path):
    with open(path, "r", encoding="UTF-8") as file:
        return [line.strip("\n") for line in file.readlines()]


"""
example line:

    gene_forehead_brow_height={ "forehead_brow_height_pos" 149 "forehead_brow_height_pos" 149 }

Elements in line after split:
0 - gene name
1 - dom_gene
2 - dom_gene_val  <- this value should be changed
3 - rec_gene
4 - rec_gene_val
5 - end bracket
"""
def modify_value_of_a_gene(line, value):
     DOM_GENE_VAL_POS = 2
     splitted_line = line.split()
     splitted_line[DOM_GENE_VAL_POS] = str(value) 
     return " ".join(splitted_line)


def modify_gene(dna_lines, new_gene_value, gene):
    result = []
    for dna_line in dna_lines:
        if gene in dna_line:
            dna_line = modify_value_of_a_gene(dna_line, new_gene_value)
            print(dna_line)
        
        result.append(dna_line)
    return "\n".join(result)


def screenshot_and_save_face(output_folder, model_name):
    output_path=f"{output_folder}/{model_name}.png"
    face_region = (786, 315, 164, 186) if "m" in model_name else (1310, 315, 164, 186)
    pyautogui.screenshot(output_path, region=face_region)


def copy_and_save_model(dna, model_name, output_folder):
    save_dna(dna, f"{output_folder}/{model_name}.txt")
    screenshot_and_save_face(output_folder, model_name)    
    
    
def generate_face_with_limits(dna, val, gene, output_folder, sex):
    modified_genes = modify_gene(dna, val, gene)
    pyperclip.copy(modified_genes)
    model_name = f"{sex}-{gene}-{datetime.now().strftime('%Y%m%d_%H%M%S%f')}"
    find_button_and_click("locate_pics/paste_persistent_dna.png", 0.1, "paste dna")
    copy_and_save_model(modified_genes, model_name, output_folder)

def generate_faces_with_gene_limits(n, genes, out, val_range):
    male_dna = read_lines_of_file(MALE_TMP)
    female_dna = read_lines_of_file(FEMALE_TMP)
    result_folder = safe_create_path(out)
    (val_from, val_to) = val_range
    
    for gene in genes:
        for _ in range(n):
            for val in range(val_from, val_to + 1):
                if val == -1: val = randint(0, 255)
                
                generate_face_with_limits(male_dna, val, gene, result_folder, "m")
                generate_face_with_limits(female_dna, val, gene, result_folder, "f")


def delete_tmp_files():
    os.remove(MALE_TMP)
    os.remove(FEMALE_TMP)

def invalid_range(val_range):
    return not (0 <= val_range[0] <= 255) or not (0 <= val_range[1] <= 255)


@click.command()
@click.option("--exec", required=True,
              type=click.Path(dir_okay=False, file_okay=True, readable=True, exists=True),
              help="Path to the CK III game. Make sure it is in debug mode.")
@click.option("--gene_list", required=True,
              type=click.Path(dir_okay=False, file_okay=True, exists=True),
              help="File with a list of genes that should be randomized")
@click.option("--gene_sample",
            type=click.Path(dir_okay=False, file_okay=True, exists=True),
            help="File with a sample for further gene specification. If not specified, random model will be generated.")
@click.option("-n", default=10, help="Number of output pictures")
@click.option("--val_range", type=(int, int), default=(-1,-1), help="Range of parameters value")
@click.option("--out", type=click.Path(dir_okay=True, file_okay=False),
                default="results",
                help="Output folder for generated faces and dna files")
@click.option("--zip", is_flag=True, default=False, help="Zip the results")
def main(exec, gene_list, gene_sample, n, val_range, out, zip):
    if not val_range == (-1, -1) and invalid_range(val_range): raise Exception("Invalid range")
     
    start_game(exec)
    prepare(gene_sample)
    
    list_of_genes = read_lines_of_file(gene_list)
    generate_faces_with_gene_limits(n, list_of_genes, out, val_range)
    delete_tmp_files()
    if (zip): archive_folder(out)
    end_game()

if __name__=="__main__":
    main()