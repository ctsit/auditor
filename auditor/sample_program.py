read test.csv
write test2.csv

column_add other test
column_order two "one bird" other test
column_rename "two birds" two
column_rename one "one bird"

separator ,
quotechar "

col "one bird" 10
| date_parse
| done

col two
| date_parse
| greater_equal "one bird"
| done

col test
| lookup test_lookup.json two
| done

col other
| done
