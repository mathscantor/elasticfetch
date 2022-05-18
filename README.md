# elasticfetch
Elasticfetch is a simple tool to fetch more than 10,000 data entries from elasticsearch. <br />
Fetching data out of elasticsearch is tough but there are numerous workarounds with their APIs. <br />
However, it is a rather manual process to do CURL commands each time you need to fetch some data. <br />
Thus, this tool helps to eliminate the tedious process of getting data out of elasticsearch.

## Required Python Packages
```sh
pip3 install requests
```

## Current Features
1. Show index health status
2. Setting Index to fetch from
3. Fetching data between timestamps

## How to use
### Step 1 - Setting parameters in configuration file
Edit elasticfetch.ini and set it to the correct : <br />
- IP address 
- port 
- username 
- password 

### Step 2 - Running elasticfetch
```sh
python3 elasticfetch.py
```
![alt text](./screenshots/main_menu.png)

### Step 3 (Optional) - Listing indices status
![alt text](./screenshots/indices_status.png)

### Step 4 - Choosing your index to get data from.
![alt text](./screenshots/setting_index.png) <br />
In the above example, I have chosen the winlogbeat-8.0.1 index.
Once you have chosen your index, it will be shown that you are fetching from that particular index
### Step 5 - Fetching data from a chosen index.
Select option 3 in the main menu. <br />
![alt text](./screenshots/option_3.png) <br />
This will prompt you for:
- start timestamp
- end timestamp
- number of logs you want to fetch in this time period.
- field names to select (Look at kibana dashboard to know what is available)

![alt text](./screenshots/step5-2.png) <br />
A successful fetch would result in the following success messages and elasticfetch 
will prompt you for a file name to dump the data in. <br />
All saved files will be found under the **datasets** folder


