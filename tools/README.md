# Adjust resolution collector
 `python adjust_collector.py`

Please change relavent constant variables in `./definitions.py`
before run the collector.

The entire data collection pipeline is the following:
1. Using `scraper.js` to scrap apps from the google app store and save it to file `apps.json` (mainly to get'add_id` for downloading).
2. Use `download_apks.py` to download. Note [apkeep](https://github.com/EFForg/apkeep) is required.
3. Update necessary variables inside `definitions.py`.
4. Run `adjust_collector.py` to collect the data.

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

# Loading and preprocess
In `grouping.py`, there are scripts for grouing isolated GUI compoennts.


In `color_map.py` and `data_prepare.py`, there are some scripts for drawing the wireframe of GUI pages and load XML metadata


in `run_preprocess.py`, we provide scripts to inject deeplinks into APKs to improve the explore coverage.




