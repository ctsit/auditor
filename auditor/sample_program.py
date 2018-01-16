read test.csv
write test2.csv

column_order one

separator ,
quotechar "

col one
| date_parse
| return
