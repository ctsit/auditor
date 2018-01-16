read test.csv
write test2.csv

column_order "two birds" one
column_rename "two birds" two
column_rename one "one bird"

separator ,
quotechar "

col "one bird"
| date_parse
| return

col two
| date_parse
| date_parse
| return
