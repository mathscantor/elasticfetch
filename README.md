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
### Setting parameters in configuration file
Edit **elasticfetch.ini** and set it to the correct : <br>
- Protocol (`https` or `http`)
- IP address (`XXX.XXX.XXX.XXX` or `domain name`)
- port (Usually `9200`)
- username (Must have *enough privilege* to use APIs)
- password 

### Running elasticfetch
```sh
python3 elasticfetch.py
```
```text
===============================================================
        _              _    _         __       _         _     
       | |            | |  (_)       / _|     | |       | |    
   ___ | |  __ _  ___ | |_  _   ___ | |_  ___ | |_  ___ | |__  
  / _ \| | / _` |/ __|| __|| | / __||  _|/ _ \| __|/ __|| '_ \ 
 |  __/| || (_| |\__ \| |_ | || (__ | | |  __/| |_| (__ | | | |
  \___||_| \__,_||___/ \__||_| \___||_|  \___| \__|\___||_| |_|

    Developed by: Gerald Lim Wee Koon (github: mathscantor)    
===============================================================

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

### Option 1 - Show indices status
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

### Option 2 - Set current index
```text
Listing all beats indices:

1 -- .internal.alerts-security.alerts-default-000001
2 -- .internal.alerts-security.alerts-default-000002
3 -- .internal.alerts-security.alerts-default-000003
4 -- .internal.alerts-security.alerts-default-000004
5 -- .internal.alerts-security.alerts-default-000005
6 -- .items-default-000001
7 -- .lists-default-000001
8 -- auditbeat-8.0.1
9 -- auditbeat-8.1.0
10 -- auditbeat-8.1.2
11 -- filebeat-7.15.2-2022.03.11-000001
12 -- filebeat-7.15.2-2022.04.10-000002
13 -- filebeat-7.15.2-2022.05.10-000003
14 -- filebeat-7.15.2-2022.06.09-000004
15 -- filebeat-7.15.2-2022.07.09-000005
16 -- filebeat-8.0.1
17 -- filebeat-8.1.0
18 -- filebeat-8.1.2
19 -- metrics-endpoint.metadata_current_default
20 -- packetbeat-8.0.1
21 -- packetbeat-8.1.0
22 -- packetbeat-8.1.2
23 -- winlogbeat-8.0.1

Enter your index choice: 23
```
In the above example, I have chosen the winlogbeat-8.0.1 index.
Once you have chosen your index, it will be shown that you are fetching from that particular index

### Option 3 - Set main timestamp

The main timestamp field name will be used in sorting the timestamps in ascending order. 
Option 3 allows you to set a new main timestamp field name from the displayed 'ALL RELATED FIELDS' column.
```text
 [SUCCESS] Showing available fields...


TOP LEVEL PARENT               TYPE       ALL RELATED FIELDS            
----------------               ----       ------------------            
@timestamp                     date       @timestamp                    

event                          date       event.created, event.ingested 

winlog                         date       winlog.event_data.ClientCreationTime, winlog.event_data.DeviceTime, winlog.event_data.NewTime, winlog.event_data.OldTime, winlog.event_data.ProcessCreationTime, winlog.event_data.StartTime, winlog.event_data.StopTime, winlog.user_data.UTCStartTime

Main Timestamp Name: @timestamp
Timestamp Type: epoch
```
In this example, option 3 will show you all related fields that are of 'date' type. <br>

The default main timestamp field is @timestamp as elasticsearch uses this field universally for referencing time. <br>

However, I am aware that certain users / organization do rename '@timestamp' to something else. Therefore, I have added this feature to support existing organizations that require this. <br>

In addition, I have given the liberty to the user to choose between timestamp types:
1. 'date' <br>
format: <br>
(`YYYY-MM-DD`T`HH:mm:ss`) - smallet unit in seconds - eg. `2022-05-01T00:00:00`
2. 'epoch' format: <br>
(`10 digit number`) -  

```text
Current index selected: winlogbeat-8.0.1
Main Timestamp Field:  @timestamp
Main Timestamp Type:  epoch

1 -- Show indices status
2 -- Set current index
3 -- Set main timestamp
4 -- Show available field names
5 -- Fetch data between two timestamps
6 -- Exit
Enter your choice: 
```

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


