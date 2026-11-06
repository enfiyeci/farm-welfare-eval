#!/bin/zsh
# usage: fetch.sh <url-list> <outdir> <ext> <prefix>
list=$1; out=$2; ext=$3; pre=$4
mkdir -p "$out"; : > "$out/_log.tsv"; n=0
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
while read -r u; do
  [ -z "$u" ] && continue
  n=$((n+1)); f=$(printf "%s%03d.%s" "$pre" $n "$ext")
  r=$(curl -sL --max-time 90 --max-filesize 80000000 -A "$UA" -o "$out/$f" -w '%{http_code}\t%{content_type}' "$u")
  printf "%s\t%s\t%s\n" "$f" "$r" "$u" >> "$out/_log.tsv"
  sleep 0.4
done < "$list"
echo DONE >> "$out/_done"
