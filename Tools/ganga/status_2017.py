
def tf(s):

    h = int(s/3600)
    s = s - h * 3600
    m = int(s/60)
    s = int(s - m * 60)

    return f'{h:02d}:{m:02d}:{s:02d}'

walltime = []
cputime = []
summary = {}
for j in range(142,202):
    for sj in jobs(j).subjobs:
        if sj.status in summary:
            summary[sj.status] += 1
        else:
            summary[sj.status] = 1
        ft = sj.time.backend_final()
        rt = sj.time.backend_running()
        if rt and ft:
            wt = (ft-rt).total_seconds()
            c = float(sj.backend.cputime)
            if wt>60 and c>60:
                walltime.append((ft-rt).total_seconds())
                cputime.append( c )

print ( 'Job Status' )
for k, v in summary.items():
    print ( k, v )

print ( f'CPUTime  Min : {tf(min(cputime))}' )
print ( f'CPUTime  Max : {tf(max(cputime))}' )
print ( f'CPUTime  Avg : {tf(sum(cputime)/len(cputime))}' )
print ( f'WallTime Min : {tf(min(walltime))}' )
print ( f'WallTime Max : {tf(max(walltime))}' )
print ( f'WallTime Avg : {tf(sum(walltime)/len(walltime))}' )
