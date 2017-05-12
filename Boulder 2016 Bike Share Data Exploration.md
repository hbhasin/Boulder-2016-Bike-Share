# Boulder 2016 B-cycle Ridership Data Exploration and Predictive Analytics

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Splash.PNG)

[Boulder B-cycle](https://Boulder.bcycle.com/) is a nonprofit organization formed by Boulder residents to create and operate Boulder’s bike-sharing program on a not-for-profit, financially sustainable basis. Its mission is to “implement and operate a community-supported bike-share program that provides Boulder’s residents, commuters and visitors with an environmentally friendly, financially sustainable, and affordable transportation option that’s ideal for short trips resulting in fewer vehicle miles traveled, less pollution and congestion, more personal mobility and better health and wellness.”

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Boulder%20Header.PNG)

Boulder B-cycle posts its trips data set on its website as soon as its annual report is released. Trips data have been available since 2010. The 2016 annual report and its associated dataset for this report were obtained from [Boulder B-Cycle website](https://Boulder.bcycle.com/). 

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Boulder%202016%20Annual%20Report.PNG)

In his study, [Exploring 2014 Denver B-cycle Ridership](http://datawrangl.com/2016/02/21/denver-bcycle/), [Tyler Byers](https://www.linkedin.com/in/tylerbyers) determined that “most calendar and clock variables were highly significant when predicting ridership, and weather variables such as temperature and amount of cloud cover appear to be as well”. 

In his report, [Boulder B-cycle Data Analysis](https://rpubs.com/rpubsmonish/175792), [Monish Sunju Prabhakar](https://www.linkedin.com/in/monishsp) attempted to predict the type of membership pass using the Random Forest classification algorithm with three numeric attributes. 

This study will explore the publicly available 2016 Boulder B-cycle Trip Data and perform some predictive analytics on the number of bike checkouts using calendar, clock and weather variables as the predictors. The reporting style will follow the [Denver 2016 B-cycle Ridership Data Exploration and Predictive Analytics](https://github.com/hbhasin/Denver-2016-Bike-Share/blob/master/Denver%202016%20Bike%20Share%20Data%20Exploration.md) study to provide continuity and similarity.


This study has three parts:
1.	Explore the Trips datasets and visualize the data to provide useful and interesting information.
2.	Deploy a variety of regression models to train and test the data followed by a prediction on 10 unseen samples.
3.	Deploy a variety of classification models to train and test the data followed by a prediction on 10 unseen samples.

# Part 1: Data Exploration

## Data Acquisition

Data for this study was downloaded from several sources and combined using the following steps:
1. Downloaded Boulder B-cycle May 2011-January 2017 Trip Data from [Dropbox](https://www.dropbox.com/s/hk8csl6fm4q0221/Boulder%20B-cycle%20May%202011-January%202017%20Trip%20Data.xlsx?dl=0). The columns names were changed to comply with Python code best practices and only rows for 2016 were kept for this exercise.
2. Created a list of the 1849 combinations of the 43 checkout/return kiosks. Used [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/) to provide the bicycling distance and time between each checkout and return kiosk. Adopted Tyler’s method of finding the average distance by taking the distance from each checkout-return pair’s distance separately then averaging it. As he pointed out in his study, this approach was taken “because of the large number of one-way streets in the Boulder downtown area where the kiosks are highly clustered”. Google only supports a maximum of 2500 requests a day, so it took two days to obtain this data.
3. Obtained daily and hourly weather data via [Dark Sky API](https://darksky.net/dev/) for all of 2016. Dark Sky supports up to 1000 requests per day.


### Basic Ridership Statistics 
#### Number of Rides 
The B-cycle data, as downloaded, contained 419,611 rows of trips data. Under normal circumstances this would mean that 419,611 B-cycle trips were taken in 2016. However, the [2016 Boulder B-cycle annual report](http://denver.bcycle.com/docs/librariesprovider34/default-document-library/dbs_annualreport_2016_05.pdf) acknowledged just 94,446 total trips for the year. The breakdown was as follows:

Membership Type | Number of Trips
--------------- | -------------
Annual (Republic Rider) | 52,951
24-hour (Day Tripper) | 27,628
Monthly (People’s Pedaler) | 10,392
Pay-per-trip (Casual Cruiser) | 816
**Total Trips**	 | **91,787**


The Trips dataset reported 4 rows with NaN (Not A Number) entries. Removal of these 4 rows resulted in 113,724 rows with the following breakdown:

Membership Type | Number of Trips
--------------- | -------------
Annual (Republic Rider) | 57,042
24-hour (Day Tripper) | 28,948
Maintenance | 15,454
Monthly (People’s Pedaler) | 10,961
Pay-per-trip (Casual Cruiser) | 853
Semester (150-day) | 465
7-day | 1
**Total Trips** | **113,724**

Removing “Maintenance” entries brought the number of rows down to 98,270. Removing entries with a Trip Duration = 0 resulted in 96,101 rows.
Over 1.4% of the Boulder B-cycle rides (1343 rides) had the same checkout station as return station with a trip duration of only 1 minute (Figure 1). Again, Tyler’s explanation of why these trips should be removed from the dataset makes sense - “I believe these should be filtered out because I believe the majority of these “rides” are likely people checking out a bike, and then deciding after a very short time that this particular bike doesn’t work for them. I believe that most of the same-kiosk rides under 5 minutes or so likely shouldn’t count, but only culled the ones that were one minute long”.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%201.PNG)

<p align="center">
FIGURE 1: TRIP DURATION WHEN CHECKOUT AND RETURN KIOSKS ARE THE SAME
</p>

Removing entries with a Trip Duration = 1 resulted in 94,512 rows with the following breakdown:

Membership Type | Number of Trips
--------------- | -------------
Annual (Republic Rider) | 54,737
24-hour (Day Tripper) | 27,935
Monthly (People’s Pedaler) | 10,568
Pay-per-trip (Casual Cruiser) | 821
Semester (150-day) | 450
7-day | 1
**Total Trips** | **94,512**

This number appeared closer to the 94,446 trips reported by Boulder B-cycle although there were differences amongst the individual membership types.

There were 193 rows in the Trips dataset that had “Maintenance” entry in the Return Kiosk column. These 193 rows were removed accordingly.

Removing the 1,343 rows with a trip duration of 1 minute and 193 rows with invalid kiosk names resulted in **94,319 Boulder B-cycle rides in 2016**.

Membership Type | Number of Trips
--------------- | -------------
Annual (Republic Rider) | 54,610
24-hour (Day Tripper) | 27,889
Monthly (People’s Pedaler) | 10,549
Pay-per-trip (Casual Cruiser) | 821
Semester (150-day) | 449
7-day | 1
**Total Trips** | **94,319**

## Distance Traveled
To estimate the distance between checkout and return kiosks when they are the same, Tyler’s method of using the “average speed of all the other rides (nominal distance ridden divided by the duration), and then applying this average speed to the same-kiosk trip durations” was adopted. This resulted in 143,006 miles ridden in 2016 and sharply contrasted with the 229,071 miles reported by Boulder B-cycle. 

### Most Popular and Least Popular Checkout and Return Kiosks 
### Most Popular 
The following ten kiosks were the most popular checkout kiosks by number of total bike checkouts in 2016.

Checkout Kiosk | Number of Checkouts
-------------- | -------------------
115th & Pearl | 5443
13th & Spruce | 4272
Municipal Building | 3666
11th & Pearl | 3566
Folsom & Colorado | 3565
13th & Arapahoe | 3392
20th & Pearl | 3327
Broadway & Alpine | 3147
31st & Pearl | 2976
Broadway & Euclid | 2968

The most popular Checkout Kiosk to Return Kiosk routes were as follows:

Checkout Kiosk | Return Kiosk | Number of Trips
-------------- | ------------ | ---------------
13th & Spruce | Broadway & Alpine | 724
Broadway & Alpine | 13th & Spruce | 695
6th & Canyon | Municipal Building | 680
Municipal Building | 6th & Canyon | 641
20th & Pearl | 15th & Pearl | 604
Municipal Building | Municipal Building | 566
28th & Mapleton | 26th & Pearl | 552
Folsom & Pearl | 15th & Pearl | 529
13th & Arapahoe | 13th & Arapahoe | 506
15th & Pearl | 20th & Pearl | 503

The following ten kiosks were the most popular return kiosks by number of total bike checkouts in 2016.

Return Kiosk | Number of Returns
------------ | -------------------
115th & Pearl | 5366
13th & Spruce | 909
Municipal Building | 3919
13th & Arapahoe | 3898
11th & Pearl | 3737
29th & Pearl | 3260
21st & Arapahoe | 3178
14th & Canyon | 3102
20th & Pearl | 3055
Broadway & Alpine | 3040


### Least Popular 
The following ten kiosks were the least popular checkout kiosks by number of total bike checkouts in 2016.

Checkout Kiosk | Number of Checkouts
-------------- | -------------------
Broadway & Iris | 1328
13th & College | 1299
UCAR Center Green | 1227
9th & Pearl | 982
27th Way & Broadway | 678
33rd & Fisher | 648
Wilderness Place | 370
30th & Diagonal Highway | 247
30th & Marine | 159
Gunbarrel North | 120

The following ten kiosks were the least popular return kiosks by number of total bike returns in 2016.

Return Kiosk | Number of Returns
------------ | -------------------
Broadway & Iris | 1265
Broadway & University | 1070
9th & Pearl | 963
13th & College | 804
33rd & Fisher | 708
27th Way & Broadway | 509
Wilderness Place | 426
30th & Diagonal Highway | 263
30th & Marine | 170
Gunbarrel North | 114


## Map of Station Popularity
### Checkout Kiosks 

The use of Tableau aided in the creation of the following map showing the popularity of the various Checkout Kiosks (Figure 2). The size of the circle is proportional to the number of checkouts from that kiosk in 2016. 

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%202.PNG)

<p align="center">
FIGURE 2: CHECKOUT KIOSK LOCATIONS AND NUMBER OF CHECKOUTS IN 2016
</p>

### Return Kiosks 
Similarly, the use of Tableau aided in the creation of the following map showing the popularity of the various Return Kiosks (Figure 3). The size of the circle corresponds to the number of checkouts returned to that kiosk in 2016.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%203.PNG)

<p align="center">
FIGURE 3: RETURN KIOSK LOCATIONS AND NUMBER OF RETURNS IN 2016
</p>


## Checkouts per Membership Type 
With the revisions made earlier to the membership type entries, the figure below shows the breakdown:

Membership Type | Number of Checkouts
--------------- | -------------------
Annual (Republic Rider) | 54,610
24-hour (Day Tripper) | 27,889
Monthly (People’s Pedaler) | 10,549
Pay-per-trip (Casual Cruiser) | 821
Semester (150-day) | 449
7-day | 1




![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%204.PNG)


<p align="center">
FIGURE 4: NUMBER OF CHECKOUTS BY MEMBERSHIP TYPE IN 2016
</p>



## Ridership by Calendar and Clock Variables 
### Ridership by Hour 
Bike checkout time is probably the most important attribute in the Trips dataset. Each checkout time was converted into its integer hour. For example, 7:02 AM or 7:59 AM would be converted to an integer of 7. In this way, total number of checkouts could be aggregated for the year and plotted against their hours of the day, as shown in Figure 5.

It appears that the highest number of checkouts occur between 4 PM and 5 PM with ridership increasing steadily from 6 AM onwards.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%205.PNG)


<p align="center">
FIGURE 5: NUMBER OF CHECKOUTS BY HOUR IN 2016
</p>



Figure 6 shows the average distance ridden by the hour of the day in 2016. Interestingly, more distance was covered during the very early hours of the morning (2 AM to 3 AM) period. The typical distance ridden ranged from 1.4 miles to 1.6 miles from 4 AM to 12 midnight.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%206.PNG)

<p align="center">
FIGURE 6: ESTIMATED AVERAGE MILES RIDDEN BY HOUR OF CHECKOUT IN 2016
</p>


## Ridership by Hour and Weekday 
Figure 7 shows that weekday ridership patterns are similar. On the other hand weekend ridership demonstrate a busy afternoon (between 12 PM and 3 PM)

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%207.PNG)

