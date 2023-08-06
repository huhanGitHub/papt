## Installation

Install required packages in the requirement.txt.
`pip install -r requirement.txt`

Note than you might need some optional tools if you need to download APKS. Please see `dataset/README.md` for more detail.

## Usage

### Adjust environment variables

Check all the variables inside `definitions.py`.
The `PHONE_ID` and `TABLET_ID` should be set to you devices' id, which
can be found using command `adb devices`. All APKs files should be placed under `APK_DIR`.

### Running the pipeline

The entire data collection pipeline is the following:

1. Using `scraper.js` to scrap apps from the google app store and save it to file `apps.json` (mainly to get `add_id` for downloading).
2. Use `download_apks.py` to download. Note [apkeep](https://github.com/EFForg/apkeep) is required.
3. Update necessary variables inside `definitions.py`.
4. Run `python adjust_collector.py` to collect the data.
   The `adjust_collector.py` is the entry point for the pipeline.
   Please change relevant constant variables in `./definitions.py` before run the collector.

### GUI Explorer and similarity comparer

We currently only publish the code for GUI exploration and collection. The code for the GUI similarity comparison will be integrated into the tool later due to some reasons of the collaborators (The reason is that a paper involving this tool has been rejected again and again, resulting in the unpublishable source code in the paper .....).

### Loading and preprocess

In `grouping.py`, there are scripts for grouping isolated GUI components.

In `color_map.py` and `data_prepare.py`, there are some scripts for drawing the wireframe of GUI pages and load XML metadata

In `run_preprocess.py`, we provide scripts to inject deeplinks into APKs to improve the explore coverage.

### testing

Set the following configuration of this test in the `dynamic_testing/dynamic_GUI_testing.py`:

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
