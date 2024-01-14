#!/usr/bin/env python

import os
import shutil
import subprocess
import time

import numpy as np
from scipy.stats import t

from datetime import datetime
from pathlib import Path

import click
import pyautogui
import pydirectinput
import pyperclip

MALE_TMP = "male_tmp.txt"
# FEMALE_TMP = "female_tmp.txt"

GAME_PATH = Path(r"C:\Users\pawel\Documents\STUDIA\magisterka\ck3_debug.exe.lnk")

def start_game(location):
    location = location if location else GAME_PATH
    
    os.startfile(location)
    time.sleep(30)  #it takes a while until the game starts...
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
    dna_to_save = pyperclip.paste()
    print(f"Dna to save: {dna_to_save}")
    save_dna(dna_to_save, output_path)
        

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
    active_window = pyautogui.getActiveWindow()
    
    assert active_window, "No active window. Activation of CK III window failed"
    assert active_window.title == title, f"The {title} is not active"


def click_to_the_portrait_mode(): 
    activate_ck3_window()
    print(f"Active window: {pyautogui.getActiveWindow().title}")
    pydirectinput.press('`')
    find_button_and_click('locate_pics/portrait_editor.png', label="Portrait Editor", retry_in_sec=0.1)
    pydirectinput.press("`")  # close debug panel 


def stabilize_heads(button_coords): #use value "1" in torso state input
    # find_button_and_click("locate_pics/torso_state.png", label="Torso_state")
    safe_click(button_coords, label="Click 1 on torso state")
    # pydirectinput.press("backspace")
    pydirectinput.press("1")
    

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
    
    time.sleep(1)
    male_copy_dna_pos = find_button("locate_pics/copy_persistent_dna_male.png")
    # female_copy_dna_pos = find_button("locate_pics/copy_persistent_dna_female.png")
    
    print(f"male {male_copy_dna_pos}")
    # print(f"female {female_copy_dna_pos}")
    time.sleep(1)
    copy_and_save_dna(MALE_TMP, male_copy_dna_pos)
    # copy_and_save_dna(FEMALE_TMP, female_copy_dna_pos)
       
def prepare(genes_sample):
    click_to_the_portrait_mode()
    stabilize_heads(find_button("locate_pics/torso_state.png"))     
    prepare_initial_dna(genes_sample)        


def read_lines_of_file(path):
    with open(path, "r", encoding="UTF-8") as file:
        return [line for line in file.readlines()]


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
     result =  " ".join(splitted_line)
     return result

def modify_gene(dna_lines, new_gene_value, gene):
    result = []
    found = False
    for dna_line in dna_lines:
        if gene in dna_line:
            found = True
            dna_line = modify_value_of_a_gene(dna_line, new_gene_value)
            print(f"Modifying gene {gene} to {new_gene_value}")
            
        result.append(dna_line)
    if not found: print(f"[WARNING] {gene} not found in dna list (value: {new_gene_value})")
    return result


def screenshot_and_save_face(output_folder, model_name, stabilize_button_coords):
    output_path=f"{output_folder}/{model_name}.png"
    face_region = (786, 315, 164, 186) if "m" in model_name else (1310, 315, 164, 186)
    # stabilize_heads(stabilize_button_coords)
    pyautogui.screenshot(output_path, region=face_region)


def copy_and_save_model(dna, model_name, output_folder, stabilize_button_coords):
    save_dna(dna, f"{output_folder}/{model_name}.txt")
    screenshot_and_save_face(output_folder, model_name, stabilize_button_coords)    
    
    
def generate_face_with_limits(dna, val_range, genes, output_folder, sex, button_coords, stabilize_button_coords):
    if len(genes) == 1:
        gene = genes[0]
        for val in val_range:
            modified_dna_lines = modify_gene(dna, val, gene)
            modified_genes = "".join(modified_dna_lines)
            pyperclip.copy(modified_genes)
            
            model_name = f"{sex}-{gene}-{datetime.now().strftime('%Y%m%d_%H%M%S%f')}"
            safe_click(button_coords, "paste dna")
            time.sleep(0.05)
            copy_and_save_model(modified_genes, model_name, output_folder, stabilize_button_coords)
        return
    
    gene = genes.pop()
    for val in val_range:
        modified_dna_lines = modify_gene(dna, val, gene)
        out = safe_create_path(f"{output_folder}/{gene}_{val}")
        generate_face_with_limits(modified_dna_lines, val_range, genes[:], out, sex, button_coords, stabilize_button_coords)

def create_range(val_range, n_buckets, gaussian):
    a, b = val_range
    mean, std = (b - a)/2, 64
    
    break_points_uniform = np.linspace(0, 1, n_buckets + 2)[1:-1]
    print(break_points_uniform)
    break_points = t.ppf(break_points_uniform, df=n_buckets-1, loc=mean, scale=std) \
        if gaussian else 2*mean*break_points_uniform
    return np.rint(break_points)


def generate_faces_with_gene_limits(n, genes, out, val_range, n_buckets, gaussian):
    male_dna_lines = read_lines_of_file(MALE_TMP)
    # female_dna = read_lines_of_file(FEMALE_TMP)
    result_folder = safe_create_path(out)
    button_coords = find_button("locate_pics/paste_persistent_dna.png", 0.1)
    stabilize_button_coords = find_button("locate_pics/torso_state.png")
    
    t1 = time.time()
    values_range = create_range(val_range, n_buckets, gaussian)
    for _ in range(n):
        generate_face_with_limits(male_dna_lines, values_range, genes, result_folder, "m", button_coords, stabilize_button_coords)
    
        # generate_face_with_limits(female_dna, val, gene, result_folder, "f")
    print(f"Done in {time.time() - t1} [s]")

def delete_tmp_files():
    os.remove(MALE_TMP)
    # os.remove(FEMALE_TMP)
    

@click.command()
@click.option("--exec",
              type=click.Path(dir_okay=False, file_okay=True, readable=True, exists=True),
              help="Path to the CK III game. Make sure it is in debug mode.")
@click.option("--gene_list", required=True,
              type=click.Path(dir_okay=False, file_okay=True, exists=True),
              help="File with a list of genes that should be randomized")
@click.option("--gene_sample",
            type=click.Path(dir_okay=False, file_okay=True, exists=True),
            help="File with a sample for further gene specification. If not specified, random model will be generated.")
@click.option("-n", default=10, help="Number of output pictures")
@click.option("--val_range", type=(int, int), default=(0, 255), help="Range of parameters value")
@click.option("--n_buckets", default=8, help="Number of sampled faces per gene")
@click.option("--out", type=click.Path(dir_okay=True, file_okay=False),
                default="results",
                help="Output folder for generated faces and dna files")
@click.option("--gaussian_t", is_flag=True, default=False, help="Step by t student with std=64")
@click.option("--zip", is_flag=True, default=False, help="Zip the results")
def main(exec, gene_list, gene_sample, n, val_range, n_buckets, out, gaussian_t, zip): 
    start_game(exec)
    prepare(gene_sample)
    
    list_of_genes = read_lines_of_file(gene_list)
    list_of_genes = [s.strip() for s in list_of_genes]
    generate_faces_with_gene_limits(n, list_of_genes, out, val_range, n_buckets, gaussian_t)
    delete_tmp_files()
    if (zip): archive_folder(out)
    end_game()

if __name__=="__main__":
    main()