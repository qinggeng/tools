#-*- coding: utf-8 -*-
import datetime
def dateRange(startDate, endDate):
	day = startDate
	while day < endDate:
		day = day + datetime.timedelta(1)
		yield day
def workdays(startDate, endDate):
	return filter(lambda x: x.weekday() != 5 and x.weekday() != 6, dateRange(startDate, endDate))

