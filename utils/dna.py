from __future__ import annotations
import re
from pydantic import BaseModel
from typing import Literal


class Genes(BaseModel):
    type: Literal["female", "male"]
    hair_color: tuple[int, int, int, int]
    skin_color: tuple[int, int, int, int]
    eye_color: tuple[int, int, int, int]
    gene_chin_forward: dict[str, int]
    gene_chin_height: dict[str, int]
    gene_chin_width: dict[str, int]
    gene_eye_angle: dict[str, int]
    gene_eye_depth: dict[str, int]
    gene_eye_height: dict[str, int]
    gene_eye_distance: dict[str, int]
    gene_eye_shut: dict[str, int]
    gene_forehead_angle: dict[str, int]
    gene_forehead_brow_height: dict[str, int]
    gene_forehead_roundness: dict[str, int]
    gene_forehead_width: dict[str, int]
    gene_forehead_height: dict[str, int]
    gene_head_height: dict[str, int]
    gene_head_width: dict[str, int]
    gene_head_profile: dict[str, int]
    gene_head_top_height: dict[str, int]
    gene_head_top_width: dict[str, int]
    gene_jaw_angle: dict[str, int]
    gene_jaw_forward: dict[str, int]
    gene_jaw_height: dict[str, int]
    gene_jaw_width: dict[str, int]
    gene_mouth_corner_depth: dict[str, int]
    gene_mouth_corner_height: dict[str, int]
    gene_mouth_forward: dict[str, int]
    gene_mouth_height: dict[str, int]
    gene_mouth_width: dict[str, int]
    gene_mouth_upper_lip_size: dict[str, int]
    gene_mouth_lower_lip_size: dict[str, int]
    gene_mouth_open: dict[str, int]
    gene_neck_length: dict[str, int]
    gene_neck_width: dict[str, int]
    gene_bs_cheek_forward: dict[str, int]
    gene_bs_cheek_height: dict[str, int]
    gene_bs_cheek_width: dict[str, int]
    gene_bs_ear_angle: dict[str, int]
    gene_bs_ear_inner_shape: dict[str, int]
    gene_bs_ear_bend: dict[str, int]
    gene_bs_ear_outward: dict[str, int]
    gene_bs_ear_size: dict[str, int]
    gene_bs_eye_corner_depth: dict[str, int]
    gene_bs_eye_fold_shape: dict[str, int]
    gene_bs_eye_size: dict[str, int]
    gene_bs_eye_upper_lid_size: dict[str, int]
    gene_bs_forehead_brow_curve: dict[str, int]
    gene_bs_forehead_brow_forward: dict[str, int]
    gene_bs_forehead_brow_inner_height: dict[str, int]
    gene_bs_forehead_brow_outer_height: dict[str, int]
    gene_bs_forehead_brow_width: dict[str, int]
    gene_bs_jaw_def: dict[str, int]
    gene_bs_mouth_lower_lip_def: dict[str, int]
    gene_bs_mouth_lower_lip_full: dict[str, int]
    gene_bs_mouth_lower_lip_pad: dict[str, int]
    gene_bs_mouth_lower_lip_width: dict[str, int]
    gene_bs_mouth_philtrum_def: dict[str, int]
    gene_bs_mouth_philtrum_shape: dict[str, int]
    gene_bs_mouth_philtrum_width: dict[str, int]
    gene_bs_mouth_upper_lip_def: dict[str, int]
    gene_bs_mouth_upper_lip_full: dict[str, int]
    gene_bs_mouth_upper_lip_profile: dict[str, int]
    gene_bs_mouth_upper_lip_width: dict[str, int]
    gene_bs_nose_forward: dict[str, int]
    gene_bs_nose_height: dict[str, int]
    gene_bs_nose_length: dict[str, int]
    gene_bs_nose_nostril_height: dict[str, int]
    gene_bs_nose_nostril_width: dict[str, int]
    gene_bs_nose_profile: dict[str, int]
    gene_bs_nose_ridge_angle: dict[str, int]
    gene_bs_nose_ridge_width: dict[str, int]
    gene_bs_nose_size: dict[str, int]
    gene_bs_nose_tip_angle: dict[str, int]
    gene_bs_nose_tip_forward: dict[str, int]
    gene_bs_nose_tip_width: dict[str, int]
    face_detail_cheek_def: dict[str, int]
    face_detail_cheek_fat: dict[str, int]
    face_detail_chin_cleft: dict[str, int]
    face_detail_chin_def: dict[str, int]
    face_detail_eye_lower_lid_def: dict[str, int]
    face_detail_eye_socket: dict[str, int]
    face_detail_nasolabial: dict[str, int]
    face_detail_nose_ridge_def: dict[str, int]
    face_detail_nose_tip_def: dict[str, int]
    face_detail_temple_def: dict[str, int]
    expression_brow_wrinkles: dict[str, int]
    expression_eye_wrinkles: dict[str, int]
    expression_forehead_wrinkles: dict[str, int]
    expression_other: dict[str, int]
    complexion: dict[str, int]
    gene_height: dict[str, int]
    gene_bs_body_type: dict[str, int]
    gene_bs_body_shape: dict[str, int]
    gene_bs_bust: dict[str, int]
    gene_age: dict[str, int]
    gene_eyebrows_shape: dict[str, int]
    gene_eyebrows_fullness: dict[str, int]
    gene_body_hair: dict[str, int]
    gene_hair_type: dict[str, int]
    gene_baldness: dict[str, int]
    eye_accessory: dict[str, int]
    teeth_accessory: dict[str, int]
    eyelashes_accessory: dict[str, int]
    clothes: dict[str, int]

    @staticmethod
    def from_ck_string(string: str) -> Genes:
        gender_pattern = r'type=(\w+)'
        genes_pattern = r'genes=(.*)'
        key_val_pattern = r'(\w+)\s*=\s*{([^}]+)}'
        list_pattern = r'\s*(\d+) (\d+) (\d+) (\d+)\s*'
        string_pattern = r'"([^"]+)" (\d+)'

        gender = re.findall(gender_pattern, string)[0]
        genes_all = re.findall(genes_pattern, string, re.DOTALL)[0]

        genes_dict = {"type": gender}
        for key, value in re.findall(key_val_pattern, genes_all):
            values = re.findall(list_pattern, value)
            if not values:
                values = {key: val for key, val in re.findall(string_pattern, value)}
            else:
                values = tuple(map(int, values[0]))
            genes_dict[key] = values
        return Genes(**genes_dict)
    
    def to_ck_string(self) -> str:
        ck_string = "ruler_designer={\ntype=" + self.type + "\nid=0\ngenes={"
        for key, value in self.dict(exclude={"type"}).items():
            if isinstance(value, tuple):
                value_str = f" {value[0]} {value[1]} {value[2]} {value[3]} "
            else:
                value_str = "".join([f' "{sub_key}" {sub_val} ' for sub_key, sub_val in value.items()])
                if len(value) == 1:
                    value_str *= 2

            ck_string += f"\t{key}={{{value_str}}}\n"
        ck_string += "}"
        return ck_string

if __name__ == "__main__":
    fpath = "data/dataset_2023_03_26/male/arabic/dna/20230327_015121422378.txt"
    with open(fpath, "r") as f:
        string = f.read()
        genes = Genes.from_ck_string(string)
        print(genes)

    print(genes.to_ck_string())
    