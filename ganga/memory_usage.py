#! /usr/bin/env python3

import matplotlib.pyplot as plt
from pathlib import Path
import re
from datetime import datetime, timedelta

workspace = Path('/stash/user/liko/gangadir/workspace')
job=0


re_mem = re.compile(r'''
    ^006\s+\(.+\)\s+(?P<datetime>[0-9\-]+\s+[0-9:]+).+\n
    \s+(?P<memory>\d+).+\n
    .+\n
    .+\n
    \.{3}$
''', re.M | re.X)

result = []
for condorLog in workspace.glob(f'liko/LocalXML/{job}/*/output/condorLog'):
    sjnr = condorLog.parts[-3]
    start = None
    tl = []
    ml = []
    with open(condorLog, 'r') as cl:
        data = cl.read()
    for m in re_mem.finditer(data):
        dt = datetime.strptime(m.group('datetime'), '%Y-%m-%d %H:%M:%S')
        if start is None:
            start = dt
            time = 0
        else:
            time = (dt - start) / timedelta(minutes=1)
        tl.append( time )
        ml.append( int(m.group('memory') ) )
    result.append( (sjnr, tl, ml) )

fig, ax = plt.subplots()

for sj, tl, ml in result:
    ax.plot(tl,ml,label='Job %s' % sj)


ax.set_xlabel('minutes')  # Add an x-label to the axes.
ax.set_ylabel('MB')  # Add a y-label to the axes.
ax.set_title("Memoryconsumption")  # Add a title to the axes.
#ax.legend()  # Add a legend.
fig.show()
