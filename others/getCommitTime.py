import csv

log_file = csv.reader(open('change_log.csv'))

commits_file = csv.reader(open('target commits.csv'))
new_file = csv.writer(open('target_commits_time.csv', 'wb+'))

commit2time = {}

for log in log_file:
    if log_file.line_num == 1:
        continue
    commit2time[log[0][:-1]] = log[2]

for record in commits_file:
    print(record)
    item = record[:]
    item.append('')
    if len(record) >= 2 and len(record[1]) != 0:
        item.append(commit2time[item[1]])
    else:
        item.append('')
    if len(record) >= 3 and len(record[2]) != 0:
        item.append(commit2time[item[2]])
    else:
        item.append('')
    new_file.writerow(item)
