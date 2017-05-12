# Boulder-2016-Bike-Share

## Project Summary
This project was undertaken to fulfill one of the two Capstone projects required by [SpringBoard.com](https://springboard.com). It explores the Boulder 2016 Bike Share Trips dataset and follows up with regression and classification analytics deploying several popular machine learning algorithms.

## Project Files
The following project files are located in this project directory:

[README.md](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/README.md) -- This document, with project description.

[Boulder 2016 Bike Share Capstone Project Proposal](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/Boulder%202016%20Bike%20Share%20Capstone%20Project%20Proposal.pdf) - Project Proposal.

[Boulder 2016 Bike Share Data Exploration.md](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/Boulder%202016%20Bike%20Share%20Data%20Exploration.md) - Final Project Report.

[Boulder 2016 B-cycle](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/Boulder%202016%20B-cycle.pdf) - Slide Deck.

[Denver 2016 Excel to CSV File Conversion](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver_2016_Excel_to_CSV_File_Conversion.ipynb) -- Converts the Trips dataset Excel spreadsheet from a hefty 27MB file size to a reasonable 6MB compressed file.

[Denver Bike Share Distance Duration Submit](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver_Bike_Share_Distance_Duration_Submit.py) - Python 3.6 script to retrieve distances between checkout and return kiosks from [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/).

[Denver Daily Forecast 2016](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver_Daily_Forecast_2016.py) - Python 2.7 script used to retrieve daily weather attributes from [Dark Sky API](https://darksky.net/dev/).

[Denver Hourly Forecast 2016](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver_Hourly_Forecast_2016.py) - Python 2.7 script used to retrieve hourly weather attributes from [Dark Sky API](https://darksky.net/dev/).

[Denver 2016 Bike Share Weather Data Consolidation](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver%202016%20Bike%20Share%20Weather%20Data%20Consolidation.ipynb) - Merges the daily and hourly weather attributes from [Dark Sky API](https://darksky.net/dev/) into the Trips dataset.

[Denver 2016 Bike Share Data Exploration](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver%202016%20Bike%20Share%20Data%20Exploration.ipynb) - Jupyter notebook containing Python code used to explore and visualize the information contained in the Denver 2016 Trips dataset. 

[Denver 2016 Bike Share Regression Modeling](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver%202016%20Bike%20Share%20Regression%20Modeling.ipynb) - Jupyter notebook containing Python code used to deploy a variety of regression models to train and test the Trips dataset followed by a predcition on 10 unseen samples. The regression models include Linear, Lasso, Ridge, Bayesian Ridge, Decision Tree, Random Forest, Extra Trees and Nearest Neighbors. 

[Denver 2016 Bike Share Multi-Class Classification Modeling](https://github.com/hbhasin/Capstone-Project-1/blob/master/Denver%202016%20Bike%20Share%20Multi-Class%20Classification%20Modeling.ipynb) - Jupyter notebook containing Python code used to deploy a variety of classification models to train and test the Trips dataset followed by a predcition on 10 unseen samples. The classification models include Logistic, Decision Tree, Random Forest, Extra Trees, Naive Bayes, Nearest Neighbors, Gradient Boosting and Multi-Layer Perceptron.

[./data](https://github.com/hbhasin/Capstone-Project-1/tree/master/data) - Folder containing data files used in the Python scripts and in the notebooks.

[./figures](https://github.com/hbhasin/Capstone-Project-1/tree/master/figures) - Folder containing figures used in the Python notebooks.


## Data Sources
[Denver B-cycle](https://www.denverbcycle.com/company) - The Trips dataset is located under [Denver B-cycle Trip Data](http://denver.bcycle.com/docs/librariesprovider34/default-document-library/2016denverbcycletripdata_public.xlsx?sfvrsn=2). The Kiosk dataset is located under [Denver B-Cycle Station Location Data](https://denver.bcycle.com/docs/librariesprovider34/default-document-library/october2016_kioskinfo.xlsx?sfvrsn=2).

Distances between Checkout and Return Kiosks: Distances were retrieved from [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/) using Python 3.6 script.

Weather Data: Retrieved from [Dark Sky API](https://darksky.net/dev/) using Python 2.7 scripts.

Geo-spatial Mapping: [Tableau](https://public.tableau.com/) was used to map the number of bike checkouts and returns by kiosks.

## Analysis Software
All data analyses were done in Python and with publicly available libraries using Jupyter Notebook and IDLE except for the geo-spatial mapping of the number of bike checkouts and returns by kiosks which was done using Tableau.

## Acknowlegements
The original plan was to use the Denver 2015 Trips dataset to continue the work by [Tyler Byers](https://github.com/tybyers/denver_bcycle). Fortunately, the 2016 dataset became available just in time for this project's undertaking. While there are certainly some differences between how the data were analyzed and reported by Denver B-Cycle and the author, credit must go to Denver B-Cycle for publishing its [2016 annual report](http://denver.bcycle.com/docs/librariesprovider34/default-document-library/dbs_annualreport_2016_05.pdf?sfvrsn=2) and posting the 2016 dataset for public consumption and for use in this project in a timely and professional manner. Credit also goes to my mentor, [Alex Chao](https://www.linkedin.com/in/alexchao56/) for his invaluable guidance and feedback on the progress of this project.Under construction
