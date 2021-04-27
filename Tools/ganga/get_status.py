def get_status():

    summary = {}
    for j in jobs:
        for sj in j.subjobs:
            if sj.status in summary:
                summary[sj.status] += 1
            else:
                summary[sj.status] = 1

    for k, v in summary.items():
        print ( f'{k:10} : {v}' )
