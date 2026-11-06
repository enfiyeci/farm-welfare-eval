#!/bin/zsh
# usage: retry.sh <rawdir> <file>... ; refetches each file listed in <rawdir>/_log.tsv slowly and rewrites its log row
dir=$1; shift
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
for f in "$@"; do
  u=$(awk -F'\t' -v f="$f" '$1==f{print $4}' "$dir/_log.tsv")
  r=$(curl -sL --max-time 600 --max-filesize 200000000 -A "$UA" -H 'Accept: application/pdf,*/*' -o "$dir/$f" -w '%{http_code}\t%{content_type}' "$u")
  awk -F'\t' -v OFS='\t' -v f="$f" -v r="$r" '$1==f{split(r,a,"\t"); $2=a[1]; $3=a[2]} {print}' "$dir/_log.tsv" > "$dir/_log.tsv.new" && mv "$dir/_log.tsv.new" "$dir/_log.tsv"
  echo "$f $r"
  sleep 6
done
echo RETRY-DONE