<p align="center">
FIGURE 7: CHECKOUTS BY HOUR OF DAY PER WEEKDAY IN 2016
</p>

## Ridership by Month 
Monthly checkouts, as shown in Figure 8, suggest high ridership during the summer months and low ridership during the winter months.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%208.PNG)

<p align="center">
FIGURE 8: TOTAL CHECKOUTS BY MONTH IN 2016
</p>

## Merging with Weather 

It is highly likely that weather plays a very important role in bike ridership and bike checkout times. This was shown in the previous plots on total checkouts per hour of the day, by weekday, and by month. To verify this, weather data obtained from [Dark Sky API](https://darksky.net/dev/) was merged with the Trips dataset and several graphs plotted to visualize the relationships.

### Checkouts vs. Daily Temperature 

Figure 9 shows the total number of checkouts against maximum and minimum daily temperature. It clearly suggests that ridership increased as the temperature increased and vice-versa.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%209.PNG)

<p align="center">
FIGURE 9: TOTAL CHECKOUTS BY DAILY TEMPERATURE IN 2016
</p>

Apparent temperature, as defined by Dark Sky, is “apparent (or “feels like”) temperature in degrees Fahrenheit”. It appeared to have a subtle effect on bike ridership as shown in Figure 10.


![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2010.PNG)

