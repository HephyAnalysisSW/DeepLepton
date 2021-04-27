# 

def cputime(id):

    for sj in jobs(id).subjobs:
        if sj.status == 'running':
            print ( f'CPUTIME: {float(sj.backend.cputime)/3600:d}' )
