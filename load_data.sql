load data local infile 'C:/Users/Joe/Downloads/armchair_analysis/BLOCK.csv'
into table nfl_stats.BLOCK
fields terminated by ','
lines terminated by '\r\n'
ignore 1 lines
;