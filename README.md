# Stock Analysis

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General Info
This program is intended to help with the stocks valuation. It presents two main functions that will be shown in the beggining of the program execution. Firstly, you can compare stocks by their actual metrics, such as price earnings ratio, price earnings growth, enterprise value, and others . It is necessary to pass the stocks code for the execution. The program will gather the stocks data using the yfinance library, and web scrapping the yahoo finance site utilizing the requests library and show a table with the summary for the companies.

Another functionality implemented is to calculate the company intrinsic value through the discounted cash flow method. This method projects the future cash flows based on the past revenues growth of the company. Then it brings to present moment to estimate the intrinsic value of the stock. This method is inspired by the lecture on https://www.youtube.com/watch?v=fd_emLLzJnk .

 ## Technologies
 The technologies used to build this program were:
 * Python 3.8
 * Numpy
 * Yfinance
 * Pandas
 * Requests
 
 ## Setup
 To run this project you need to execute the python script named "stock_analysis.py". For this you need to have installed Python 3.8 or more recent versions. To check your python version open a linux terminal or the cmd for Windows and type:
 ```
 python3 -V
 ```
 To install pip:
 ```
 sudo apt install pip3
```
 And the libraries numpy, yfinance:
 ```
 pip3 install yfinance
 pip3 install numpy
 ```
 To run the program, go to the folder where is the script "stock_analysis" and execute:
 ```
 python3 stock_analysis.py
 ```
