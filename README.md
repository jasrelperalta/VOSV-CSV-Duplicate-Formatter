# VOSV-CSV Duplicate Formatter

## Description

This script is used to format a CSV file containing duplicate entries into a CSV file containing all the entries with the duplicates removed. The script also concatenates the IDs of the duplicate entries into a single column with the entry it was duplicated from. By setting a threshold for the minimum similarity score, the script will only consider entries with a similarity score above the threshold to be duplicates by using the Szymkiewicz-Simpson coeffiecient as the similarity metric.

## Dependencies

This script requires Python 3.6 or later to run. It also requires the following Python packages:

* strsimpy

## Usage

The script is run from the command line with the following command:

``` bash
python3 format-vosv-csv.py

```

The script reads an input CSV file and writes to an output CSV file. The input CSV file must be specified as "Citation-Organization.csv" and the output CSV file will be specified as "Citation-Organization-Filtered.csv

The user will then be prompted to enter the minimum similarity score. The minimum similarity score is the minimum similarity score between two entries for them to be considered duplicates. The minimum similarity score must be a float value between 0 and 1. The minimum similarity score I recommend is 0.15.

## Issue

If the entry is too vague, the entry will be too general and will catch too many entries. For example, if the entry is containing only 'insead, fontainebleau, france', most departments and universities will be caught by this entry.

## Author

* Jasrel Peralta
