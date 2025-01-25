# NIST-SRD-46-Dataset-Explorer

Streamlit app: https://nist-srd-46.streamlit.app/

The NIST SRD 46 dataset contains imprtoant information about a range of important metals and ligands. The dataset is a great resource for many chemists and electrochemists. However, the database has been discontinued since around 2006 and there are no official apps that can be used to explore and visualize the dataset. Dr. Hatada from Kyoto University has created a Sqlite batabase for the SRD-46 dataset and also created a handy app called "Stability Constant Explorer" to explore the database which can be found [here](https://github.com/n-hatada/stability-constant-explorer). While useful for visualization, Dr. Hatada's Stability Constant Explorer app and the Sqlite database can be cumbersome for automatic exploration for machine learning purposes and do not work on all operating systems. 

Here, the database used for Stability Constant Explorer app is cleaned and is provided as a csv file (gzip compressed) with all the references in the same table. A streamlit app is created on top of the csv file that provides the same functionality as the Stability Constant Explorer app. The app is hosted online, so no installation is required and the database can be explored from any platform (Linux, Mac, or Windows). Having the references in the same table as a column enables automated scraping of the journal articles.

Note, the database files in this repo are gzipped due to Github's file size restrictions. These files can be easily decompressed to get the csv file. You can use any gzip decompresser app/software. Or, you can use Python.

```python
df = pd.read_csv("db_clean_gzip_compressed", compression='gzip')
df.to_csv('db_clean.csv', index=False) 
```
After you decompress the gzip compressed files to a csv file, you can use any text editor or Excel to look at the csv file. For Excel, you may need to change the encoder to see the proper text since the csv database here uses utf-8 unicode characters. A possible way to change the encoder in Excel can be found [here](https://support.microsoft.com/en-us/office/choose-text-encoding-when-you-open-and-save-files-60d59c21-88b5-4006-831c-d536d42fd861)

Check out the [streamlit app](https://nist-srd-46.streamlit.app/)!
