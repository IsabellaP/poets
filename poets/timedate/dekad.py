# Copyright (c) 2014, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Author: Thomas Mistelbauer thomas.mistelbauer@geo.tuwien.ac.at
# Creation date: 2014-08-05

"""
Module provides functions for date manipulation on a dekadal basis
"""

import datetime
import calendar
import pandas as pd


def dekad_index(begin, end=None):
    """Creates a pandas datetime index on a decadal basis.

    Parameters
    ----------
    begin : datetime.date
        datetime index start date
    end : datetime.date, optional
        datetime index end date, set to current date if None

    Returns
    -------
    dtindex : pandas.DatetimeIndex
        dekadal datetime index
    """

    if end is None:
        end = datetime.date.today()

    mon_begin = datetime.date(begin.year, begin.month, 1)
    mon_end = datetime.date(end.year, end.month, 1)

    daterange = pd.date_range(mon_begin, mon_end, freq='MS')

    dates = []

    for i, dat in enumerate(daterange):
        lday = calendar.monthrange(dat.year, dat.month)[1]
        if i == 0 and begin.day > 1:
            if begin.day < 11:
                if daterange.size == 1:
                    if end.day < 11:
                        dekads = [10]
                    elif end.day >= 11 and end.day < 21:
                        dekads = [10, 20]
                    else:
                        dekads = [10, 20, lday]
                else:
                    dekads = [10, 20, lday]
            elif begin.day >= 11 and begin.day < 21:
                if daterange.size == 1:
                    if end.day < 21:
                        dekads = [20]
                    else:
                        dekads = [20, lday]
                else:
                    dekads = [20, lday]
            else:
                dekads = [lday]
        elif i == (len(daterange) - 1) and end.day < 21:
            if end.day < 11:
                dekads = [10]
            else:
                dekads = [10, 20]
        else:
            dekads = [10, 20, lday]

        for j in dekads:
            dates.append(pd.datetime(dat.year, dat.month, j))

    dtindex = pd.DatetimeIndex(dates)

    return dtindex


def check_dekad(date):
    """Checks the dekad of a date and returns the dekad date.

    Parameters
    ----------
    date : datetime.datetime
        Date to check

    Returns
    -------
    new_date : datetime.datetime
        Date of the dekad
    """
    if date.day < 11:
        dekad = 10
    elif date.day > 10 and date.day < 21:
        dekad = 20
    else:
        dekad = calendar.monthrange(date.year, date.month)[1]

    new_date = datetime.datetime(date.year, date.month, dekad)

    return new_date


def dekad2day(year, month, dekad):
    """Gets the day of a dekad.

    Parameters
    ----------
    year : int
        year of the date
    month : int
        month of the date
    dekad : int
        dekad of the date

    Returns
    -------
    day : int
        Day value for the dekad
    """

    if dekad == 1:
        day = 10
    elif dekad == 2:
        day = 20
    elif dekad == 3:
        day = calendar.monthrange(year, month)[1]

    return day


def day2dekad(day):
    """Returns the dekad of a day.

    Parameters
    ----------
    day : int
        day of the date

    Returns
    -------
    dekad : int
        number of the dekad in a month
    """

    if day < 11:
        dekad = 1
    elif day > 10 and day < 21:
        dekad = 2
    else:
        dekad = 3

    return dekad


def get_dekad_period(date):

    period = []

    for dat in date:

        d = check_dekad(dat)
        dekad = day2dekad(d.day)
        per = dekad + ((d.month - 1) * 3)
        period.append(per)

    return period


if __name__ == "__main__":
    pass
