# Navigate to the directory containing the .xyz files
cd /red/roitberg/nick_analysis/Extracts/Others

# Create a file to store the counts
> frame_counts.txt

# Loop through all .xyz files and count occurrences of "Frame"
for file in *.xyz Broke/*.xyz; do
    count=$(grep -c Frame "$file")
    echo "$file: $count" >> frame_counts.txt
done
