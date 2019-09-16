#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# ## Player Count

# * Display the total number of players
# 

# In[2]:


# Remove the duplicated Screen Names
purchase_data.drop_duplicates(["SN"])
total_players = len(purchase_data.drop_duplicates(["SN"])) 

# Show the total number of players
player_count = pd.DataFrame([total_players], columns =['Total Players'])
player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


# Calculate the number of unique items
purchase_data.drop_duplicates(["Item ID"])
total_items = len(purchase_data.drop_duplicates(["Item ID"])) 

# Calculate the average purchase price
average_price = purchase_data["Price"].mean()

# Calculate the total number of purchases
total_purchases = purchase_data["Purchase ID"].count()

# Calculate the total revenue
total_revenue = purchase_data["Price"].sum()

# Display the summary data frame
summary_table = pd.DataFrame({"Number of Unique Items": [total_items],
                              "Average Price": [average_price],
                              "Number of Purchases": [total_purchases], 
                              "Total Revenue": [total_revenue]})
summary_table['Average Price'] = summary_table['Average Price'].map('${:,.2f}'.format)
summary_table['Total Revenue'] = summary_table['Total Revenue'].map('${:,.2f}'.format)
summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


# Remove all the duplicated names
genPurchase_data = pd.DataFrame(purchase_data, columns = ["SN", "Gender"]).drop_duplicates()

# Find the number of person in each gender 
genCount = genPurchase_data["Gender"].value_counts()

# Find the percentage of each gender 
genPercCount = round((genCount)/len(genPurchase_data['Gender'])*100,2)

# Show summary table
summarytable = pd.DataFrame({"Total Count": genCount, "Percentage of Players":genPercCount})
summarytable


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


# Find purchase count broken by gender
purchase_count = purchase_data.groupby(['Gender']).count()["Price"]

#Find average purchase price broken by gender
average_purchase = purchase_data.groupby(['Gender']).mean()["Price"]

# Find total purchase value broken by gender
total_purchase_value = purchase_data.groupby(['Gender']).sum()["Price"]

# Calculate average purchase total per person by gender
avg_total_purchase_person = total_purchase_value / genCount

# Display the summary data frame
pa_gender_table = pd.DataFrame({"Purchase Count":purchase_count,
                                "Average Purchase Price":average_purchase.map("${:.2f}".format),
                                "Total Purchase Value":total_purchase_value.map("${:.2f}".format),
                                "Avg Total Purchase per Person":avg_total_purchase_person.map("${:.2f}".format)})
pa_gender_table


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[6]:


# Create the bins of 4 years (i.e. &lt;10, 10-14, 15-19, etc.)in which the data will be held
bins = [-1, 9, 14, 19, 24, 29, 34, 39, 1000]
# Name the bins
name_bins = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Categorize the players using bins 
uniqueDataFrame = purchase_data.drop_duplicates(subset= 'SN', keep = 'first', inplace = False)
uniqueDataFrame["Age Group"] = pd.cut(uniqueDataFrame["Age"], bins, labels=name_bins)
uniqueDataFrame

# Calculate numbers of players per age group
age_purchase_data= uniqueDataFrame['Age Group'].value_counts()

# Calculate percent of players per age group
age_purchase_data_percents = age_purchase_data / total_players * 100

# Create summary table
table = pd.DataFrame({"Total Count":age_purchase_data, "Percentage of Players": age_purchase_data_percents})

# Round numbers to two decimals
table = table.round(2)
table


# ## Purchasing Analysis (Age)

# 
# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


# Bin the purchase data by age
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], bins, labels=name_bins)

#Calculate the average purchase total per age groups
age_purchase_total = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")

#Calculate the average purchase price per age groups
age_avrg = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")

#Calculate the purchase count per age groups
age_counts = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

#Normalize total purchase
norm_total = age_purchase_total/table["Total Count"]

# Convert calculations to DataFrame
tabel_calculation = pd.DataFrame({"Purchase Count":age_counts,
                                 "Average Purchase Price":age_avrg.map("${:.2f}".format),
                                 "Total Purchase Value":age_purchase_total.map("${:.2f}".format),
                                 "Avg Total Purchase per Person":norm_total.map("${:.2f}".format)})
tabel_calculation


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[8]:


#Basic calculations 
player_total = purchase_data.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
player_avrg = purchase_data.groupby(["SN"]).mean()["Price"].rename("Average Purchase Price")
player_count = purchase_data.groupby(["SN"]).count()["Price"].rename("Purchase Count")

#Convert to DataFrame
player_data = pd.DataFrame({"Purchase Count":player_count,
                           "Average Purchase Price":player_avrg.map("${:.2f}".format),
                           "Total Purchase Value":player_total})

#Sort
sort_player = player_data.sort_values("Total Purchase Value", ascending=False)

#Display the top 5 spenders in the game by total purchase value
sort_player.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:


#Get item data
item_data = purchase_data.loc[:,("Item ID", "Item Name", "Price")]

# Basic calculations
total_item_purch = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Value")
avrg_item_purch = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"].rename("Item Price")
count_item_purch = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")

# Create new DataFrame showing the 5 most popular items by purchase count
item_table = pd.DataFrame({"Purchase Count":count_item_purch,
                         "Item Price":avrg_item_purch.map("${:.2f}".format),
                         "Total Purchase Value":total_item_purch.map("${:.2f}".format)})

#Sort values in table
sort_table = item_table.sort_values("Purchase Count", ascending=False)

#Show table
sort_table.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[10]:


#Assign new table using data without the previous sort
most_profitable_item = item_table

#Find the most profitable items sorted by total purchase
most_profitable_item = item_table.sort_values("Total Purchase Value", ascending=False)

#Show table
most_profitable_item.head()

