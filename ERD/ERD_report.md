# Gainers Compilation Report
## Introduction
This report describes the "gainers" stock data, including data collection, data processing, and use cases. These data are collected with the intent to identify useful trends and patterns in the top daily gainers identified by several financial websites. These trends and patterns could be used in the future to help inform shareholders' stock trading and investing actions.

## Use Cases
* Identify regularly recurring stocks

* Assess data source consistency: are the same stocks identified as gainers simultaneously across data sources?

## Methods
Gainers data were downloaded at regular intervals during trading hours from 3 sources: [Stock Analysis](https://stockanalysis.com/markets/gainers/), [The Wall Street Journal](https://www.wsj.com/market-data/stocks/us/movers), and [Yahoo Finance](https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200). Downloads were normalized to contain only the columns `symbol`, `price`, `price_percent_change`, and `price_change` and saved as CSV files with filenames containing the date and time of download.  

A "sources" table was compiled, listing all gainers data sources - currently WSJ, Yahoo, and Stock Analysis. Downloaded gainers CSV files were compiled and parsed into 3 tables: "downloads", "gainers", and "gainer detials": 

* **Downloads**: Contains the date and the hour of all downloads carried out for one or more gainer sources.

* **Gainers**: Contains all stock symbols that appear anywhere within the gainers data, as well as a count of the number of times each symbol has appeared.

* **Gainer Details**: Contains the primary keys from Sources, Downloads, and Gainers as well as the specific data associated with a particular gainer instance (price, price change, and price percent change)

## Summary