<p align="center">
FIGURE 10: TOTAL CHECKOUTS BY DAILY APPARENT TEMPERATURE IN 2016
</p>


## Checkouts vs. Daily Cloud Cover 
Dark Sky defines Cloud Cover as “the percentage of sky occluded by clouds, between 0 and 1, inclusive”. Figures 11 shows the total number of checkouts against daily cloud cover. They clearly suggest that ridership was highest as the cloud cover stayed at around 0.15.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2011.PNG)

<p align="center">
FIGURE 11: TOTAL CHECKOUTS BY DAILY CLOUD COVER IN 2016
</p>

## Checkouts vs. Daily Wind Speed 
Wind speed is reported in miles per hour. As shown in Figure 12, ridership did not seem to be somewhat impacted by higher wind speeds. 

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2012.PNG)

<p align="center">
FIGURE 12: TOTAL CHECKOUTS BY DAILY WIND SPEED IN 2016
</p>

## Checkouts vs. Daily Humidity 
Humidity is defined by Dark Sky as “relative humidity, between 0 and 1. Figure 13 shows decreased ridership at higher humidity levels.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2013.PNG)

<p align="center">
FIGURE 13: TOTAL CHECKOUTS BY DAILY HUMIDITY IN 2016	
</p>

## Checkouts vs. Daily Visibility 
Visibility is measured in miles and capped at 10 miles, according to Dark Sky. As Figure 14 shows, ridership peaked when visibility was at 10 miles.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2014.PNG)

