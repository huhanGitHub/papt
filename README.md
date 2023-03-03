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
[alg1.pdf](https://github.com/huhanGitHub/papt/files/10881643/alg1.pdf)

Second, we compare the similarities of two GUIs from phones and tablets and match two GUIs with high similarity.

[alg2.pdf](https://github.com/huhanGitHub/papt/files/10881651/alg2.pdf)



The `tools` directoty contains data collection tools. You may see the introduction in this directory.
We open source two tools: Adjust resolution collector and GUI Explorer and similarity comparer.


