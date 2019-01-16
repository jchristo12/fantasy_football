load data local infile "C:/Users/Joe/Downloads/armchair_analysis/DEFENSE.csv"
into table nfl_stats.DEFENSE
fields terminated by ","
lines terminated by "\n"
ignore 1 lines
;