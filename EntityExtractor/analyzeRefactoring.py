import csv
import sys
sys.path.append('..')
sys.path.append('../SubjectProfiler')
import parameter
import datetime
import processIssues


def dumpAllRefactoredMethods(project):
    issues_file = csv.reader(open(parameter.KEYWORDS_ISSUE_PATH[project]))
    changed_method_file = csv.reader(open(parameter.DATA_ROOT+'\\%s\change_method_log.csv' % project))
    out_file = csv.writer(open(parameter.DATA_ROOT+'\\%s\\all_refactored_methods.csv' % project, 'wb+'))
    out_file.writerow(['file', 'method', 'issue', 'hash', 'date', 'title'])

    refactoring_issues = []
    myid = 1
    for record in issues_file:
        if issues_file.line_num == 1:
            continue
        if len(record[1])>0:
            refactoring_issues.append(record[1])
    for record in changed_method_file:
        if changed_method_file.line_num == 1:
            continue
        isfound = False
        for issue in refactoring_issues:
            # if issue=='AVRO-1282' and record[3].startswith(issue):
            #     print record
            if (record[3].lower().find(issue.lower()+':')!=-1 or record[3].lower().find(issue.lower()+' ')!=-1 or \
            record[3].lower().find(issue.lower() + '.') != -1 or record[3].lower().endswith(issue.lower()) or \
            record[3].lower().find(issue.lower() + ',') != -1 or record[3].lower().find(issue.lower() + ']') != -1 or \
                            record[3].lower().find(issue.lower() + ')') != -1) and len(record[5])>0:
                isfound = True
                method_changes = record[5].split('; ')
                for change in method_changes:
                    method = change.split('->')[0]
                    if method == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                    method.find('Test') != -1 or method.find('test') != -1:
                        continue
                    out_file.writerow([record[4], method, issue, record[0], record[2], record[3]])
                break
            # elif record[3].lower().find(issue.lower())!=-1 and len(record[5])>0:
            #     print issue, record[3]
        if not isfound and len(record[5])>0:
            for kw in processIssues.include_keywords:
                if record[3].lower().find(kw) != -1:
                    print record[3]
                    method_changes = record[5].split('; ')
                    issue = 'MyIssue-'+str(myid)
                    myid += 1
                    for change in method_changes:
                        method = change.split('->')[0]
                        if method == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                        method.find('Test') != -1 or method.find('test') != -1:
                            continue
                        out_file.writerow([record[4], method, issue, record[0], record[2], record[3]])
                    break