<p align="center">
FIGURE 14: TOTAL CHECKOUTS BY DAILY VISIBILITY IN 2016
</p

## Days with Highest/Lowest Ridership
Another interesting data discovery was the fact that Saturdays and Sundays had the highest and lowest ridership depending upon the weather. In his study, Tyler suggests that this may be due to “‘weekend warriors’ who rent B-cycles for pleasure and are highly affected by the weather in their decision to ride”. This may well be the case.

### Highest Ridership

Checkout Week Day | Date of Checkout | Max Temperature | Min Temperature | Number of Checkouts
----------------- | ------------------- | --------------- | --------------- | -------------------
Sunday | 2016-09-05 | 86.950 | 49.210 | 638
Tuesday | 2016-07-27 | 87.150 | 55.300 | 534
Saturday | 2016-08-06 | 76.320 | 59.090 | 529
Thursday | 2016-08-05 | 69.330 | 57.110 | 524
Thursday | 2016-07-29 | 82.480 | 58.620 | 523
Saturday | 2016-08-07 | 84.200 | 57.750 | 512
Wednesday | 2016-07-21 | 89.250 | 61.160 | 510
Sunday | 2016-08-01 | 92.090 | 59.880 | 509
Wednesday | 2016-08-04 | 70.920 | 58.620 | 509
Monday | 2016-08-02 | 80.100 | 62.820 | 509


### Lowest Ridership

Checkout Week Day | Date of Checkout | Max Temperature | Min Temperature | Number of Checkouts
----------------- | ------------------- | --------------- | --------------- | -------------------
Friday | 2016-01-09 | 25.800 | 13.110 | 33
Tuesday | 2016-12-07 | 16.050 | 0.210 | 32
Thursday | 2016-03-18 | 26.860 | 19.730 | 30
Saturday | 2016-12-18 | 18.320 | -6.840 | 26
Saturday | 2016-04-17 | 35.670 | 30.690 | 24
Tuesday | 2016-03-23 | 38.610 | 21.560 | 24
Friday | 2016-12-17 | 6.910 | -6.440 | 21
Sunday | 2016-02-01 | 27.130 | 21.230 | 20
Monday | 2016-02-02 | 22.670 | 11.790 | 20
Saturday | 2016-12-25 | 37.090 | 21.040 | 11


## Checkouts vs. Hourly Weather Variables
Hourly weather conditions provide better resolution than daily weather conditions. To investigate this, number of checkouts against hourly weather variables were also plotted and compared with the plots using daily weather variables.

### Checkouts vs. Hourly Temperature
The scatter plots in Figure 15 and 16 show that the relationship between the number of checkouts and the hourly temperatures were not linear.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2015.PNG)

