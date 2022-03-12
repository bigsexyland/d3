#!/usr/bin/env python
# D3 Paragon Calculator
# Get total paragon by combining seasonal + non seasonal paragon
# or seasonal paragon needed to reach non seasonal goal

import cgi
import sys
from paragon_calc import ParagonCalc


def main():

    print('Content-type: text/html\r\n\r\n')
    form = cgi.FieldStorage()
    output = None
    goal = None
    halfway = None
    non_seasonal = None
    seasonal = None
    if form.getvalue('non_seasonal'):
        non_seasonal = int(form.getvalue('non_seasonal'))
        if form.getvalue('seasonal'):
            seasonal = int(form.getvalue('seasonal'))
        elif form.getvalue('goal'):
            goal = int(form.getvalue('goal'))
    elif form.getvalue('halfway'):
        halfway = int(form.getvalue('halfway'))

    paragon_file = './p20000.csv'
    verbose = False
    paragons = ParagonCalc(
        paragon_seasonal=seasonal,
        paragon_non_seasonal=non_seasonal,
        paragon_goal=goal,
        paragon_halfway=halfway,
        paragon_file=paragon_file,
        verbose=verbose,
    )
    if seasonal:
        output = paragons.get_paragon_total()
    elif goal:
        output = paragons.get_paragon_goal()
    elif halfway:
        output = paragons.get_paragon_halfway()

    print('''
<HTML>
<HEAD>
<TITLE>D3 Paragon Calculator</TITLE>
</HEAD>
<BODY>
<H1>D3 Paragon Calculator</H1>
<P>
<TABLE WIDTH=60% CELLPADDING=2 CELLSPACING=2>
<FORM METHOD="POST" ACTION="/~jon/d3/paragon_tool.cgi">
<TR><TD COLSPAN=2>
<P>
When a Diablo 3 Season ends, your Paragon is rolled over to your
Non Seasonal profile.
<P>
To calculate your Non Seasonal Paragon when the current Season ends,
enter your Non Seasonal and Seasonal paragon and press Submit.
<P>
To calculate the Paragon you need this Season to reach
your Goal Non Seasonal Paragon, enter your Non Seasonal and
Goal paragon and press Submit.
<P>
To calculate the Halfway point to an arbitrary Paragon,
enter that paragon and press Submit.  (Enter "1" to see a list of round-number
milestones)
<P>
The calculator\'s cap is 20,000 and is based on <A
HREF="https://d3.maxroll.gg/resources/experience-explained#Paragon-Experience-Table">Maxroll's\'</A> chart.
<BR>
</TD></TR></TABLE>
<P>
<TABLE WIDTH=60% CELLPADDING=2 CELLSPACING=2>
<TR><TD VALIGN="top">Non-Seasonal Paragon</TD><TD>
 <INPUT TYPE="number" NAME="non_seasonal" SIZE="1" MAXLENGTH="5">
</TD></TR>
<TR><TD VALIGN="top">Seasonal Paragon</TD><TD>
 <INPUT TYPE="number" NAME="seasonal" SIZE="1" MAXLENGTH="5">
</TD></TR>
<TR><TD VALIGN="top"> - OR -</TD><TD></TR>
<TR><TD VALIGN="top">Goal Paragon</TD><TD>
 <INPUT TYPE="number" NAME="goal" SIZE="1" MAXLENGTH="5">
</TD></TR>
<TR><TD VALIGN="top"> - OR -</TD><TD></TR>
<TR><TD VALIGN="top">Halfway Paragon</TD><TD>
 <INPUT TYPE="number" NAME="halfway" SIZE="1" MAXLENGTH="5">
</TD></TR>
<TR><TD>&nbsp;</TD><TD>
<INPUT TYPE="submit" VALUE="Submit"></FORM></TD></TR>
          ''')

    if output:
        print('<TR><TD bgcolor="green"><B>{}</B></TD></TR>'.format(output))

    print('''
</TABLE>
<P>
<A HREF="https://www.d3bg.org/paragon-calculator/">D3BG</A> inspired
this project.
</P>
<P>
<A HREF="https://github.com/bigsexyland/d3/">Source code</A> available.
</P></TD></TR>
</TABLE>
</BODY>
</HTML>
          ''')
    sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
