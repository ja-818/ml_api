# Locust stress tests report

## Test 1
### Parameters
- Number of users: 100
- Spawn rate: 10
- Model service instances: 1
### Results
- With 100 users, and 6.4 RPS: 0 Failures
### Conclusion
The service doesn't have problems with this level of users and requests

<br>

## Test 2
### Parameters
- Number of users: 500
- Spawn rate: 50
- Model service instances: 1
### Results
- With 500 users and 7 RPS: 0 Failures
### Conclusion
The service doesn't have problems with this level of users and requests


<br>

## Test 3
### Parameters
- Number of users: 1000
- Spawn rate: 25
- Model service instances: 1
### Results
- With 650 users, and 6.6 RPS: 0 Failures
- The model begins to fail with 700 users and 9.3 RPS: 2.7 Failures
- At the top RPS (36.4) and 1000 users: 36.4 Failures
### Conclusion
The service begins to fail with 700 users and the failures gets worst as the RPS and users increase

<br>

## Test 4
### Parameters
- Number of users: 1000
- Spawn rate: 25
- Model service instances: 5
### Results
- With 675 users, and 11.6 RPS: 0 Failures
- The model begins to fail with 725 users and 13.9 RPS: 2.8 Failures
- At the top RPS (46.8) and 1000 users: 37.3 Failures
### Conclusion
The service begins to fail with 725 users and the failures gets worst as the RPS and users increase. 
Nonetheless, the service works better with 5 instances of the service model than it does with just 1, as it supports more RPS with a lesser percentage of failures.

<br>

## Final conclusions
1. With 1 model service, the api runs without failures with a max of 650 users and 6.6 RPS
2. With 5 model services, the api runs without failures with a max of 675 users and 11.6 RPS
3. Increasing the number of model services not only increases the max number of users and RPS before failure, but also decreases the number of 