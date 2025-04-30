# ERD
```mermaid
erDiagram
    WSJ only one to zero or more wsj_gainers_YYYY-MM-DD-HH:MM.csv: "download 3x daily on weekdays"
    YAHOO only one to zero or more yahoo_gainers_YYYY-MM-DD-HH:MM.csv: "download 3x daily on weekdays"
    "STOCK ANALYSIS" only one to zero or more stockanalysis_gainers_YYYY-MM-DD-HH:MM.csv: "download 3x daily on weekdays"
    
    wsj_gainers_YYYY-MM-DD-HH:MM.csv {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    yahoo_gainers_YYYY-MM-DD-HH:MM.csv {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    stockanalysis_gainers_YYYY-MM-DD-HH:MM.csv {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }

wsj_gainers_YYYY-MM-DD-HH:MM.csv only one to only one parsed_wsj_gainers: "parse source and timestamp from filename (pandas dataframe)"
yahoo_gainers_YYYY-MM-DD-HH:MM.csv only one to only one parsed_yahoo_gainers: "parse source and timestamp from filename (pandas dataframe)"
stockanalysis_gainers_YYYY-MM-DD-HH:MM.csv only one to only one parsed_stockanalysis_gainers: "parse source and timestamp from filename (pandas dataframe)"

    parsed_wsj_gainers {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change "change in price as a percentage"
        string source "Download source"
        string date_time "Timestamp in YYYYMMDD_HHMM format"
    }
    parsed_yahoo_gainers {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change "change in price as a percentage"
        string source "Download source"
        string date_time "Timestamp in YYYYMMDD_HHMM format"
    }
    parsed_stockanalysis_gainers {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change "change in price as a percentage"
        string source "Download source"
        string date_time "Timestamp in YYYYMMDD_HHMM format"
    }

parsed_wsj_gainers only one to only one downloads_seed: "parse individually"
parsed_yahoo_gainers only one to only one downloads_seed: "parse individually"
parsed_stockanalysis_gainers only one to only one downloads_seed: "parse individually"

parsed_wsj_gainers only one to only one gainers_seed: "parse individually"
parsed_yahoo_gainers only one to only one gainers_seed: "parse individually"
parsed_stockanalysis_gainers only one to only one gainers_seed: "parse individually"

parsed_wsj_gainers only one to only one gainers_details_seed: "parse individually"
parsed_yahoo_gainers only one to only one gainers_details_seed: "parse individually"
parsed_stockanalysis_gainers only one to only one gainers_details_seed: "parse individually"

parsed_wsj_gainers only one to only one sources_seed: "parse individually"
parsed_yahoo_gainers only one to only one sources_seed: "parse individually"
parsed_stockanalysis_gainers only one to only one sources_seed: "parse individually"

    downloads_seed {
        str date_time PK "Download timestamp in Date, Hour format"
        int year "Year of download"
        int month "Month of download (1-12)"
        int day "Day of download"
        int time "Time of download (HHMM, 24-hour time)"
    }
    gainers_seed {
        string symbol PK "Unique stock symbol"
    }
    gainer_details_seed {
        int date_time FK "From the DOWNLOADS table"
        string source FK "From the SOURCE table"
        string symbol FK "From the GAINERS table"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    sources_seed {
        string source PK "'wsj', 'yahoo', or 'stockanalysis'"
    }
 
downloads_seed one or more to only one downloads: "incremental"
gainers_seed one or more to only one gainers: "incremental"
gainer_details_seed one or more to only one gainer_details: "incremental"
sources_seed one or more to only one sources: "incremental"

    downloads {
        str date_time PK "Download timestamp in Date, Hour format"
        int year "Year of download"
        int month "Month of download (1-12)"
        int day "Day of download"
        int time "Time of download (HHMM, 24-hour time)"
    }
    gainers {
        string symbol PK "Unique stock symbol"
    }
    gainer_details {
        int date_time FK "From the DOWNLOADS table"
        string source FK "From the SOURCE table"
        string symbol FK "From the GAINERS table"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    sources {
        string source PK "'wsj', 'yahoo', or 'stockanalysis'"
    }

gainer_details only one to only one source_overlap: "view"
gainer_details only one to only one source_reliability: "view"
gainer_details only one to only one ticker_price_range: "view"
gainer_details only one to only one ticker_repeats: "view"

    source_overlap {
        string source FK "FK from the SOURCE table via the GAINER-DETAILS table"
        float avg_proportion_overlapping "Average proprtion of the source's gainers that are found in the other sources at the time of each download"
    }
    source_reliability {
        string source FK "Data download source"
        int download_count "Total successful downloads for the source"
        float reliability_score "Proportion of the total attempted downloads successfully executed for the source"
    }
    ticker_price_range {
        string symbol FK "Stock ticker"
        float min_price "Lowest observed price for the ticker"
        float max_price "Highest observed price for the ticker"
        float price_range "Difference between the ticker's highest and lowest observed prices"
    }
    ticker_repeats {
        str symbol FK "FK from the GAINERS table via the GAINER-DETAILS table"
        int counts "Number of times the stock has appeared across different timepoints"
    }
```
