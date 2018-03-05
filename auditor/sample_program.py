#!/usr/local/bin/auditor

read test.csv
write test2.csv

column_add test bird_name
column_order two one color bird_name test
column_rename "two birds" two

separator ,
quotechar "

col color 7
| strip_whitespace
| done

col one 10
| date_parse
| done

col test 5
| lookup test_lookup.json two
| blacklist test_blacklist.newline
| done

col bird_name 5
| lookup color_lookup.yaml color
| done

col two -5
| date_parse
| greater_than one
| done
