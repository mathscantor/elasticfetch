# elasticfetch
Elasticfetch is a simple tool to fetch more than 10,000 data entries from elasticsearch. <br />
Fetching data out of elasticsearch is tough but there are numerous workarounds with their APIs. <br />
However, it is a rather manual process to do CURL commands each time you need to fetch some data. <br />
Thus, this tool helps to eliminate the tedious process of getting data out of elasticsearch.

## Required Python Packages
```sh
pip3 install requests
pip3 install tqdm
```

## Current Features
1. Show index health status
2. Setting Index to fetch from
3. Fetching data between timestamps

## How to use
### Step 1 - Setting parameters in configuration file
Edit **elasticfetch.ini** and set it to the correct : <br />
- IP address 
- port (Usually, it is 9200)
- username 
- password 

### Step 2 - Running elasticfetch
```sh
python3 elasticfetch.py
```
```text
Current index selected:  N/A (Please set an index before fetching any data!)
Main Timestamp Field:  @timestamp
Main Timestamp Type:  date

1 -- Show indices status
2 -- Set current index
3 -- Set main timestamp
4 -- Show available field names
5 -- Fetch data between two timestamps
6 -- Exit
```

### Step 3 (Optional) - Show indices status
```text
health status index                                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   .internal.alerts-security.alerts-default-000001 ######################   1   1       1094            0      3.7mb          3.7mb
yellow open   .internal.alerts-security.alerts-default-000002 ######################   1   1        213            0      1.5mb          1.5mb
yellow open   .internal.alerts-security.alerts-default-000003 ######################   1   1        264            0      1.5mb          1.5mb
yellow open   .internal.alerts-security.alerts-default-000004 ######################   1   1        237            0      2.2mb          2.2mb
yellow open   .internal.alerts-security.alerts-default-000005 ######################   1   1         33            0    614.5kb        614.5kb
yellow open   .items-default-000001                           ######################   1   1          0            0       225b           225b
yellow open   .lists-default-000001                           ######################   1   1          0            0       225b           225b
yellow open   auditbeat-8.0.1                                 ######################   1   1   40024180            0     25.9gb         25.9gb
yellow open   auditbeat-8.1.0                                 ######################   1   1   12285275            0      7.9gb          7.9gb
yellow open   auditbeat-8.1.2                                 ######################   1   1    4298254            0      3.1gb          3.1gb
yellow open   filebeat-7.15.2-2022.03.11-000001               ######################   1   1       1008            0    455.6kb        455.6kb
yellow open   filebeat-7.15.2-2022.04.10-000002               ######################   1   1          0            0       225b           225b
yellow open   filebeat-7.15.2-2022.05.10-000003               ######################   1   1          0            0       225b           225b
yellow open   filebeat-7.15.2-2022.06.09-000004               ######################   1   1          0            0       225b           225b
yellow open   filebeat-7.15.2-2022.07.09-000005               ######################   1   1          0            0       225b           225b
yellow open   filebeat-8.0.1                                  ######################   1   1   15815910            0        9gb            9gb
yellow open   filebeat-8.1.0                                  ######################   1   1   22087647            0     13.6gb         13.6gb
yellow open   filebeat-8.1.2                                  ######################   1   1    6655497            0      4.1gb          4.1gb
green  open   metrics-endpoint.metadata_current_default       ######################   1   0          0            0       225b           225b
yellow open   packetbeat-8.0.1                                ######################   1   1  215773987            0     92.1gb         92.1gb
yellow open   packetbeat-8.1.0                                ######################   1   1   21195763            0      9.8gb          9.8gb
yellow open   packetbeat-8.1.2                                ######################   1   1   52814104            0     20.8gb         20.8gb
yellow open   winlogbeat-8.0.1                                ######################   1   1  102336389            0    103.9gb        103.9gb
```

### Step 4 - Choosing your index to get data from.
```text

```
In the above example, I have chosen the winlogbeat-8.0.1 index.
Once you have chosen your index, it will be shown that you are fetching from that particular index
### Step 5 - Fetching data from a chosen index.
Select option 3 in the main menu. <br />
![Fetching Data Example](./screenshots/option_3.png "Fetching Data Example") <br />
This will prompt you for:
- start timestamp
- end timestamp
- number of logs you want to fetch in this time period.
- field names to select (Look at kibana dashboard to know what is available)
- filtering your queries by specifying (FIELD FILTER_KEYWORD VALUE;)

Current Supported Filter Keywords:
- is_not_gte
- is_not_lte
- is_not_gt
- is_not_lt
- is_not
- is_gte
- is_lte
- is_gt
- is_lt
- is

At the end, it will prompt you for a file name to dump the data in (Currently only support .json, .csv). <br />
All saved files will be found under the **datasets** folder


