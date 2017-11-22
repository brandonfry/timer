# timer

This project spanned from my love of timeit results and my loathe of using it, as well as a curiosity about decorators. iPython's magic %%timeit covers much of this module's ease-of-use functionality, but I wanted my own, so here we are. 

The code is perfectly functional as of right now, with the caveat that it can't handle dot notation for some reason. I.e., if a decorated function is in a second file outside of __main__, it should be imported like "from x import y" rather than doing "import x" and using dot notation "x.y()" to access the function y.

The main usage is to easily do multiple time trials via timeit now that I've removed the barrier of the module's ridiculous stmt and setup strings. Decorated functions (@timer.timerit(num, out)) run for the given num of times and either out=1 prints to the screen and log file or out=0 prints only to a log file.

Also included is a standalone implementation of a single-run timer using Python's high performance counter. This works much the same, decorating functions as @timer.timertime(out).

Finally, there is a simple module to clear the log file.
