import glob

from generate_2d_viz import generate_2d_viz
from generate_3d_viz import generate_3d_viz
from preprocessing import s3_download

from pathlib import Path
import os
import shutil

if __name__ == "__main__":
    link = "s3://medvolt-drp/results/client_6/workspace_1/project_1/experiment_1/C1CCC(C(C1)CN2CCN(CC2)C3=NSC4=CC=CC=C43)CN5C(=O)C6C7CCC(C7)C6C5=O/"
    download_folder = link.split("/")[8]
    s3_download(link, download_folder)

    f_list = [x for x in Path(download_folder).rglob('*.pdb')]
    f_list = [str(x) for x in f_list if "complex" in x.name]
    f_name = [x.split("/")[1] for x in f_list]
    # print(f_list)  # Downloading complete
    print("Downloaded Files")

    # Move the files to root dir
    for i in range(len(f_list)):
        shutil.move(f_list[i], f"./{f_name[i]}.pdb")

    # List out moved files
    curr_files = [x.split("/")[1] for x in glob.glob("./*") if ".pdb" in x]
    print(curr_files)

    for file in curr_files:
        generate_2d_viz(file)
        generate_3d_viz(file)
