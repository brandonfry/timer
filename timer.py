# -*- coding: utf-8 -*-
"""
Two simple wrapper functions to either time a single run of a decorated
function, or two run timeit.Timer() for multiple trials.

Copyright (C) Sat Nov 11 09:16:19 2017  Brandon C. Fry
brandoncfry@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from functools import wraps
import timeit
import time
#import inspect
#import importlib


def clear_log():
    """Clears the log of all values."""

    with open("timer_log.txt", "w") as f:
        pass


def log(value, name):
    """Logs the time stamp and result of a timing."""

    with open("timer_log.txt", "a") as f:
        t = str(time.time())
        value = str(value*1000)
        f.write("{}, {}: {} ms\n".format(name, t, value))


def timerit(num, output):
    """Calls timeit on the function given the number of trials. Output = 0
    for quiet mode, and = 1 to print the average time to the screen."""

    def timing_it(func):
        is_evaluating = False

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            nonlocal is_evaluating
            if is_evaluating:
                return func(*args, **kwargs)
            else:
                is_evaluating = True
                name = func.__name__
#                frm = inspect.stack()[1]
#                line = frm.code_context
                # __wrapped__ returns the function without the wrapper
                # Without this timeit goes into a recursive loop!
                t = timeit.Timer("ans = {}.__wrapped__(*{},**{})".format(name,
                                 args, kwargs),
                                 setup="from __main__ import {}".format(name))
                ttime = t.timeit(num)
                ans = func(*args, **kwargs)
                is_evaluating = False
                if output == 1:
                    print("{:.<30}{:0.6f} ms".format(name+":", ttime/num*1000))
                log(ttime/num, name)
                return ans
        return func_wrapper
    return timing_it


def timertime(output):
    """Runs one iteration of the function and records the execution time.
    Output = 0 for quiet mode, and = 1 to print the average time to
    the screen."""

    def timing(func):
        is_evaluating = False

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            nonlocal is_evaluating
            if is_evaluating:
                return func(*args, **kwargs)
            else:
                is_evaluating = True
                t1 = time.perf_counter()
                ans = func(*args, **kwargs)
                t2 = time.perf_counter()
                is_evaluating = False
                if output == 1:
                    print("{:.<30}{:0.6f} ms".format(func.__name__+":",
                          (t2-t1)*1000))
                log(t2-t1, func.__name__)
                return ans
        return func_wrapper
    return timing
