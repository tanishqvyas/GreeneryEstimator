**Folder Structure**
```
*
|--- data
|	|
|	|--- images
|	|	|
|	|	|--- roadmap
|	|	|--- satellite
|	|	
|	|--- csv
|	|	|
|	|	|--- greenery_percentage.csv
|	|	|--- sector_image.csv
|	|	
|	|--- dataset_loader.py
|	|--- create_image_csv.py
|	|--- create_greenery_percentage_csv.py
|
|
|--- README.md
|
```

**Executing with hadoop version 2.7.2**

Check status:  
```
jps
```

Navigate to Hadoop: 
```
cd /use/local/Hadoop
```
Copy input file to HDFS:  
```
hadoop fs -put /home/hduser/Documents/greenery_percentage.csv /input1
```

Navigate to hadoop streaming:  
```
cd share/hadoop/tools/lib
```
Execute MapReduce specifying all file paths:  
```
hadoop jar hadoop-streaming-2.7.2 jar \
-file /home/hduser/mapper.py \
-file /home/hduser/reducer.py \
-mapper /home/hduser/mapper.py \
-reducer home/hduser/reducer.py \
-input /input1 \
-output /greenery
```
