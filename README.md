# auditor v2.0.0
Makes sure your CSV's remain compliant

There are times that CSV files need either cleaning, or replacement of certain items, or filtering 
of specific values or sorting etc. 

Enter Auditor. This software is meant to scan through and clean your csv in various ways and make sure that
everything is ready to go before your application needs to do the rest of the data processing.

## Configs

Auditor no longer uses configs as of version `2.0.0`. Please consult the examples to figure out how to
migrate to the new system.

## Usage

Auditor defines a Domain Specific Language (D.S.L) which is yet to be named. It allows one to write an
auditor program that operates on a csv on a row by row basis to do things like rename columns, apply
data transforms, remove whitespace, compare one value in a row to another, whitelist and blacklist items,
and do lookups.

`$ auditor <path_to_my_program>`

## Development

Adding further features to auditor falls into two categories: new column transforms and other things.
If all you need is to add a transform to the `col` block to implement something, for example fixed length
fields, follow the following steps:

  * fork this repo
  * clone this repository
  * install the dev-requirements with `pip3 install -r dev-requirements.txt`
  * 'cd <repo-clone-directory>/auditor/transforms'
  * run `python3 ../dev_scripts/make_new_col_transform.py <transforms-you-need>...`
  * edit the code till it works. Testing against a program and data file in the examples directory
  * submit a pull request

## Examples

Look in the examples folder for a sample program of all features that are currently implemented.
