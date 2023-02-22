import os
import definitions

from static_analysis_apk.extract_atg import (
    activity_searching,
    activity_searching_one,
    unit_extract,
)
from static_analysis_apk.extract_intent_paras import (
    smali_intent_para_extractor,
    smali_intent_para_extractor_one,
)
from static_analysis_apk.instrument_apk import unit_inject
from static_analysis_apk.merge_deeplink_params import ParamGenerator


def unit_run_preprocess(
    app_save_dir, recompiled_apks, repackage_app_save_dir, deeplinks_path, save_dir
):
    if not os.path.exists(app_save_dir):
        print(app_save_dir, "not found")
        return

    # # recompile apk
    # print('recompile', apk_path)
    # unit_decpmpile(apk_path, app_save_dir)

    # instrument apk
    apk = app_save_dir[app_save_dir.rindex("/") + 1 :]
    repackage_app_save_apk = os.path.join(repackage_app_save_dir, apk) + ".apk"
    # if not os.path.exists(repackage_app_save_apk):
    #     os.mkdir(repackage_app_save_apk)
    unit_inject(app_save_dir, repackage_app_save_apk, deeplinks_path)

    # extract atg
    folders = os.listdir(recompiled_apks)
    ignore = [
        ".idea",
        ".git",
        "activity_match",
        "README.md",
        ".DS_Store",
        ".ipynb_checkpoints",
        "activity.py",
        "smalianalysis.py",
        "activity.py",
    ]
    folders = [x for x in folders if x not in ignore]

    available_activity_dict = activity_searching(folders, recompiled_apks)
    atg_save_dir = os.path.join(save_dir, "activity_atg")
    if not os.path.exists(atg_save_dir):
        os.mkdir(atg_save_dir)
    unit_extract(
        folder=app_save_dir,
        available_activity_dict=available_activity_dict,
        save_dir=atg_save_dir,
    )

    # extract intent parameters
    paras_save_path = os.path.join(save_dir, "intent_para.json")
    smali_intent_para_extractor(path=recompiled_apks, save_path=paras_save_path)

    # merge intent params and activity atgs
    params = ParamGenerator(paras_save_path)
    params.merge_deeplinks_params(deeplinks_path, paras_save_path)
    return repackage_app_save_apk


def unit_run_preprocess_one(
    decom_folder,
    repackaged_dir,
    deeplinks_path,
    paras_save_dir=None,
    atg_save_dir=definitions.ATG_DIR,
):
    if paras_save_dir is None:
        paras_save_path = os.path.join(decom_folder, "intent_para.json")

    pkg_name = os.path.basename(decom_folder)
    recompile_path = os.path.join(repackaged_dir, f"{pkg_name}.apk")

    # instrument apk
    unit_inject(decom_folder, recompile_path, deeplinks_path)

    available_activity_dict = activity_searching_one(decom_folder)
    unit_extract(
        folder=decom_folder,
        available_activity_dict=available_activity_dict,
        save_dir=atg_save_dir,
    )

    # extract intent parameters
    smali_intent_para_extractor_one(decom_folder, paras_save_path)

    # merge intent params and activity atgs
    params = ParamGenerator(paras_save_path)
    params.merge_deeplinks_params(deeplinks_path, deeplinks_path)
    return recompile_path


if __name__ == "__main__":

    # fixed results path, change once
    repackage_app_save_dir = r"data/repackaged_apks"
    deeplinks_path = r"data/deeplinks_params.json"
    save_dir = r"data"
    recompiled_apks = r"data/recompiled_apks"

    # decompiled apk source files, change test cases here
    app_save_dir = r"data/recompiled_apks/youtube"

    unit_run_preprocess(
        app_save_dir, recompiled_apks, repackage_app_save_dir, deeplinks_path, save_dir
    )
