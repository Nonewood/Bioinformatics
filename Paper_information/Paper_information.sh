#！/usr/bin/bash
# doi
python3 advanced_paper_informational.py -l "10.1016/S0140-6736(19)32319-0"

# doi file, a list of doi, line break
#python3 advanced_paper_informational.py -f doilist.txt

# dowload the pdf, only support one doi in current version +.+, TBD
python3 scihub.py -d "10.1016/S0140-6736(19)32319-0"
