stock_fundementals_scrapey
<h2>Scrapes for fundemental stock financials and metrics</h2>

<h4>Contains a number of functions that return the following for one or a list of stock ticker symbols:</h4>
<li> Gross Revenue and Net Income for three latest available annual Income Statements</li>
<li> Current Ratio (Current Assets / Current Liabilities) for two latest available annual Balance Sheets</li>
<li> Trailing P/E ratios for up to past 12 months of quarterly report and the quarterly report 1-year prior </li>
<li> Price difference for a stock ticker given a start date and number of days after start day </li>


<br>Functions:

pull_curr_ratio_list(symbol_list):
<br>#returns two most recent annual current ratio (Current Assets / Current Liabilities) as a dictionary with following structure: 
#{symbol: [(most_recent_date, most_recent_curr_ratio), (prev_date, prev_curr_ratio)]}

pull_rev_list(symbol_list):
<br>#returns dictionary with following structure:
#{symbol: [most_recent_annual_rev, prev_yr_annual_rev, two_yrs_ago_rev]}

pull_pe_list(symbol_list):
<br>#returns dictionary of up to a year's worth of trailing P/E ratios from quarterly reports.
#Dictionary has following structure: 
#{symbol: [(most_recent_date, most_recent_pe), 
           (prev_date, prev_pe), 
           (six_mos_date, six_mos_pe), 
           (nine_mos_date, nine_mos_pe),
            (yr_ago_date, yr_ago_pe)]]
  }

<br>
<em>pull_annual_rev_and_ni(symbol):</em>
<br>Pulls Revenue and Net Income for last three available annual reports from zacks.com
Returns dictionary as follows:
{'SYMBOL': (last date, last_rev, last_ni), (prev date, prev_rev, prev_ni), 
            (two_yrs_ago_date, two_yrs_ago_rev, two_yrs_ago, ni)}
            
<br> 
<br><em>def get_price_change(symbol, beg_date, days_to_add):</em>
<br>Returns stock price difference for given symbol between the start_date and 
date after days_to_add is added to start_date.
<br>Assumes dates are given as strings in format MM/DD/YYYY.
<br>Returns begining stock price, ending stock price and difference.
