In this project I have created a data pipeline in airflow which send an email with list of five nearest holidays from four distinct countries.
The pipeline contain four tasks
1. check_source - makes sure that we can connect to api and get valid response
2. download_holidays - makes request to calendarific api and tranform data to create json file with five nearest holidays
3. check_file - look for json file that was created based on response in get_holidays function 
4. send_holidays - read json file and based on prepare message that will be send by email

Below you can see the pipeline in airflow 

![airflow pipeline](https://github.com/BartlomiejBogajewicz/get_holidays/blob/main/dags.PNG)
test
