read test.csv
write test2.csv

column_add other test
column_order two "one bird" other test
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

col test
| return

col other
| return
