reset
set xlabel 'number of which time kthread-run'
set ylabel 'time (ns)'
set title 'khttpd kthread-run cost'
set term png enhanced font 'Verdana,10'
set output 'bench.png'
set key left

plot [0:][0:] \
'kthread_run_cost.txt' using 1:2 with points title 'Avg. time elapsed'