<p align="center">
FIGURE 15: TOTAL CHECKOUTS BY HOURLY TEMPERATURE IN 2016
</p>

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2016.PNG)

<p align="center">
FIGURE 16: TOTAL CHECKOUTS BY HOURLY APPARENT TEMPERATURE IN 2016
</p>

### Checkouts vs. Hourly Humidity
Figure 17 shows that humidity affected ridership significantly.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2017.PNG)

<p align="center">
FIGURE 17: TOTAL CHECKOUTS BY HOURLY HUMIDITY IN 2016	
</p>

### Checkouts vs. Hourly Cloud Cover
As shown in Figure 18 Cloud Cover certainly impacted ridership.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2018.PNG)

<p align="center">
FIGURE 18: TOTAL CHECKOUTS BY HOURLY CLOUD COVER IN 2016	
</p>

### Checkouts vs. Hourly Wind Speed
Data on wind speed indicated it was clustered heavily in 0 to 8 miles per hour range, as shown in Figure 19.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2019.PNG)

<p align="center">
FIGURE 19: TOTAL CHECKOUTS BY HOURLY WIND SPEED IN 2016	
</p>

### Checkouts vs. Hourly Visibility
As shown in Figure 20 visibility at 10 miles had the greatest impact on ridership.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2020.PNG)

<p align="center">
FIGURE 20: TOTAL CHECKOUTS BY HOURLY VISIBILITY IN 2016	
</p>

# Part 2: Regression Modeling 

In his study, Tyler attempted to create a linear regression model using a number of calendar and weather variables. Using temperature, temperature squared, humidity, month, weekday, hour of day, holiday and cloud cover as input variables he arrived at an R squared value of 0.7382 which meant that approximately 73.8% of the variation in the hourly ridership could be explained by the selected variables and the linear model he used to fit the data.

In this section various linear and non-linear regression models were used to test and train the Trips data that was merged with the weather data to try to predict the number of checkouts based on calendar, clock and weather conditions.

The following regression models with their brief explanation were used in this study:
	
* Linear Regression
  * Most widely used statistical and machine learning technique to model relationship between two sets of variables typically using a straight line. Simple to use and fast performance but lacks high accuracy when compared to non-linear models.
	
* Lasso Regression
  * A type of linear regression that uses shrinkage to reduce data values toward the mean. Well suited for automating feature selection.

* Ridge Regression
  * Well suited for data that suffers from multicollinearity, i.e. features with high correlation.

* Bayesian Ridge Regression
  * An approach to linear regression in which the statistical analysis is undertaken using Bayesian inference.

* Decision Tree Regression
  * Uses a tree like structure to derive a final decision on the outcome of the analysis.

* Random Forest Regression
  * An ensemble learning method that operates by constructing a multitude of decision trees to arrive at the mean prediction.

* Extra Trees Regression
  * An extremely randomized tree regressor. Builds a totally random decision tree.

* Nearest Neighbors Regression
  * A simple algorithm that uses a similarity measure (e.g. distance between neighbors) to predict the outcome.

## Regression Modeling with Categorical Feature Set
The Checkout Month, Week Day and Hour numeric variables were converted to categorical features resulting in 45 total features for regression modeling.

Prior to applying the models a feature correlation was performed on all the features to see if any of the features were highly correlated to one another. As shown in Figure 21, Temperature and Apparent Temperature were highly correlated suggesting that one of them could be removed from the features in the model application.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2021.PNG)

<p align="center">
FIGURE 21: FEATURE CORRELATIONS
</p>

The models used for regression supported the use of several parameters that could be used to adjust or tune them for better performance. In most cases in this study, the parameters were set to default.

The dataset was randomly spilt into 70% for training and 30% for testing. For each model the training and test scores, R Squared and RMSE results were collected and summarized. In addition, the Decision Tree, Random Forest and Extra Trees models also had their Feature Importance bar charts plotted. The chart for Extra Tree model is shown in Figure 22.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2022.PNG)

<p align="center">
FIGURE 22: EXTRA TREES REGRESSION MODEL FEATURE IMPORTANCE CHART
</p>

## Regression Modeling Summary – Categorical Feature Set

