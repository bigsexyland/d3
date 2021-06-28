#!/usr/bin/env python
# D3 Paragon Calculator
# Get total paragon by combining seasonal + non seasonal paragon
# or seasonal paragon needed to reach non seasonal goal
# It doesn't matter which is which, they are valued equally
# Inspired by: https://www.d3bg.org/paragon-calculator/en.php
# Data from: https://www.diablofans.com/forums/diablo-forums/diablo-iii-general-discussion/130338-paragon-10000
# And: https://docs.google.com/spreadsheets/d/1MIVWYG18yayYU52xFPIH2iT-N_Yap3_UoQh_ZSHndlY/edit#gid=0

import sys
import csv


class ParagonCalc(object):
    def __init__(
        self,
        paragon_seasonal,
        paragon_non_seasonal,
        paragon_goal,
        paragon_halfway,
        paragon_file,
        verbose,
    ):

        self.paragon_seasonal = paragon_seasonal
        self.paragon_non_seasonal = paragon_non_seasonal
        self.paragon_goal = paragon_goal
        self.paragon_halfway = paragon_halfway
        self.paragon_file = paragon_file
        self.paragon_max = 10000
        self.verbose = verbose
        self._paragons = None

    @property
    def paragons(self):
        if self._paragons is None:
            self._paragons = self.get_paragon_table()
        return self._paragons

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

    def get_paragon_total(self):
        # Add seasonal + non seasonal to get total paragon level
        # Max of 10000 paragon since chart stops here
        xp_combined = self.paragons[self.paragon_seasonal]['total'] + self.paragons[self.paragon_non_seasonal]['total']
        if xp_combined > self.paragons[self.paragon_max]['total']:
            return('Seasonal: {} Non Seasonal: {} Total: {} (MAX)'.format(self.paragon_seasonal, self.paragon_non_seasonal, self.paragon_max))

        if self.paragon_seasonal > self.paragon_non_seasonal:
            higher = self.paragon_seasonal
        else:
            higher = self.paragon_non_seasonal
        if self.verbose:
            print('Checking using higher paragon: {}'.format(higher))

        for level, data in self.paragons.iteritems():
            if level >= higher:
                if xp_combined < data['total']:
                    total = level - 1
                    if self.verbose:
                        print('XP Combined: {} Total: {}'.format(xp_combined, total))
                    break
        return('Non Seasonal: {} Seasonal: {} Total: {}'.format(self.paragon_non_seasonal, self.paragon_seasonal, total))

    def get_paragon_goal(self):
        # Get seasonal paragon needed to reach a non seasonal paragon goal
        # Max of 10000 paragon since chart stops here
        if self.paragon_goal <= self.paragon_non_seasonal:
            return('Goal: {} Non Seasonal: {} Goal already achieved!'.format(self.paragon_goal, self.paragon_non_seasonal))

        if self.paragon_goal >= self.paragon_max:
            self.paragon_goal = self.paragon_max

        xp_current = self.paragons[self.paragon_non_seasonal]['total']
        xp_goal = self.paragons[self.paragon_goal]['total']

        for level, data in self.paragons.iteritems():
            if data['total'] + xp_current >= xp_goal:
                paragon_goal = level
                if self.verbose:
                    print('XP Goal: {} Paragon Goal: {}'.format(xp_goal, paragon_goal))
                break
        if self.paragon_goal >= self.paragon_max:
            return('Goal: {} (MAX) Non Seasonal: {} Seasonal Needed: {}'.format(self.paragon_goal, self.paragon_non_seasonal, paragon_goal))
        else:
            return('Goal: {} Non Seasonal: {} Seasonal Needed: {}'.format(self.paragon_goal, self.paragon_non_seasonal, paragon_goal))

    def get_paragon_halfway(self):
        # Get halfway point to desired paragon
        # Handle special case '1' which returns 1000-10000 by thousands
        if self.paragon_halfway != 1:
            return self._get_paragon_halfway(self.paragon_halfway)
        else:
            thousands = ''
            for thousand in xrange(1000, 11000, 1000):
                thousands += self._get_paragon_halfway(thousand)
                thousands += '<br>\n'
            return thousands

    def _get_paragon_halfway(self, halfway):
        # Get halfway point to desired paragon passed as argument
        level_half = None
        total = 0
        if halfway > self.paragon_max:
            return('Halfway to {}: {} (MAX={})!'.format(halfway, level_half, self.paragon_max))
        elif halfway < 2:
            return('Halfway to {}: {} (MIN=2)!'.format(halfway, level_half, self.paragon_max))

        xp_half = self.paragons[halfway]['total'] / 2
        for level, data in self.paragons.iteritems():
            total += data['next']
            if xp_half <= total:
                level_half = level
                break
        return('Halfway to {}: {}'.format(halfway, level_half))


if __name__ == '__main__':
    sys.exit("This is a library")
