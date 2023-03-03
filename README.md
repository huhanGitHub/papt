# Papt

Papt is a pairwise GUI dataset between Android phones and tablets. The detail introduction about this dataset is in the `dataset` directory. 
This dataset includes pairwise phone-tablet GUIs.
Current dataset is avaliable at [Papt](https://drive.google.com/drive/folders/1a7IuofYFwntbjFkIjWDE05qvMFJGXtyF?usp=sharing).

The 'dataset' directory contain pair examples and more introduction.

### Data Source
We first crawl 6,456 tablet apps from Google Play.
Then we match their corresponding phone apps by their app names and app developers.
Finally, we collect 5,593 valid phone-tablet app pairs from 22 app categories.



### Data Collection

First, we dynamically adjust the resolution of the device to match GUI pairs. 
![image](https://user-images.githubusercontent.com/9078829/222718086-7af79fdb-0537-4d7a-9277-cd7ea7e10205.png)



Second, we compare the similarities of two GUIs from phones and tablets and match two GUIs with high similarity.
![image](https://user-images.githubusercontent.com/9078829/222718147-98d1c20e-84dc-4913-8a6a-74867bd490a0.png)


The `tools` directoty contains data collection tools. You may see the introduction in this directory.
We open source two tools: Adjust resolution collector and GUI Explorer and similarity comparer.

### Pair format

Currently, we have about 10,000 phone-tablet GUI pairs now.

<img width="459" alt="image" src="https://user-images.githubusercontent.com/9078829/222717542-07412c06-6393-4046-b03a-8de0af488ca7.png">

This figure shows an example of pairwise GUI pages of the app 'Spotify' in our dataset.
All GUI pairs in one phone-tablet app pair are placed in the same directory.
Each pair consists of four elements: a screenshot of the GUI running on the phone ('phone_1676189565_MainActivity.png'), the metadata data corresponding to the GUI screenshot on the phone ('phone_1676189565_MainActivity.xml'), a screenshot of the GUI running on the tablet ('tablet_1676189565_MainActivity.png'
), and the metadata data corresponding to the GUI screenshot on the tablet ('tablet_1676189565_MainActivity.xml').
The naming format for all files in the dataset is 'Device_Timestamp_Activity' Name.
As shown in Figure, The filename tablet_1676189565_-MainActivity.xml indicates that this file was obtained by the tablet and was collected with the timestamp '1676189565', this GUI belongs to 'MainActivity' and this file is a metadata file in XML format.
We use timestamps and activity names to distinguish phone-tablet GUI pairs.


### Source Paper
We describe all the details in our source paper. You can refer to this paper to get more details. 

'paper link.. show soon'