Metric | Linear | Lasso | Ridge | Bayesian Ridge | Decision Tree | Random Forest | Extra Trees | Nearest Neighbors
------ | ------ | ----- | ----- | -------------- | ------------- | ------------- | ----------- | -----------------
Training Test Score | 0.680 | 0.677 | 0.677 | 0.680 | 1.000 | 0.943 | 1.000 | 0.597
Test Set Score | 0.676 | 0.674 | 0.674 | 0.676 | 0.423 | 0.679 | 0.699 | 0.496
R Squared | 0.822253 | 0.821127 | 0.821127 | 0.822232 | 0.650078 | 0.824289 | 0.835802 | 0.70400
RMSE | 46.268837 | 46.533272 | 46.533272 | 46.273848 | 82.481079 | 45.789939 | 43.059707 | 72.051003


The Extra Trees regression model achieved the highest accuracy and the lowest RMSE. The Decision Tree model had lowest accuracy and the highest RMSE.

## Regression Modeling with Numerical Feature Set

Using Checkout Month, Week Day and Hour numeric variables resulted in just 9 total features for regression modeling.

Prior to applying the models a feature correlation was performed on all the features to see if any of the features were highly correlated to one another. As shown in Figure 23, Temperature and Apparent Temperature were highly correlated suggesting that one of them could be removed from the features in the model application.


![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2023.PNG)

<p align="center">
FIGURE 23: FEATURE CORRELATION
</p>

For each model the training and test scores, R Squared and RMSE results were collected and summarized. In addition, the Decision Tree, Random Forest and Extra Trees models also had their Feature Importance bar charts plotted. The chart for Random Forest and the Extra Trees models are shown in Figures 24 and 25, respectively.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2024.PNG)

<p align="center">
FIGURE 24: RANDOM FOREST REGRESSION MODEL FEATURE IMPORTANCE CHART
</p>

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2025.PNG)

<p align="center">
FIGURE 25: EXTRA TREES REGRESSION MODEL FEATURE IMPORTANCE CHART
</p>

## Regression Modeling Summary – Numerical Feature Set

Metric | Linear | Lasso | Ridge | Bayesian Ridge | Decision Tree | Random Forest | Extra Trees | Nearest Neighbors
------ | ------ | ----- | ----- | -------------- | ------------- | ------------- | ----------- | -----------------
Training Test Score | 0.452 | 0.444 | 0.444 | 0.451 | 1.000 | 0.947 | 1.000 | 0.867
Test Set Score | 0.470 | 0.463 | 0.463 | 0.471 | 0.481 | 0.735 | 0.739 | 0.616
R Squared | 0.655919 | 0.680605 | 0.680605 | 0.685989 | 0.693454 | 0.857242 | 0.859465 | 0.784742
RMSE | 74.533468 | 75.555613 | 75.555613 | 74.519813 | 73.070383 | 37.319948 | 36.782801 | 54.076287


### Regression Modeling Summary
* The data exploration phase of this study revealed the significance of weather variables on the ridership. The regression modeling phase confirmed this to be accurate. Looking at the feature importance graphs generated by the Extra Trees and Random Forest models, the weather attributes rank the highest.
* The non-linear regression models performed better than the linear models. In particular, even with a reduced feature set, the non-linear models such as the Extra Trees and the Random Forest were the best performers with R Squared values well above 0.85.

## Testing Regressor on unseen samples
The Extra Trees Forest Regressor with a predictive accuracy of 85.9% was used to predict 10 samples (with numerical feature set) from the dataset that had not been used neither in the training nor in the test sets. The results are tabulated below. The regressor predicted all 10 of the 10 samples accurately. 

Sample Number | Actual Number of Checkouts | Predicted Number of Checkouts | +/-
------------- | -------------------------- | ----------------------------- | ---
1 | 12 | 12 | 0
2 | 48 | 48 | 0
3 | 9 | 9 | 0
4 | 33 | 33 | 0
5 | 12 | 12 | 0
6 | 13 | 13 | 0
7 | 9 | 9 | 0
8 | 6 | 6 | 0
9 | 8 | 8 | 0
10 | 5 | 5 | 0


# Part 3: Classification Modeling 
In this section various classification models were used to test and train the Trips data that was merged with the weather data to try to predict the checkout hour based on weather conditions.

The following classification models were used in this study:

* Linear (Logistic) Classification
  * Similar to linear regression but used for classification

* Decision Tree Classification
  * Uses a tree like structure to derive at a final decision on the outcome of the analysis

* Random Forest Classification
  * Similar to random forest regression but used for classification

* Extra Trees Classification
  * Similar to extra trees regression but used for classification

* Naïve Bayes Classification
  * Uses the Bayes’ Theorem (i.e. assumes that the presence of a particular feature is unrelated to the presence of any other feature)

