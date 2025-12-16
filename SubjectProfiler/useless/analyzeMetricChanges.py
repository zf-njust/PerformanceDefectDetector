import csv

import parameter


def collect_all_version_data(project):
    metric_record_dict = {}
    for version in parameter.VERSIONS[project]:
        version_record_file = csv.reader(open('%s//%s//metrics_valid.csv' % (parameter.SUBJECT_ROOT, version)))
        metric_records = []
        for record in version_record_file:
            if version_record_file.line_num == 1:
                continue
            metric_records.append(record)
        metric_record_dict[version] = metric_records
    return metric_record_dict


def find_metric_in_record(metric_records, path, method, argument):
    for record in metric_records:
        if record[0]==path and record[1]==method and record[2]==argument:
            return record[:]
    return None


def report_performance_changes(project):
    out_record = csv.writer(open('%s_metric_changes.csv' % project, 'w', encoding='utf8', newline=''))
    out_record.writerow(['class path', 'method name', 'method arguments', 'version1', 'version2',
                        'LOC1', 'Cyclomatic1',
                        'Time1', 'OwnTime1', 'Count1',
                        'Layer1', 'Callees1', 'CalleeInvocations1', 'Callers1', 'CallerInvocations1',
                        'LOC2', 'Cyclomatic2',
                        'Time2', 'OwnTime2', 'Count2',
                        'Layer2', 'Callees2', 'CalleeInvocations2', 'Callers2', 'CallerInvocations2',
                        'delta AvgTime', 'delta AvgOwnTime'
                        ])
    metric_record_dict = collect_all_version_data(project)
    for version_id in range(len(parameter.VERSIONS[project])-1):
        version1 = parameter.VERSIONS[project][version_id]
        version2 = parameter.VERSIONS[project][version_id + 1]
        metric_records1 = metric_record_dict[version1]
        metric_records2 = metric_record_dict[version2]
        increse_time_count = 0
        decrease_time_count = 0
        increse_owntime_count = 0
        decrease_owntime_count = 0
        for record in metric_records1:
            metric2 = find_metric_in_record(metric_records2, record[0], record[1], record[2])
            if metric2 != None:
                increse_time = float(metric2[5])/float(metric2[7])-float(record[5])/float(record[7])
                if increse_time>0:
                    increse_time_count += 1
                elif increse_time<0:
                    decrease_time_count += 1
                increse_owntime = float(metric2[6])/float(metric2[7])-float(record[6])/float(record[7])
                if increse_owntime>0:
                    increse_owntime_count += 1
                elif increse_owntime<0:
                    decrease_owntime_count += 1
                out_record.writerow([record[0], record[1], record[2], version1, version2]+record[3:13]+metric2[3:]+
                                    [increse_time, increse_owntime])
        print(version1, version2, increse_time_count, decrease_time_count, increse_owntime_count, decrease_owntime_count)





if __name__ == '__main__':
    report_performance_changes('pdfbox')