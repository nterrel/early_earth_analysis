cd /red/roitberg/nick_analysis/Extracts/Others

# Create a file to store the counts
> frame_counts.txt

for file in *.xyz Broke/*.xyz; do
    count=$(grep -c Frame "$file")
    echo "$file: $count" >> frame_counts.txt
done
