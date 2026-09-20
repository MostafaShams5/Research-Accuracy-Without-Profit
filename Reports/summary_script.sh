echo "=== MAIN.TEX EXTRACT ==="
grep -E '\\(title|author|abstract|section|subsection)' main.tex

echo "=== CODE EXTRACT ==="
for f in Code/*.py; do
    echo "--- $f ---"
    grep -E '^(def |class |"""|#)' "$f" | head -n 15
done

echo "=== DATA SAMPLE ==="
head -n 3 Data/master_feature_table.csv | cut -d',' -f1-10

echo "=== PEER REVIEWS EXTRACT ==="
for f in Peer-Reviews/*.pdf; do
    echo "--- $f ---"
    pdftotext "$f" - | head -n 25
done
