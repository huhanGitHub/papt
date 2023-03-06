# About Our dataset Papt

This dataset includes pairwise phone-tablet GUIs.
Current dataset is available at [Papt](https://drive.google.com/drive/folders/1a7IuofYFwntbjFkIjWDE05qvMFJGXtyF?usp=sharing).

In directory `pair_examples`, there are same GUI pair examples.
We will dynamically update the newly collected data.

## Folder structures

All GUI pairs of the same app are placed in the same directory with its `app_id` (provided by Google Play Store) as the folder name.
For example, pairs of the BBC News application is under folder `bbc.mobile.news.ww`.

Each pair consists of four elements: a screenshot of the GUI running on the phone, the metadata data corresponding to the GUI screenshot on the phone, a screenshot of the GUI running on the tablet, and the metadata data corresponding to the GUI screenshot on the tablet.
Each pair has four files (png and XML for both phone and tablet) with file name pattern `<pair_id>_<device_type>_<activiey_name>.<file_type>`. `pair_id` is a timestamps we used to
uniquely identify each pair.

For example, the first pair we collected of the BBC News application has

- 1658671579_phone_TopLevelActivity.png
- 1658671579_phone_TopLevelActivity.xml
- 1658671579_tablet_TopLevelActivity.png
- 1658671579_tablet_TopLevelActivity.xml

## File structures

XML files contain the entire UI object captured by `uiautomator2` at runtime. Each node in the object contained necessary attributes such as `class`(describe a UI object's type) and `bounds`(describe size and location of an UI element). PNG files are also provided for visual comparison and debugging purposes.

Note that there is a one-to-many correlation between `class` and actual type label (e.g., BUTTON, IMAGE, CHECKBOX, which describe an UI element's semantic type). Refer to `tools/color_map.py` for more detail.

The entire data collection pipeline is the following:

1. Using `scraper.js` to scrap apps from the google app store and save it to file `apps.json` (mainly to get `app_id` for downloading).
2. Use `download_apks.py` to download. Note [apkeep](https://github.com/EFForg/apkeep) is required.
3. Update necessary variables inside `definitions.py`.
4. Run `adjust_collector.py` to collect the data.

## Loading and preprocess

There are some scripts may help you load and preprocess data in `tools` directory. Please the comments in these scripts.

In `grouping.py`, there are scripts for grouping isolated GUI components.

In `color_map.py` and `data_prepare.py`, there are some scripts for drawing the wireframe of GUI pages and load XML metadata

In `run_preprocess.py`, we provide scripts to inject deeplinks into APKs to improve the explore coverage.

## app ids examples

The `apps.json` contains an example file produced by `scraper.js`.

Please cite our paper if you use the dataset:
....
