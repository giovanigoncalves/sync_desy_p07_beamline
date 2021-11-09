# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 23:23:29 2021

@author: Giovani
"""

# Corrigido o erro da unificação dos arquivos


import os
import pandas as pd


first_extension = str(
    input("What is the file extension? (Examples: .asc, .chi, .txt, ...): ")).lower()
change = str(input("Do you want to change file extension? [Y/N] ")).lower()
if "y" == change:
    second_extension = str(input(
        "What is the final extension: (Examples: .asc, .chi, .txt, ...): ")).lower()
elif "n" == change:
    second_extension = first_extension

# For the case where the file is not cut
procede = "yes"
while "y" in procede:
    decision = str(input("Do you want to cut the file: "))
    if decision.lower() in "no":
        folder = "Completed_files_converted"
        os.mkdir(folder)
        for filename in os.listdir(os.getcwd()):
            if filename[-4:] == first_extension:
                with open(filename) as file_a:
                    lines = file_a.readlines()[4:]
                    with open(f"./{folder}/" + filename[:-4] + second_extension, mode="w") as file_b:
                        file_b.writelines(lines)
        print(f"\nFiles converted to {folder} folder\n")

# Joining the file in one from completed converted files
        join = str(
            input("Do you want to join the files in one unique file: [Y/N]")).lower()
        if "y" in join:

            df = pd.DataFrame()
            df_indiv_normal = pd.DataFrame()
            df_normalized = pd.DataFrame()
            for new_file in os.listdir(str(os.getcwd() + f"/{folder}/")):
                df_intensity = pd.DataFrame()
                df_intensity = pd.read_csv(str(os.getcwd() + f"/{folder}/" + new_file), delim_whitespace=True)
                df_intensity.columns = ["angle", new_file[:-4]]
                # df_intensity.drop('index', axis=1, inplace=True)
                df["intensity_" + new_file[:-4]] = df_intensity[new_file[:-4]]

                del df_intensity

            angle = pd.DataFrame()
            angle = pd.read_csv(str(os.getcwd() + f"/{folder}/" + new_file[:-5] + "1" + new_file[-4:]), delim_whitespace=True)
            angle.columns = ["angle", "intensity"]
            df["_angle"] = angle["angle"]

            df = df.reindex(sorted(df.columns), axis=1)

            with open(str(os.getcwd()) + f"/{folder}/unique_file.asc", 'a') as f:
                f.write(df.to_string(index=False))

            print("The files were created!")
        procede = str(input("\nDo you want to continue: \n")).lower()


# For the case where the file is cut

    elif (decision.lower() in "yes"):
        start = int(input("Start line: "))
        finish = int(input("Finish line: "))
        folder = str(start) + "-" + str(finish) + "_lines"
        os.mkdir(folder)
        for filename in os.listdir(os.getcwd()):
            if filename[-4:] == first_extension:
                with open(filename) as file_a:
                    lines = file_a.readlines()[start-1:finish]
                    with open(f"./{folder}/" + filename[:-4] + second_extension, mode="w") as file_b:
                        file_b.writelines(lines)
        print(f"\nFiles cut and converted to {folder} folder\n")

# Joining the file in one from cut files
        join = str(
            input("Do you want to join the files in one unique file: [Y/N]")).lower()
        if "y" in join:

            df = pd.DataFrame()
            df_indiv_normal = pd.DataFrame()
            df_normalized = pd.DataFrame()
            for new_file in os.listdir(str(os.getcwd() + f"/{folder}/")):
                df_intensity = pd.DataFrame()
                df_intensity = pd.read_csv(str(os.getcwd() + f"/{folder}/" + new_file), delim_whitespace=True)
                df_intensity.columns = ["angle", new_file[:-4]]
                df["intensity_" + new_file[:-4]] = df_intensity[new_file[:-4]]

                del df_intensity

            angle = pd.DataFrame()
            angle = pd.read_csv(str(os.getcwd() + f"/{folder}/" + new_file[:-5] + "1" + new_file[-4:]), delim_whitespace=True)
            angle.columns = ["angle", "intensity"]
            df["_angle"] = angle["angle"]

            df = df.reindex(sorted(df.columns), axis=1)

            with open(str(os.getcwd()) + f"/{folder}/unique_file.asc", 'a') as f:
                f.write(df.to_string(index=False))
            with open(str(os.getcwd()) + f"/{folder}/unique_file_individual_normalized.asc", 'a') as g:
                g.write(df_indiv_normal.to_string(index=False))
            with open(str(os.getcwd()) + f"/{folder}/unique_file_normalized.asc", 'a') as h:
                h.write(df_normalized.to_string(index=False))
            print("The files were created!")
        procede = str(input("\nDo you want to continue: \n")).lower()

print("\n\nOk, BYE!\n\n")
