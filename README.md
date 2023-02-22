# Adjust resolution collector
 `python adjust_collector.py`
 
#### NOTE
- resolution and orientation
    - if device x-axis is at longer side (i.e Device().infoand some at shorter side
2. larger numer of apks

# GUI Explorer and similarity comparer

We currently only publish the code for GUI exploration and collection. The code for the GUI similarity comparison will be integrated into the tool later due to some reasons of the collaborators.

Step 1: install required packages in the requirement.txt
`pip install -r requirement.txt`

Step 2:
set the following configuration of this test in the `dynamic_testing/dynamic_GUI_testing.py`：

```python
deviceId = '192.168.57.105'
apk_path = r'../data/repackaged_apks/youtube.apk'
atg_json = r'../data/activity_atg/youtube.json'
deeplinks_json = r'../data/deeplinks/youtube.json'
log = r'../data/visited_rate/youtube.txt'
```
 Then, run this script to explore apps.
 
 We provide two pre-injected example apps: youtube and EZ explorer in the data/repackaged_apks.
 Note that the apks are all pre-injected into deeplinks and extracted intent parameters and atg in the deeplinks_json and atg_json.
 There may be unpredictable issues, so pls run each app multiple times.
 Pre-login and granting permission in advance will improve the effectiveness of app exploration.
 The code here is not the latest version, but it can still achieve state-of-the-art to explore Android actvities.


# About Our dataset Papt

Current dataset is avaliable at [Papt](https://drive.google.com/drive/folders/1a7IuofYFwntbjFkIjWDE05qvMFJGXtyF?usp=sharing)

The dataset includes pairwise phone-tablet GUIs. 

All GUI pairs in one phone-tablet app pair are placed in the same directory.
Each pair consists of four elements: a screenshot of the GUI running on the phone, the metadata data corresponding to the GUI screenshot on the phone, a screenshot of the GUI running on the tablet, and the metadata data corresponding to the GUI screenshot on the tablet.
Each pair has four files (png and XML for both phone and tablet), which are located at `data/<app_id>/` with file name pattern `<pair_id>_<device_type>_<activiey_name>.<file_type>`.
The naming format for all files in the dataset is Device_Timestamp_Activity Name.
We use timestamps and activity names to distinguish phone-tablet GUI pairs.

Type labels (e.g., BUTTON, IMAGE, CHECKBOX) that describe a UI object's semantic type on Android app screenshots.

XML files contain the entire UI object captured by `uiautomator2` at runtime. Each node in the object contained necessary attributes such as `class` and `bounds`. PNG files are also provided for visual comparison and debugging purposes.

The entire data collection pipeline is the following:
1. Using `scraper.js` to scrap apps from the google app store and save it to file `apps.json` (mainly to get'add_id` for downloading).
2. Use `download_apks.py` to download. Note [apkeep](https://github.com/EFForg/apkeep) is required.
3. Update necessary variables inside `definitions.py`.
4. Run `adjust_collector.py` to collect the data.

# Loading and preprocess
In `grouping.py`, there are scripts for grouing isolated GUI compoennts.
In `color_map.py` and `data_prepare.py`, there are some scripts for drawing the wireframe of GUI pages and load XML metadata

# pair examples
In directory `pair_example`, there are same GUI pair examples.


Please cite our paper if you use the dataset:
....