* Gradient Boosting Classification
  * A machine learning method that produces a prediction model in the form of an ensemble of weak prediction models, typically decision trees.

* Nearest Neighbors Classification
  * Similar to nearest neighbors regressor but used for classification

* Multi-layer Perceptron Classification
  * A feedforward artificial neural network mode that maps sets of input data onto a set of appropriate outputs.

The dataset was randomly spilt into 70% for training and 30% for testing. The class labels were defined as follows:

* Class 0: Number of Checkouts >= 1 and <= 10
* Class 1: Number of Checkouts > 10

A cross validation using the Stratified Shuffle Split method was performed on the dataset for each model using a training sample size of 50% and a testing sample size of 50% with 10 splits.

## Classification Modeling – Categorical Feature Set

As in the case of Regression modeling, feature correlation was carried out to determine if any features had a high correlation with one another. As shown in Figure 21, Temperature and Apparent Temperature were highly correlated suggesting that one of them could be removed from the features in the model application.

For each model the training and test scores, Accuracy, F1 (micro), F1 (macro), Precision (macro), Precision (micro), Recall (macro) and Recall (micro) results were collected and summarized. In addition, the Decision Tree, Random Forest and Extra Trees models also had their Feature Importance bar charts plotted.



### Classification Modeling Summary – Categorical Feature Set
Metric | Logistic | Decision Tree | Random Forest | Extra Trees | Naïve Bayes | Nearest Neighbors | Gradient Boosting | Multi-Layer Perceptron
------ | -------- | ------------- | ------------- | ----------- | ----------- | ----------------- | ----------------- | ---------------------
Accuracy | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
F1 (macro) | 0.877009 | 0.811243 | 0.856088 | 0.876795 | 0.747293 | 0.703119 | 0.817388 | 0.875557
F1 (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
Precision (macro) | 0.877030 | 0.811341 | 0.857210 | 0.877409 | 0.799952 | 0.751804 | 0.817524 | 0.875965
Precision (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
Recall (macro) | 0.8777014 | 0.811251 | 0.856172 | 0.876995 | 0.756566 | 0.714103 | 0.817399 | 0.875576
Recall (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
F1 (macro) | 0.877009 | 0.811243 | 0.856088 | 0.876795 | 0.747293 | 0.703119 | 0.817388 | 0.875557
F1 (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
Precision (macro) | 0.877030 | 0.811341 | 0.857210 | 0.877409 | 0.799952 | 0.751804 | 0.817524 | 0.875965
Precision (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
Recall (macro) | 0.8777014 | 0.811251 | 0.856172 | 0.876995 | 0.756566 | 0.714103 | 0.817399 | 0.875576
Recall (micro) | 0.877010 | 0.811258 | 0.856197 | 0.877010 | 0.756386 | 0.714286 | 0.817408 | 0.875591
Cross Validation | 0.858643 | 0.804258 | 0.856145 | 0.864045 | 0.740562 | 0.721885 | 0.799319 | 0.870338
Execution Time (sec) | 10.791598 | 0.317235 | 4.023082 | 3.425960 | 0.175422 | 0.994537 | 48.096231 | 9.780759

The Extra Trees model attained the highest accuracy in classifying the two classes. The Naïve Bayes model attained the lowest.

## Classification Modeling – Numerical Feature Set
Using Checkout Month, Week Day and Hour numeric variables resulted in just 9 total features for regression modeling.

As in the case of Regression modeling, feature correlation was carried out to determine if any features had a high correlation with one another. As shown in Figure 26, Temperature and Apparent Temperature were highly correlated suggesting that one of them could be removed from the features in the model application.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2026.PNG)

<p align="center">
FIGURE 26: FEATURE CORRELATION
</p>

For each model the training and test scores, Accuracy, F1 (micro), F1 (macro), Precision (macro), Precision (micro), Recall (macro) and Recall (micro) results were collected and summarized. In addition, the Decision Tree, Random Forest, Extra Trees and Gradient Boosting models also had their Feature Importance bar charts plotted. The chart for the Random Forest model is shown in Figure 27.

![](https://github.com/hbhasin/Boulder-2016-Bike-Share/blob/master/figures/Figure%2027.PNG)

<p align="center">
FIGURE 27: RANDOM FOREST CLASSIFICATION MODEL FEATURE IMPORTANCE CHART
</p>

## Classification Modeling Summary – Numerical Feature Set
Metric | Logistic | Decision Tree | Random Forest | Extra Trees | Naïve Bayes | Nearest Neighbors | Gradient Boosting | Multi-Layer Perceptron
------ | -------- | ------------- | ------------- | ----------- | ----------- | ----------------- | ----------------- | ---------------------
Accuracy | 0.772942 | 0.845790 | 0.878430 | 0.872280 | 0.771523 | 0.815043 | 0.851939 | 0.867550
F1 (macro) | 0.772932 | 0.845788 | 0.878403 | 0.872190 | 0.769910 | 0.812961 | 0.851927 | 0.867515
F1 (micro) | 0.772942 | 0.845790 | 0.878430 | 0.872280 | 0.771523 | 0.815043 | 0.851939 | 0.867550
Precision (macro) | 0.773004 | 0.845802 | 0.878721 | 0.873266 | 0.779530 | 0.829477 | 0.852033 | 0.867893
Precision (micro) | 0.772942 | 0.845790 | 0.878430 | 0.872280 | 0.771523 | 0.815043 | 0.851939 | 0.867550
Recall (macro) | 0.772949 | 0.845790 | 0.878416 | 0.872256 | 0.771603 | 0.819944 | 0.851932 | 0.867535
Recall (micro) | 0.772942 | 0.845790 | 0.878430 | 0.872280 | 0.771523 | 0.815043 | 0.851939 | 0.867550
Cross Validation | 0.771672 | 0.832108 | 0.874368 | 0.871019 | 0.765200 | 0.822538 | 0.843486 | 0.852682
Execution Time (sec) | 9.676564 | 0.301543 | 3.972808 | 3.246149 | 0.106590 | 0.953759 | 20.225848 | 4.669855


Both the Random Forest and the Extra Trees classifiers achieved the highest accuracy and the Naïve Bayes the lowest. The cross validation test accuracy were comparable to the F1 (micro), Precision (micro) and the Recall (micro) accuracies.

## Classification Modeling Summary
* The Extra Trees model attained the highest accuracy in classifying the two classes using the categorical feature set. The Naïve Bayes model attained the lowest.

* The Random Forest Classifier achieved the highest accuracy and the Naïve Bayes the lowest with the numerical feature set.

* The non-linear classification models (except Naive Bayes) performed better than the linear model.

## Testing Classifier on unseen samples
The Random Forest Classifier with a predictive accuracy of 87.8% was used to predict 10 samples (with numerical feature set) from the dataset that had not been used neither in the training nor in the test sets. The results are tabulated below. The classifier predicted 9 of the 10 samples accurately. Of the remaining 1 sample, it predicted one class above the actual class.


Sample Number | Actual Number of Checkouts | Class Number | Predicted Number of Checkouts | Class Number
------------- | -------------------------- | ------------ | ----------------------------- | ------------
1 | Greater than 10 | 1 | Greater than 10 | 1
2 | Greater than 10 | 1 | Greater than 10 | 1
3 | Between 1 and 10 | 0 | Between 1 and 10 | 0
4 | Greater than 10 | 1 | Greater than 10 | 1
5 | Greater than 10 | 1	| Greater than 10 | 1
6 | Greater than 10 | 1	| Greater than 10 | 1
7 | Between 1 and 10 | 0 | Greater than 10 | 1
8 | Between 1 and 10 | 0 | Between 1 and 10 | 0
9 | Between 1 and 10 | 0 | Between 1 and 10 | 0
10 | Between 1 and 10 | 0 | Between 1 and 10 | 0

# Summary

This in-depth study on Boulder 2016 Bike Share Trips data was undertaken to continue the work that Tyler started on the 2014 Denver Bike Ridership data. It agrees with his findings that merging calendar, clock and weather attributes into the Trips dataset can reveal ridership patterns and allow regression and classification techniques to be applied for prediction purposes.

This study covered three areas:

1. Explored the Trips datasets and visualized the data and provided useful and interesting information.
2. Deployed a variety of supervised machine learning regression models to predict the number of checkouts using calendar, clock and weather attributes.
3. Deployed a variety of supervised machine learning classification models to predict two classes reflecting the number of checkouts using calendar, clock and weather attributes.

## Next Steps

* Provide and/or present findings to Boulder B-cycle executives to improve future ridership
* Develop a simple desktop, web or mobile app that takes calendar, clock and weather variables as inputs and predicts the number of checkouts as the output.
* Longmont, CO has just introduced its bike sharing system – this study could be useful to the management.
