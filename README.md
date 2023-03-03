# Papt

Papt is a pairwise GUI dataset between Android phones and tablets. The detail introduction about this dataset is in the `dataset` directory. 

This dataset includes pairwise phone-tablet GUIs.
Current dataset is avaliable at [Papt](https://drive.google.com/drive/folders/1a7IuofYFwntbjFkIjWDE05qvMFJGXtyF?usp=sharing).

## data source
We first crawl 6,456 tablet apps from Google Play.
Then we match their corresponding phone apps by their app names and app developers.
Finally, we collect 5,593 valid phone-tablet app pairs from 22 app categories.
Thsi table shows the disctribution of data source apps.
![image](https://user-images.githubusercontent.com/9078829/222712905-f2ab3dad-c87e-4fda-bb5d-bdcc49861995.png)




# Data Collection


The `tools` directoty contains data collection tools. You may see the introduction in this directory.

We open source two tools: Adjust resolution collector and GUI Explorer and similarity comparer.
