#git log --no-walk --tags --pretty="%h;%d;%an;%ai;%s" --decorate=full > ../tags_info
#git log --name-only --pretty="==================%n%h;%an;%ai;%s%n%b%n==" > ../log_info

import csv

import parameter


def dump_change_log(project):
    with open(parameter.LOG_ROOT[project]+ 'log_info') as f:
        fp = open('%s_change_log.csv' %project, 'wb+')
        logcsv = csv.writer(fp)
        logcsv.writerow(['hash','author','date','title','file'])
        logflag = True
        fileflag = False
        logitem = []
        files = []
        for line in f:
            line = line.strip()
            if line == '==================':
                if len(logitem) == 0:
                    continue
                if len(files) > 0:
                    logcsv.writerow(logitem+[files,len(files)])
                else:
                    logcsv.writerow(logitem)
                logflag = True
                fileflag = False
                logitem = []
                files = []
            elif logflag and not fileflag:
                commit = line.split(";")
                logitem.append(commit[0])
                logitem.append(commit[1])
                logitem.append(commit[2][0:-6])
                logitem.append(line[(len(commit[0])+len(commit[1])+len(commit[2])+3):])
                logflag = False
                fileflag = False
            elif line == '==':
                fileflag = True
            elif fileflag and len(line) != 0 and line.endswith('.java'):
                files.append(line)


def get_fix_info(project):
    new_issue_record = csv.writer(open('%s_issues_info2.csv' % project, 'wb+'))
    new_issue_record.writerow(['bugID','target methods','fixed release',
                               'fix commit','author','date','title','files'])
    old_issue_record = csv.reader(open('%s_issues_info.csv' % project))
    change_log_record = csv.reader(open('%s_change_log.csv' % project))
    change_log = []
    for log in change_log_record:
        if change_log_record.line_num == 1:
            continue
        change_log.append(log)
    for record in old_issue_record:
        if old_issue_record.line_num == 1:
            continue
        if len(record[0])==0:
            continue
        newrow = record[:3]
        for log in change_log:
            if log[3].find(record[0].strip())!=-1:
                if len(log)<=4 or len(log[4])==0:
                    continue
                files = log[4].replace('[','').replace(']','').replace(' ','').replace('\'','').split(',')
                log_copy = log[0:4]
                for file in files:
                    new_issue_record.writerow(newrow+log_copy+[file])
                    log_copy = ['','','','']
                    newrow = ['','','']


def add_issue_metric(project):
    new_issue_record = csv.writer(open('%s_issues_info4.csv' % project, 'wb+'))
    new_issue_record.writerow(['bugID','target methods','fixed release', 'version1','version2',
                               'fix commit','author','date','title','class path',
                               'method name1', 'method arguments1',
                               'LOC1','Cyclomatic1',
                               'Time1','OwnTime1','Count1',
                               'Layer1','Callees1','CalleeInvocations1','Callers1','CallerInvocations1',
                               'method name2', 'method arguments2',
                               'LOC2', 'Cyclomatic2',
                               'Time2', 'OwnTime2', 'Count2',
                               'Layer2', 'Callees2', 'CalleeInvocations2', 'Callers2', 'CallerInvocations2'
                               ])
    old_issue_record = csv.reader(open('%s_issues_info3.csv' % project))
    for record in old_issue_record:
        if old_issue_record.line_num == 1:
            continue
        if len(record[0])!=0:
            title = record[0:9]
        else:
            title = [record[i] if len(record[i])!=0 else title[i] for i in range(9)]
        # print(record)
        # print(title)
        if title[2]!='2.0.0':
            continue
        filename = record[9].replace('/', '\\')
        modified_methods = record[10].replace(' ','').split(';')
        if len(record[10])==0 or len(modified_methods)==0:
            continue
        version1 = title[3]
        version2 = title[4]
        version_record_file1 = csv.reader(open('%s//%s//metrics_valid.csv' % (parameter.SUBJECT_ROOT, version1)))
        version_record1 = []
        for r in version_record_file1:
            if version_record_file1.line_num==1:
                continue
            version_record1.append(r)
        version_record_file2 = csv.reader(open('%s//%s//metrics_valid.csv' % (parameter.SUBJECT_ROOT, version2)))
        version_record2 = []
        for r in version_record_file2:
            if version_record_file2.line_num == 1:
                continue
            version_record2.append(r)

        for method in modified_methods:
            method_name = method[:method.find('(')]
            method_arguments = method[(method.find('(')+1):-1]
            newrow = title[:] + [filename, method_name, method_arguments]
            for r in version_record1:
                if r[0]==filename and r[1]==method_name and r[2]==method_arguments:
                    newrow.extend(r[3:])
                    break
            else:
                newrow.extend(['']*10)
            for r in version_record2:
                if r[0]==filename and r[1]==method_name and r[2]==method_arguments:
                    newrow.extend(r[3:])
                    break
            else:
                newrow.extend(['']*10)
            new_issue_record.writerow(newrow)

if __name__ == '__main__':
    # first step: generate change_log.csv from git log
    dump_change_log('pdfbox')
    # second step: generate issues_info.csv (bugID,target methods,fix release)from collected issues
    # third step: generate issues_info2.csv (bugID,target methods,fix release, commit info...) to complement issues_info.csv
    # get_fix_info('pdfbox')
    # check uncorrect commits, generate issues_info3.csv
    # generate issues_info4.csv to complement metrics
    # add_issue_metric('pdfbox')