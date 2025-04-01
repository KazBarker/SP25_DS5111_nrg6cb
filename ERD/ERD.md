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
 
    TIMESTAMP-WSJ-GAINERS many to only one DOWNLOADS : "compile"
    TIMESTAMP-Y-GAINERS many to only one DOWNLOADS : "compile"
    TIMESTAMP-STOCKANALYSIS-GAINERS many to only one DOWNLOADS : "compile"

    DOWNLOADS {
        int download_id PK
        date date "Date of download"
        int hour "Hour of download"
    }

    SOURCES {
        string source PK "'wsj', 'yahoo', or 'stockanalysis'"
    }

    DOWNLOADS many to one or more SOURCE-DOWNLOAD : "link"
    SOURCES many to one or more SOURCE-DOWNLOAD : "link"

    SOURCE-DOWNLOAD {
        int gainer_id PK
        int download_id FK "From the DOWNLOADS table"
        string source FK "From the SOURCE table"
    }
```


```
    TIMESTAMP-WSJ-GAINERS many to only one GAINER-DOWNLOADS : "compile"
    TIMESTAMP-Y-GAINERS many to only one GAINER-DOWNLOADS : "compile"
    TIMESTAMP-STOCKANALYSIS-GAINERS many to only one GAINER-DOWNLOADS : "compile"

    GAINER-DOWNLOADS {
        int download_id PK
        date date "Date of download"
        int hour "Hour of download"
        string symbol "The stock symbol"
        int instances "Number of gainer sources the symbol is found in for this timepoint"
    }
```

```

    TIMESTAMP-WSJ-GAINERS many to only one WSJ-GAINERS : "compile"
    TIMESTAMP-Y-GAINERS many to only one Y-GAINERS : "compile"
    TIMESTAMP-STOCKANALYSIS-GAINERS many to only one STOCKANALYSIS-GAINERS : "compile"

    WSJ-GAINERS {
        date date PK
        int hour PK
        string symbol PK
        float price
        float price_change
        float percent_price_change
    }
    Y-GAINERS {
        date date PK
        int hour PK
        string symbol PK
        float price
        float price_change
        float percent_price_change
    }
    STOCKANALYSIS-GAINERS {
        date date PK
        int hour PK
        string symbol PK
        float price
        float price_change
        float percent_price_change
    }
```
