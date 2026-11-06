#!/bin/zsh
# usage: uga-pdfs.sh <pull-folder> ; waits for the UGA tips crawl, then fetches every newsletter PDF its pages link
P=${1:A}; here=${0:A:h}
until [ -f "$P/raw/uga-tips/_done" ]; do sleep 5; done
grep -ohE 'https://www.poultryventilation.com/wp-content/uploads/[^"]+\.pdf' "$P"/raw/uga-tips/*.html | sort -u > "$P/inputs/uga-housing-tips-pdf-urls.txt"
"$here/fetch.sh" "$P/inputs/uga-housing-tips-pdf-urls.txt" "$P/raw/uga-pdf" pdf g
