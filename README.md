## Scraping Pipeline
This is part of project Kedaireka UMKM Dian Nuswantoro University Center of Excellence 2023 as Data Engineer

## Data Source
From this automatic scraping program, in the first program, the data comes from the Basic Material Price Comparison table (https://sp2kp.kemendag.go.id/), and in the second program, the data comes from the news website (https:// business.com/) with keywords that can be adjusted to your needs

### Libraries
The scraping program that has been created uses the Selenium and BeautifulSoup libraries for each website destination

## How the Program Works?
This following program, works like the flow below :
1. Airflow triggerer will carry out the task of running this DAG scraping pipeline to run the program based on the scheduler
2. The scraping program will carry out its duties to extract information on the destination website
3. The extracted data will be transformed into a .csv file
4. Next, the data is stored in XComs for communication between instances
5. Data is stored in each destination table in the database system
6. The data is ready to be used for the machine learning process

## Conclusion
In conclusion, this scraping pipeline project demonstrates the application scraping program automated to collect data from various websites. Through the implementation and evaluation of these program, we gain insight into the application of scraping programs combined with Orchestration Tools (Apache Airflow) to meet the needs of external data that can be used for Machine Learning program datasets such as Predictions, Topic Classification, and Sentiment Analysis. The findings from this project can contribute to further research and decision-making processes in the field of Big Data Pipeline

## Addition
Our research regarding the application of scraping pipeline in the Big Data Pipeline environment can be read in the paper below :
https://ejournal.undip.ac.id/index.php/transmisi/article/view/59003
https://doi.org/10.14710/transmisi.26.1.48-54
