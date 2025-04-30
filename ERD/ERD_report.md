# Gainers Compilation Report
## Introduction
This report describes the "gainers" stock data, including data collection, data processing, and use cases. These data are collected with the intent to identify useful trends and patterns in the top daily gainers identified by several financial websites. These trends and patterns could be used in the future to help inform shareholders' of the reliability of information sources (WSJ, Yahoo, and Stock Analysis) and provide data for stock trading and investing actions.

## Use Cases
* Assess data source consistency:
    - Do downloads succeed regularly across all data sources? Are there any failure patterns present?
    - Are the same stocks identified as gainers simultaneously across data sources?

* Gather stock information:
    - What stocks repeat regularly?
    - Show gainer observed price ranges

## Methods
Gainers data were downloaded at regular intervals during trading hours from 3 sources: [Stock Analysis](https://stockanalysis.com/markets/gainers/), [The Wall Street Journal](https://www.wsj.com/market-data/stocks/us/movers), and [Yahoo Finance](https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200). Downloads were normalized to contain only the columns `symbol`, `price`, `price_percent_change`, and `price_change` and saved as CSV files with filenames containing the date and time of download.  

To export data to Snowflake, each normalized file was parsed using a python script: timestamp and download source information were extracted from the filename, then the data were converted into "seed" tables, with formats exactly matching those described below. These "seed" tables were then iteratively appended to the (existing) tables within Snowflake using DBT. This process was automated to continually extract and upload data each time a new download became available. After export, the original gainers data files were moved to a cache to enable rebuilding of Snowflake tables if necessary.

Once gainer downloads were parsed and uploaded to Snowflake, DBT was again used to create the Views described below.

### Table Descriptions:
* **Downloads**: Parsed from the downloaded gainers csv files Contains the timestamp, year, month, day, and time of all downloads carried out for at least one gainer source.

* **Gainers**: Contains all stock symbols that appear anywhere within the gainers data.

* **Gainer Details**: Contains the primary keys from Sources, Downloads, and Gainers as well as the specific data associated with a particular gainer instance (price, price change, and price percent change).

* **Sources**: All unique download sources. To be used in the future in case of expansion of sources, and for debugging purposes.

### View Descriptions:
* **Download Consistency (Day)**: Derived from the Gainer Details and Downloads tables, this view describes the consistency with which download sources provided data, by weekday. Includes the total downloads for each source on each weekday, as well as the proportion of successful downloads, compared to the expected number of downloads. 

* **Download Consistency (Time)**: Derived from the Gainer Details and Downloads tables, this view describes the consistency with which download sources provided data, by time of download. Includes the total downloads for each source on each download time, as well as the proportion of successful downloads, compared to the expected number of downloads. 

* **Source Overlap**: Derived from the Gainer Details table, this view displays the proportion of each source's gainers that were also found in at least of the other sources downloaded at the same time, averaged over all download times.

* **Source Reliability**: Derived from the Gainer Details table, this view displays the total downloads for each source and a "reliability score" for that source, calculated as the proportion of the expected number of downloads the source actually exhibits.

* **Ticker Price Range**: Derived from the Gainer Details table, this view displays the minimum and maximum observed prices for each stock ticker, across all dates and sources, as well as the total computed price range for each ticker.

* **Ticker Repeats**: Derived from the Gainer Details table, this view contains the total number of instances each stock ticker was observed throughout the dataset.

## Summary
The *available* data indicate Yahoo is the most consistent data source in data aquisition both at the weekday and download time scales. This is supported by the overall reliability score from the Source Reliability table, where Yahoo earned a score of 1.0, Stock Analysis a score of 0.94, and WSJ a score of 0.89. Also considering the *available* data, Yahoo appears to demonstrate the greatest average overlap with the other data sources, seemingly indicating tickers listed within the Yahoo data are, on average, more consistent/less unique than the tickers listed within either of the other data sources. 

Further investigation is necessary before any conclusions can be drawn from these data. Early bugs in the download pipeline likely have created uneven coverage for download *attempts* between days, times, and download sources themselves. To effectively evaluate data source performance it will be necessary to run a data collection study, with uninterrupted and consistent download attempts spanning several weeks. Furthermore, because each data source currently provides differing numbers of gainers on download, it is not possible to rely on the consistency evaluation: for example, Yahoo provides far fewer gainers on each download than WSJ, meaning there will automatically be less overlap of WSJ's stocks with Yahoo's than vice versa. It is recommended to further develop the download or parsing processes, to ensure all data sources provide the same number of gainers upon each download. The large size of the attempted download from WSJ may additionally be contributing to a higher download failure rate: in this case, standardizing the requested download size would be a highly productive solution and should be investigated prior to downstream limitations on gainers. 

Given the necessary improvements highlighted above, significant caution is warrented in considering the compiled stock information. The provided views of price range and repeat counts provide a proof-of-concept that analyses can be conducted in the future when the pipeline is more robust; however, due to missing data and the lack of sophistocation in the available views no confident conclusions can be reached about the gainers within the download period. It is notable that, across a total of 48 maximum attempted downloads, the maximum number of times a gainer recurred was 17. Future analyses could investigate recurrence using time series, and price range insights could be expanded by using price percentage change in addition to base price.

Overall, further pipeline development is necessary before any reliable insights can be achieved. Normalizing the number of gainers downloaded, ensuring downloads are consistently successful, and implementing methods of managing data in the case of failure of one data source will produce significant improvements in the quality of insights possible to derive from the data. Furthermore, additional data sources could improve robustness, data diversity, and provide additional insights about source reliability and consistency. Only once these steps are completed should further analyses be implemented.
