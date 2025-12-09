import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.write("""
# Stock Price App

Shows the stock **closing price**, ***volume***, and other metrics for the company entered.
""")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Enter ticker symbol(s)", "", help="Enter one or more ticker symbols separated by commas (e.g., AAPL, GOOGL, MSFT)")
with col2:
    st.write("")

col3, col4 = st.columns(2)
with col3:
    start_date = st.date_input("Start Date", datetime(2020, 1, 1))
with col4:
    end_date = st.date_input("End Date", datetime.today())

show_high_low = st.checkbox("Show High/Low Prices", value=False)
show_open = st.checkbox("Show Open Prices", value=False)

def get_stock_data(ticker_symbol, start, end):
    try:
        tickerData = yf.Ticker(ticker_symbol)
        info = tickerData.info
        company_name = info.get('longName', ticker_symbol)
        tickerDf = tickerData.history(start=start, end=end)
        if tickerDf.empty:
            return None, None, f"No data found for {ticker_symbol}"
        return tickerDf, company_name, None
    except Exception as e:
        return None, None, f"Error fetching data for {ticker_symbol}: {str(e)}"

def display_stock(ticker_symbol, start, end, show_comparison=False):
    tickerDf, company_name, error = get_stock_data(ticker_symbol, start, end)
    
    if error:
        st.error(error)
        return None
    
    st.subheader(f"{company_name} ({ticker_symbol})")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Close", f"${tickerDf['Close'].iloc[-1]:.2f}")
    with col2:
        st.metric("Latest Volume", f"{tickerDf['Volume'].iloc[-1]:,.0f}")
    with col3:
        change = tickerDf['Close'].iloc[-1] - tickerDf['Close'].iloc[0]
        pct_change = (change / tickerDf['Close'].iloc[0]) * 100
        st.metric("Period Change", f"${change:.2f}", f"{pct_change:.2f}%")
    with col4:
        st.metric("Avg Volume", f"{tickerDf['Volume'].mean():,.0f}")
    
    return tickerDf

if st.button('Submit'):
    if not name.strip():
        st.error("Please enter at least one ticker symbol")
    else:
        tickers = [t.strip().upper() for t in name.split(',')]
        
        all_close_data = pd.DataFrame()
        all_volume_data = pd.DataFrame()
        all_high_data = pd.DataFrame()
        all_low_data = pd.DataFrame()
        all_open_data = pd.DataFrame()
        
        for ticker in tickers:
            if ticker:
                tickerDf = display_stock(ticker, start_date, end_date)
                if tickerDf is not None:
                    all_close_data[ticker] = tickerDf['Close']
                    all_volume_data[ticker] = tickerDf['Volume']
                    all_high_data[ticker] = tickerDf['High']
                    all_low_data[ticker] = tickerDf['Low']
                    all_open_data[ticker] = tickerDf['Open']
                st.markdown("---")
        
        if not all_close_data.empty:
            st.write("## Closing Price Comparison")
            st.line_chart(all_close_data)
            
            st.write("## Volume Comparison")
            st.line_chart(all_volume_data)
            
            if show_high_low:
                st.write("## High Price Comparison")
                st.line_chart(all_high_data)
                st.write("## Low Price Comparison")
                st.line_chart(all_low_data)
            
            if show_open:
                st.write("## Open Price Comparison")
                st.line_chart(all_open_data)
            
            st.write("## Download Data")
            combined_data = pd.DataFrame()
            for ticker in tickers:
                if ticker in all_close_data.columns:
                    combined_data[f'{ticker}_Close'] = all_close_data[ticker]
                    combined_data[f'{ticker}_Open'] = all_open_data[ticker]
                    combined_data[f'{ticker}_High'] = all_high_data[ticker]
                    combined_data[f'{ticker}_Low'] = all_low_data[ticker]
                    combined_data[f'{ticker}_Volume'] = all_volume_data[ticker]
            
            csv = combined_data.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"stock_data_{'-'.join(tickers)}_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
