# Papt

Papt is a pairwise GUI dataset between Android phones and tablets. The detail introduction about this dataset is in the `dataset` directory. 

This dataset includes pairwise phone-tablet GUIs.
Current dataset is avaliable at [Papt](https://drive.google.com/drive/folders/1a7IuofYFwntbjFkIjWDE05qvMFJGXtyF?usp=sharing).

## data source
We first crawl 6,456 tablet apps from Google Play.
Then we match their corresponding phone apps by their app names and app developers.
Finally, we collect 5,593 valid phone-tablet app pairs from 22 app categories.



# Data Collection

First, we dynamically adjust the resolution of the device to match GUI pairs. 
![image](https://user-images.githubusercontent.com/9078829/222715144-6ccb4627-b2de-40ef-baf8-c6df13958c09.png)


Second, we compare the similarities of two GUIs from phones and tablets and match two GUIs with high similarity.
![image](https://user-images.githubusercontent.com/9078829/222715223-90a2b8c0-96d5-473e-86b1-2f6a196c98b4.png)



The `tools` directoty contains data collection tools. You may see the introduction in this directory.
We open source two tools: Adjust resolution collector and GUI Explorer and similarity comparer.