def getRefactoredMethods(project, version1, version2):
    print project, version1, version2
    class_record1 = csv.reader(open('%s\%s\project_info.csv' % (parameter.SUBJECT_ROOT, version1)))
    VersionDate1 = datetime.datetime.strptime(parameter.VERSION_DATE[version1], "%Y-%m-%d %H:%M:%S")
    Path2Class1 = {}
    for record in class_record1:
        if class_record1.line_num == 1:
            continue
        Path2Class1[record[1]] = record[2] + '.' + record[0]  # x/z/a.java -> XX.XX.a
    class_record2 = csv.reader(open('%s\%s\project_info.csv' % (parameter.SUBJECT_ROOT, version2)))
    VersionDate2 = datetime.datetime.strptime(parameter.VERSION_DATE[version2], "%Y-%m-%d %H:%M:%S")
    Path2Class2 = {}
    for record in class_record2:
        if class_record2.line_num == 1:
            continue
        Path2Class2[record[1]] = record[2] + '.' + record[0]  # x/z/a.java -> XX.XX.a
    # print Path2Class2
    issues_file = csv.reader(open(parameter.KEYWORDS_ISSUE_PATH[project]))
    changed_method_file = csv.reader(open(parameter.DATA_ROOT+'\\%s\change_method_log.csv' % project))
    all_refactoring_issues = []
    refactoring_issues = []
    myid = 1
    simple_refactoring_methods = []  # (m1, m2)
    full_refactoring_methods = []  # (m1(), m2())
    for record in issues_file:
        if issues_file.line_num == 1:
            continue
        if len(record[1])>0:
            all_refactoring_issues.append(record[1])
    for record in changed_method_file:
        if changed_method_file.line_num == 1:
            continue
        time = datetime.datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S")
        if time<=VersionDate1 or time>VersionDate2:
            continue
        isfound = False
        for issue in all_refactoring_issues:
            if (record[3].lower().find(issue.lower()+':')!=-1 or record[3].lower().find(issue.lower()+' ')!=-1 or \
            record[3].lower().find(issue.lower() + '.') != -1 or record[3].lower().endswith(issue.lower()) or \
            record[3].lower().find(issue.lower() + ',') != -1 or record[3].lower().find(issue.lower() + ']') != -1 or \
                            record[3].lower().find(issue.lower() + ')') != -1) and len(record[5])>0:
                isfound = True
                method_changes = record[5].split('; ')
                for change in method_changes:
                    method1 = change.split('->')[0]
                    if method1 == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                    method1.find('Test') != -1 or method1.find('test') != -1:
                        continue
                    path1 = record[4].replace('/', '\\')
                    if path1 not in Path2Class1.keys():
                        continue
                    full_method1 = Path2Class1[path1] + '.' + method1  # XX.XX.a.ff(x,x)
                    simple_method1 = full_method1[: -len(method1.split('(')[-1]) - 1]
                    method2 = change.split('->')[1]
                    if method2 == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                    method2.find('Test') != -1 or method2.find('test') != -1:
                        continue
                    path2 = record[4].replace('/', '\\')
                    if version1=='avro-1.3.0' and version2=='avro-1.8.1':
                        path2=path2.replace('lang\java\src\java\org\\apache\\avro', 'lang\java\\avro\src\main\java\org\\apache\\avro')


                    if path2 not in Path2Class2.keys():
                        # print path2
                        continue
                    full_method2 = Path2Class2[path2] + '.' + method2  # XX.XX.a.ff(x,x)
                    simple_method2 = full_method2[: -len(method2.split('(')[-1]) - 1]
                    simple_refactoring_methods.append((simple_method1, simple_method2))
                    full_refactoring_methods.append((full_method1, full_method2))
                    if issue not in refactoring_issues:
                        refactoring_issues.append(issue)
                    #     print 'issue:', issue
                    # print simple_method1, simple_method2
                break
        if not isfound and len(record[5])>0:
            for kw in processIssues.include_keywords:
                if record[3].lower().find(kw) != -1:
                    # print record[3]
                    method_changes = record[5].split('; ')
                    issue = 'MyIssue-'+str(myid)
                    myid += 1
                    for change in method_changes:
                        method1 = change.split('->')[0]
                        if method1 == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                        method1.find('Test') != -1 or method1.find('test') != -1:
                            continue
                        path1 = record[4].replace('/', '\\')
                        if path1 not in Path2Class1.keys():
                            continue
                        full_method1 = Path2Class1[path1] + '.' + method1  # XX.XX.a.ff(x,x)
                        simple_method1 = full_method1[: -len(method1.split('(')[-1]) - 1]
                        method2 = change.split('->')[1]
                        if method2 == '[None]' or record[4].find('Test') != -1 or record[4].find('test') != -1 or \
                                        method2.find('Test') != -1 or method2.find('test') != -1:
                            continue
                        path2 = record[4].replace('/', '\\')
                        if path2 not in Path2Class2.keys():
                            continue
                        full_method2 = Path2Class2[path2] + '.' + method2  # XX.XX.a.ff(x,x)
                        simple_method2 = full_method2[: -len(method2.split('(')[-1]) - 1]
                        simple_refactoring_methods.append((simple_method1, simple_method2))
                        full_refactoring_methods.append((full_method1, full_method2))
                        if issue not in refactoring_issues:
                            refactoring_issues.append(issue)
                    break
    print 'Number of performance issues:', len(refactoring_issues)
    print refactoring_issues
    return full_refactoring_methods


if __name__ == '__main__':
    dumpAllRefactoredMethods('cxf')
    # dumpAllRefactoredMethods('ivy')
    # dumpAllRefactoredMethods('avro')