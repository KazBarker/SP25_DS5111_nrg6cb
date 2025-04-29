# ERD
```mermaid
erDiagram
    WSJ only one to zero or more TIMESTAMP-WSJ-GAINERS : "download 3x daily"
    YAHOO only one to zero or more TIMESTAMP-Y-GAINERS : "download 3x daily"
    "STOCK ANALYSIS" only one to zero or more TIMESTAMP-STOCKANALYSIS-GAINERS : "download 3x daily"
    
    TIMESTAMP-WSJ-GAINERS {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    TIMESTAMP-Y-GAINERS {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }
    TIMESTAMP-STOCKANALYSIS-GAINERS {
        string symbol PK "The stock symbol"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }

    SOURCES {
        string source PK "'wsj', 'yahoo', or 'stockanalysis'"
    }
 
    TIMESTAMP-WSJ-GAINERS many optionally to only one DOWNLOADS : "extract"
    TIMESTAMP-Y-GAINERS many optionally to only one DOWNLOADS : "extract"
    TIMESTAMP-STOCKANALYSIS-GAINERS many optionally to only one DOWNLOADS : "extract"

    DOWNLOADS {
        str date_time PK "Download timestamp in Date, Hour format"
        int year "Year of download"
        int month "Month of download (1-12)"
        int day "Day of download"
        int time "Time of download (HHMM, 24-hour time)"
    }

    TIMESTAMP-WSJ-GAINERS many optionally to only one GAINERS : "unique"
    TIMESTAMP-Y-GAINERS many optionally to only one GAINERS : "unique"
    TIMESTAMP-STOCKANALYSIS-GAINERS many optionally to only one GAINERS : "unique"

    GAINERS {
        string symbol PK "Unique stock symbol"
    }
    
    DOWNLOADS one to one or more GAINER-DETAILS : "link"
    SOURCES one to one or more GAINER-DETAILS : "link"
    GAINERS one to one or more GAINER-DETAILS : "link"
    TIMESTAMP-WSJ-GAINERS one to one GAINER-DETAILS : "parse"
    TIMESTAMP-Y-GAINERS one to one GAINER-DETAILS : "parse"
    TIMESTAMP-STOCKANALYSIS-GAINERS one to one GAINER-DETAILS : "parse"

    GAINER-DETAILS {
        int date_time FK "From the DOWNLOADS table"
        string source FK "From the SOURCE table"
        string symbol FK "From the GAINERS table"
        float price "Current price"
        float price_change "Current price vs price at opening"
        float price_percent_change
    }

    GAINER-DETAILS one or more to one SOURCE-OVERLAP : "aggregate & view"

    SOURCE-OVERLAP {
        string source FK "FK from the SOURCE table via the GAINER-DETAILS table"
        float avg_proportion_overlapping "Average proprtion of the source's gainers that are found in the other sources at the time of each download"
    }

    GAINER-DETAILS one or more to one TICKER-REPEATS : "aggregate & view"

    TICKER-REPEATS {
        str symbol FK "FK from the GAINERS table via the GAINER-DETAILS table"
        int counts "Number of times the stock has appeared across different timepoints"
    }

    GAINER-DETAILS one or more to one SOURCE-RELIABILITY: "aggregate & view"

    SOURCE-RELIABILITY {
        str source FK "Data download source"
        int download_count "Total successful downloads for the source"
        float reliability_score "Proportion of the total attempted downloads successfully executed for the source"
}
```
