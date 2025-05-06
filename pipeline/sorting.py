import pandas as pd
import os
import shutil

excel_path = ""
source_folder = ""
good_folder = ""
bad_folder = ""

df = pd.read_excel(excel_path, sheet_name="Sheet1")

#Add conditions here


def get_qc_status(row):
    if (
        row["coverslip_edge"] <  and
        row["nonwhite"]  and 
        row["dark"] and
        row["flat_areas"] and
        row["fatlike_tissue_removed_percent"] and
        row["small_tissue_filled_percent"] and
        row["blurry_removed_percent"] and
        row["template4_MSE_hist"] and
        row["tenenGrad_contrast"] and
        row["michelson_contrast"] and 
        row["rms_contrast"] and
        row["grayscale_brightness"] and
        row["grayscale_brightness_std"] and
        row["deconv_c0_mean"] and
        row["decon_c1_mean"] and
        row["deconv_c2_mean"]
    ):
        return "Pass"
    else:
        return "Fail"           
    

df["QC_Status"] = df.apply(get_qc_status, axis=1)

df.to_excel("result_with_qc_status.xlsx", index=False)


for _,row in df.iterrows():
    file_name = row["dataset:file_name"]
    qc_status = row["QC_Status"]
    
    source_path = os.path.join(source_folder, file_name)
    
    if qc_status == "Pass":
        destination_path = os.path.join(good_folder, file_name)
    else:
        destination_path = os.path.join(bad_folder, file_name)
    
    shutil.copy(source_path, destination_path)
    
    