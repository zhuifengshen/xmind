#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.markerref
    ~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""

__author__ = "stanypub@gmail.com <Stany MARCEL>"

from . import const
from .mixin import WorkbookMixinElement


class MarkerId:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<MarkerId: %s>" % self

    def getFamilly(self):
        return self.name.split('-')[0]


MarkerId.starRed         = 'star-red'
MarkerId.starOrange      = 'star-orange'
MarkerId.starYellow      = 'star-yellow'
MarkerId.starBlue        = 'star-blue'
MarkerId.starGreen       = 'star-green'
MarkerId.starPurple      = 'star-purple'

MarkerId.priority1       = 'priority-1'
MarkerId.priority2       = 'priority-2'
MarkerId.priority3       = 'priority-3'
MarkerId.priority4       = 'priority-4'
MarkerId.priority5       = 'priority-5'
MarkerId.priority6       = 'priority-6'
MarkerId.priority7       = 'priority-7'
MarkerId.priority8       = 'priority-8'
MarkerId.priority9       = 'priority-9'

MarkerId.smileySmile     = 'smiley-smile'
MarkerId.smileyLaugh     = 'smiley-laugh'
MarkerId.smileyAngry     = 'smiley-angry'
MarkerId.smileyCry       = 'smiley-cry'
MarkerId.smileySurprise  = 'smiley-surprise'
MarkerId.smileyBoring    = 'smiley-boring'

MarkerId.task0_8         = 'task-start'
MarkerId.task1_8         = 'task-oct'
MarkerId.task2_8         = 'task-quarter'
MarkerId.task3_8         = 'task-3oct'
MarkerId.task4_8         = 'task-half'
MarkerId.task5_8         = 'task-5oct'
MarkerId.task6_8         = 'task-3quar'
MarkerId.task7_8         = 'task-7oct'
MarkerId.task8_8         = 'task-done'

MarkerId.flagRed         = 'flag-red'
MarkerId.flagOrange      = 'flag-orange'
MarkerId.flagYellow      = 'flag-yellow'
MarkerId.flagBlue        = 'flag-blue'
MarkerId.flagGreen       = 'flag-green'
MarkerId.flagPurple      = 'flag-purple'

MarkerId.peopleRed       = 'people-red'
MarkerId.peopleOrange    = 'people-orange'
MarkerId.peopleYellow    = 'people-yellow'
MarkerId.peopleBlue      = 'people-blue'
MarkerId.peopleGreen     = 'people-green'
MarkerId.peoplePurple    = 'people-purple'

MarkerId.arrowUp         = 'arrow-up'
MarkerId.arrowUpRight    = 'arrow-up-right'
MarkerId.arrowRight      = 'arrow-right'
MarkerId.arrowDownRight  = 'arrow-down-right'
MarkerId.arrowDown       = 'arrow-down'
MarkerId.arrowDownLeft   = 'arrow-down-left'
MarkerId.arrowLeft       = 'arrow-left'
MarkerId.arrowUpLeft     = 'arrow-up-left'
MarkerId.arrowRefresh    = 'arrow-refresh'

MarkerId.symbolPlus      = 'symbol-plus'
MarkerId.symbolMinus     = 'symbol-minus'
MarkerId.symbolQuestion  = 'symbol-question'
MarkerId.symbolExclam    = 'symbol-exclam'
MarkerId.symbolInfo      = 'symbol-info'
MarkerId.symbolWrong     = 'symbol-wrong'
MarkerId.symbolRight     = 'symbol-right'

MarkerId.monthJan        = 'month-jan'
MarkerId.monthFeb        = 'month-feb'
MarkerId.monthMar        = 'month-mar'
MarkerId.monthApr        = 'month-apr'
MarkerId.monthMay        = 'month-may'
MarkerId.monthJun        = 'month-jun'
MarkerId.monthJul        = 'month-jul'
MarkerId.monthAug        = 'month-aug'
MarkerId.monthSep        = 'month-sep'
MarkerId.monthOct        = 'month-oct'
MarkerId.monthNov        = 'month-nov'
MarkerId.monthDec        = 'month-dec'

MarkerId.weekSun         = 'week-sun'
MarkerId.weekMon         = 'week-mon'
MarkerId.weekTue         = 'week-tue'
MarkerId.weekWed         = 'week-wed'
MarkerId.weekThu         = 'week-thu'
MarkerId.weekFri         = 'week-fri'
MarkerId.weekSat         = 'week-sat'


class MarkerRefsElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_MARKERREFS

    def __init__(self, node=None, ownerWorkbook=None):
        super(MarkerRefsElement, self).__init__(node, ownerWorkbook)

class MarkerRefElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_MARKERREF

    def __init__(self, node=None, ownerWorkbook=None):
        super(MarkerRefElement, self).__init__(node, ownerWorkbook)

    def getMarkerId(self):
        return MarkerId(self.getAttribute(const.ATTR_MARKERID))

    def setMarkerId(self, val):
        self.setAttribute(const.ATTR_MARKERID, str(val))

def main():
    pass

if __name__ == '__main__':
    main()
