stock_fundementals_scrapey
<h2>Scrapes for some fundemental stock financials </h2>

<h4>Contains a number of functions that return the following for one or a list of stock ticker symbols:</h4>
<li> Net Income for two latest available annual Income Statements</li>
<li> Gross Revenue for two latest available annual Income Statements</li>
<li> Current Ratio (Current Assets / Current Liabilities) for two latest available annual Balance Sheets</li>
<li> Trailing P/E ratios for up to past 12 months of quarterly report and the quarterly report 1-year prior </li>

<br>Functions:

pull_ni_list(symbol_list) 
<br>#given a list of stock ticker symbols as strings, returns most recent annual Net Income and the previous year's annual net income

pull_curr_ratio_list(symbol_list):
<br>#returns two most recent annual current ratio (Current Assets / Current Liabilities) as a dictionary with following structure: 
#{symbol: [(most_recent_date, most_recent_curr_ratio), (prev_date, prev_curr_ratio)]}

pull_rev_list(symbol_list):
<br>#returns dictionary with following structure:
#{symbol: [most_recent_annual_rev, prev_yr_annual_rev]}

pull_pe_list(symbol_list):
<br>#returns dictionary of up to a year's worth of trailing P/E ratios from quarterly reports.
#Dictionary has following structure: 
#{symbol: [(most_recent_date, most_recent_pe), 
           (prev_date, prev_pe), 
           (six_mos_date, six_mos_pe), 
           (nine_mos_date, nine_mos_pe),
            (yr_ago_date, yr_ago_pe)]]
  }
