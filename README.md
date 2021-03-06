# elasticfetch - overview
Elasticfetch is a simple tool to export huge amounts of data from elasticsearch. <br>

Currently, this tool is not reliant on the `scroll API` and in the event where elasticsearch decides to discontinue the support for `scroll API`, this tool will remain to function properly. <br>

This tool aims to facilitate work flow of threat hunting and data analysis in the event where you need to query huge amount of data without killing the server.
## Required Python Packages
```sh
pip3 install requests
pip3 install tqdm
```

## Current Features
1. Show index health status
2. Setting Index to fetch from
3. Set main timestamp (This field will be used to sort your data in chronological order)
4. Showing available field names related to your index (**Not Hardcoded**)
5. Fetching data between two timestamps

## How to use
### Setting parameters in configuration file
Edit **elasticfetch.ini** and set the following variables to your own values : <br>
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

<!-- Output copied to clipboard! -->

<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.389 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0??33
* Fri Jul 22 2022 03:51:52 GMT-0700 (PDT)
* Source doc: Untitled document
* Tables are currently converted to HTML tables.
----->
<table>
  <tr>
   <td>Type
   </td>
   <td>Supported Formats
   </td>
   <td>Smallest Unit
   </td>
   <td>Examples
   </td>
  </tr>
  <tr>
   <td rowspan="2" >date
   </td>
   <td>&lt;%Y-%m-%d>T&lt;%H:%M:%S>
   </td>
   <td>seconds
   </td>
   <td>2022-05-01T00:00:00
   </td>
  </tr>
  <tr>
   <td>&lt;%Y-%m-%d>T&lt;%H:%M:%S.%f>Z
   </td>
   <td>milliseconds
   </td>
   <td>2022-05-01T00:00:00.000Z
   </td>
  </tr>
  <tr>
   <td rowspan="2" >epoch
   </td>
   <td>10 digit string
   </td>
   <td>seconds
   </td>
   <td>1420070400
   </td>
  </tr>
  <tr>
   <td>13 digit string
   </td>
   <td>milliseconds
   </td>
   <td>1420070400000
   </td>
  </tr>
</table>

### Option 4 - Listing all available fields within the current chosen index
It is a known grievance that the users have to manually check what fields are available to them. Option 4 allows users to list the whole shebang of fields.
```text
[SUCCESS] Showing available fields...


TOP LEVEL PARENT               TYPE       ALL RELATED FIELDS            
----------------               ----       ------------------            
@timestamp                     date       @timestamp                    

_data_stream_timestamp         NoType     _data_stream_timestamp        

_doc_count                     NoType     _doc_count                    

_feature                       NoType     _feature                      

_field_names                   NoType     _field_names

file                           text       file.code_signature.status, file.code_signature.subject_name, file.directory, file.extension, file.hash.md5, file.hash.sha256, file.name, file.path, file.pe.imphash
                               keyword    file.code_signature.status.keyword, file.code_signature.subject_name.keyword, file.directory.keyword, file.extension.keyword, file.hash.md5.keyword, file.hash.sha256.keyword, file.name.keyword, file.path.keyword, file.pe.imphash.keyword
                               boolean    file.code_signature.valid     

group                          text       group.domain, group.id, group.name
                               keyword    group.domain.keyword, group.id.keyword, group.name.keyword

host                           text       host.architecture, host.hostname, host.id, host.ip, host.mac, host.name, host.os.build, host.os.family, host.os.kernel, host.os.name, host.os.platform, host.os.type, host.os.version
                               keyword    host.architecture.keyword, host.hostname.keyword, host.id.keyword, host.ip.keyword, host.mac.keyword, host.name.keyword, host.os.build.keyword, host.os.family.keyword, host.os.kernel.keyword, host.os.name.keyword, host.os.platform.keyword, host.os.type.keyword, host.os.version.keyword
.
.
.
```


### Option 5 - Fetching data from a chosen index.
```text
Current index selected: winlogbeat-8.0.1
Main Timestamp Field:  @timestamp
Main Timestamp Type:  date

1 -- Show indices status
2 -- Set current index
3 -- Set main timestamp
4 -- Show available field names
5 -- Fetch data between two timestamps
6 -- Exit
Enter your choice: 5                                                                                ??? (Your input)

timestamp format: <%Y-%m-%d>T<%H:%M:%S> or <%Y-%m-%d>T<%H:%M:%S.%f>Z
eg. 2022-05-01T00:00:00 or 2022-05-01T00:00:00.000Z
Start Timestamp: 2022-05-01T00:00:00                                                                ??? (Your input)
End Timestamp: 2022-05-20T00:00:00                                                                  ??? (Your input)
Number of logs to retrieve: 50000                                                                   ??? (Your input)
Select your field names (eg. event.created,event.code,message): event.created, event.code, message  ??? (Your input)

Filter Format: <FIELD_NAME> <FILTER_KEYWORD> <VALUE>;
Supported Filter Keywords:
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

eg. event.code is_gt 4000; event.code is_lte 5000; event.category is authentication;                ??? (Your input)
(OPTIONAL - PRESS ENTER TO SKIP) Filter your queries: event.code is_gte 1000;
 [INFO] Fetching elastic data...
Fetch Progress: 100%|??????????????????????????????| 50000/50000 [01:26<00:00, 577.40it/s]
 [SUCCESS] Successfully fetched 50000 data entries!
File name to save as (.json, .csv): test.csv                                                        ??? (Your input)
 [INFO] Saving data to datasets/test.csv
 [SUCCESS] Successfully saved data to datasets/test.csv

```


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


