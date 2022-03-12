#!/usr/bin/env python
# D3 Paragon Calculator
# Maxroll published a paragon chart for levels 1-20,000 but the format
# differs from the original Diablofans format that paragon_calc expects.
# Convert Maxroll to Diablofans format.
# Maxroll: https://docs.google.com/spreadsheets/d/1Opipj41r5GBqVSVWW67cHiD0M8yJ_4-B7PKCDzoMq2s/edit?copiedFromTrash#gid=416995773
# Diablofans: https://www.diablofans.com/forums/diablo-forums/diablo-iii-general-discussion/130338-paragon-10000

import csv


# Get paragon data from maxroll csv file
maxroll_file = 'maxroll.csv'
maxroll_tmp = {}
with open(maxroll_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    c = 0
    for row in csv_reader:
        if c == 0:
            # Level,Exp Required,Exp Increase,ExpChangeLoL%,Total Exp Required,
            c += 1
        else:
            """ Maxroll:
            Level,Exp Required,Exp Increase,ExpChangeLoL%,Total Exp Required,
            0,0,0,0,0,,
            1,"7,200,000","1,440,000.00",,"7,200,000",
            2,"8,640,000","1,440,000.00",100.0%,"15,840,000",
            3,"10,080,000","1,440,000.00",100.0%,"25,920,000",
            4,"11,520,000","1,440,000.00",100.0%,"37,440,000",
                Desired:
            Level,Total,Next level,Difference
            0,0,"7,200,000",
            1,"7,200,000","8,640,000","1,440,000"
            2,"15,840,000","10,080,000","1,440,000"
            """
            level = int(row[0].replace(',', ''))
            maxroll_tmp[level] = {}
            maxroll_tmp[level]['total'] = row[4]
            maxroll_tmp[level]['next'] = row[1]
            maxroll_tmp[level]['difference'] = row[2]
        c += 1

    # Generate usable paragon dict based on data from csv
    # We can't update a dict while iterating through it, so use new dict
    maxroll_paragons = {}
    for k, v in maxroll_tmp.iteritems():
        maxroll_paragons[k] = {}
        try:
            maxroll_paragons[k]['next'] = maxroll_tmp[k + 1]['next']
        except KeyError:
            maxroll_paragons[k]['next'] = 0
        maxroll_paragons[k]['total'] = v['total']
        maxroll_paragons[k]['difference'] = v['difference']

    # Write output to new csv file
    paragon_file = 'p20000.csv'
    headers = ['Level', 'Total', 'Next level', 'Difference']
    with open(paragon_file, 'w') as csv_outfile:
        writer = csv.writer(csv_outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for k, v in maxroll_paragons.iteritems():
            line = [k, v['total'], v['next'], v['difference']]
            writer.writerow(line)
