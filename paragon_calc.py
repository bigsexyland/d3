#!/usr/bin/env python
# D3 Paragon Calculator
# Combines Seasonal + Non Seasonal to determine resulting Paragon
# It doesn't matter which is which, they are valued equally
# Inspired by: https://www.d3bg.org/paragon-calculator/en.php
# Data from: https://www.diablofans.com/forums/diablo-forums/diablo-iii-general-discussion/130338-paragon-10000
# And: https://docs.google.com/spreadsheets/d/1MIVWYG18yayYU52xFPIH2iT-N_Yap3_UoQh_ZSHndlY/edit#gid=0

import sys
import argparse
import csv


class ParagonCalc(object):
    def __init__(
        self,
        paragon1,
        paragon2,
        paragon_file,
        verbose,
    ):

        self.paragon1 = paragon1
        self.paragon2 = paragon2
        self.paragon_file = paragon_file
        self.verbose = verbose

    def get_paragon_table(self):
        """Get the list of paragon data from a csv file
        """
        paragons = {}
        with open(self.paragon_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            c = 0
            for row in csv_reader:
                if c == 0:
                    """Level,Total,Next level,Difference
                    """
                    if self.verbose:
                        print('Headers: {}'.format(', '.join(row)))
                    c += 1
                else:
                    """
                    0,0,"7,200,000",
                    1,"7,200,000","8,640,000","1,440,000"
                    2,"15,840,000","10,080,000","1,440,000"
                    """
                    level = int(row[0].replace(',', ''))
                    paragons[level] = {}
                    paragons[level]['total'] = int(row[1].replace(',', ''))
                    paragons[level]['next'] = int(row[2].replace(',', ''))
                    paragons[level]['difference'] = int(row[3].replace(',', ''))
                    c += 1
        if self.verbose:
            print('Read {} rows in file {}'.format(c, self.paragon_file))
        return paragons

    def run(self):
        # max of 10000 paragon since chart stops here
        result = 10000
        paragons = self.get_paragon_table()
        combined_xp = paragons[self.paragon1]['total'] + paragons[self.paragon2]['total']
        if combined_xp > paragons[result]['total']:
            print('Seasonal: {} Non Seasonal: {} Result: {} (MAX)'.format(self.paragon1, self.paragon2, result))
            return result

        if self.paragon1 > self.paragon2:
            higher = self.paragon1
        else:
            higher = self.paragon2
        if self.verbose:
            print('Checking using higher paragon: {}'.format(higher))

        for level, data in paragons.iteritems():
            if level >= higher:
                if combined_xp < data['total']:
                    result = level - 1
                    if self.verbose:
                        print('Combined XP: {} Result: {}'.format(combined_xp, result))
                    break
        print('Seasonal: {} Non Seasonal: {} Result: {}'.format(self.paragon1, self.paragon2, result))
        return result


def main():
    parser = argparse.ArgumentParser(description='Calculate Paragons')
    parser.add_argument('--seasonal', '-s', type=int, required=True,
                        help='Seasonal paragon (integer)')
    parser.add_argument('--non_seasonal', '-n', type=int, required=True,
                        help='Non Seasonal paragon (integer)')
    parser.add_argument('--paragon_file', '-p', default='p10000.csv',
                        help='File to get paragon definitions from, csv')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print verbose output')

    args = parser.parse_args()

    paragons = ParagonCalc(
        paragon1=args.seasonal,
        paragon2=args.non_seasonal,
        paragon_file=args.paragon_file,
        verbose=args.verbose,
    )
    paragons.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
