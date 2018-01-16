read test.csv
write test2.csv

column_order "two birds" one

separator ,
quotechar "

col one
| date_parse
| return

col "two birds"
| return
