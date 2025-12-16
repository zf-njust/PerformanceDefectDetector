import csv
import os
import os.path
import sys
sys.path.append('..')
import parameter


def dump_time_result(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        out_path = '%s\\%s\\method_time_dev.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        out_path = '%s\\%s\\method_time_evo.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        out_path = '%s\\%s\\method_time_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    out_result = csv.writer(open(out_path, 'wb+'))
    out_result.writerow(['class path', 'method name', 'method arguments', 'Time', 'OwnTime', 'count'])

    project_info_record = [] #(class path, package, method name)
    project_info = csv.reader(open('%s\\%s\\project_info.csv' %(parameter.SUBJECT_ROOT, project)))
    for row in project_info:
        if project_info.line_num == 1:
            continue
        project_info_record.append((row[1], row[2], row[3].split(','))) #'fontbox\src\main\java\org\apache\fontbox\ttf\TTFTable.java'

    if tests_source == 'D':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot-Evosuite\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return
    out_record = {} # m_path: c_path, m_name, m_arguments, 'Time', 'OwnTime', 'count'

    # search yourkit file from folder
    for root, dirs, files in os.walk(youkit_dir):
        for filename in files:
            if filename.find('-Method-list--CPU.csv')!= -1:
                profile_file = csv.reader(open(os.path.join(root, filename)))
                # dir_record = open(root+'\dir.txt').readlines()
                # src_dir = dir_record[0].strip()
                # test_dir = dir_record[1].strip()
                print('processing: %s ' %(filename))
                # precess
                for record in profile_file:  # method, Time(ms), Avg. Time(ms), Own Time(ms), Count
                    if profile_file.line_num == 1:
                        continue
                    # record format: org.apache.pdfbox.pdfparser.PDFParser.<init>(InputStream, RandomAccess, boolean) PDFParser.java
                    m_arguments = record[0].split('(')[1].split(')')[0] # InputStream, RandomAccess, boolean
                    m_name = record[0].split('(')[0].split('.')[-1] # <init>
                    c_package = record[0].split('(')[0][:-len(m_name)-1] # org.apache.pdfbox.pdfparser.PDFParser
                    c_path = c_package.replace('.', '\\') + '.java' # org\apache\pdfbox\pdfparser\PDFParser.java
                    c_name = c_package.split('.')[-1]
                    c_package = c_package[:-(len(c_name)+1)]
                    # check whether method location is correctly handled (in project_info)
                    for method_record in project_info_record:
                        if method_record[0].find(c_path)!=-1 and c_package==method_record[1] and \
                                (m_name in method_record[2] or m_name=='<init>'): # valid
                            m_path = method_record[0] + '[%s(%s)]' % (m_name, m_arguments)
                            if m_path in out_record.keys(): # already exsit
                                out_item = out_record[m_path]
                                if method_record[0]!=out_item[0] or m_name!=out_item[1] or m_arguments!=out_item[2]:
                                    print('error!!!!', record[0], out_item)
                                    continue
                                out_item[3] += int(record[1])
                                out_item[4] += int(record[3])
                                out_item[5] += int(record[4])
                            else: # new method record
                                out_record[m_path] = [method_record[0], m_name, m_arguments, int(record[1]), int(record[3]), int(record[4])]
                            break
                    else:
                        if m_name.find('<')==-1 and m_name.find('$')==-1:
                            for method_record in project_info_record:
                                if c_package == method_record[1] and \
                                   method_record[0].find(c_path) != -1 and method_record[0].find('target')==-1:
                                    print('invalid[known package] ', record[0], c_package, method_record)
                                    # break
                            # else:
                            #     print('invalid[unknown package] ', record[0])
    out_result.writerows(out_record.values())


def dump_time_all_result(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        out_path = '%s\\%s\\method_time_all_dev.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        out_path = '%s\\%s\\method_time_all_evo.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        out_path = '%s\\%s\\method_time_all_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    out_result = csv.writer(open(out_path, 'wb+'))
    out_result.writerow(['method', 'Time', 'OwnTime', 'count'])

    if tests_source == 'D':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot-Evosuite\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return
    out_record = {}

    # search yourkit file from folder
    for root, dirs, files in os.walk(youkit_dir):
        for filename in files:
            if filename.find('-Method-list--CPU.csv')!= -1:
                profile_file = csv.reader(open(os.path.join(root, filename)))
                print('processing: %s ' %(filename))
                # precess
                # record format: org.apache.pdfbox.pdfparser.PDFParser.<init>(InputStream, RandomAccess, boolean) PDFParser.java
                for record in profile_file:  # method, Time(ms), Avg. Time(ms), Own Time(ms), Count
                    if profile_file.line_num == 1:
                        continue
                    method = record[0][: -len(record[0].split(' ')[-1])-1]
                    if len(method)==0:
                        continue
                    if method in out_record.keys():
                        out_record[method] = [out_record[method][0]+int(record[1]),
                                                 out_record[method][1]+int(record[3]),
                                                 out_record[method][2]+int(record[4])]
                    else:
                        out_record[method] = [int(record[1]), int(record[3]), int(record[4])]
    for key in out_record.keys():
        out_result.writerow([key, out_record[key][0], out_record[key][1], out_record[key][2]])


def dump_invocation_result(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        out_path = '%s\\%s\\method_invocation_dev.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        out_path = '%s\\%s\\method_invocation_evo.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        out_path = '%s\\%s\\method_invocation_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    out_result = csv.writer(open(out_path, 'wb+'))
    out_result.writerow(['method', 'method', 'invocation counts'])

    project_info_record = [] #(c_name, c_package, method names)
    project_info = csv.reader(open('%s\\%s\\project_info.csv' % (parameter.SUBJECT_ROOT, project)))
    for row in project_info:
        if project_info.line_num == 1:
            continue
        project_info_record.append((row[0], row[2], row[3].split(','))) #row[1]:'fontbox\src\main\java\org\apache\fontbox\ttf\TTFTable.java'

    if tests_source == 'D':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot-Evosuite\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    callee_record = []  #[m1, m2, Invocation Count]

    # search yourkit file from folder
    for root, dirs, files in os.walk(youkit_dir):
        for filename in files:
            if filename.find('-Call-tree')!= -1:
                profile_file = csv.reader(open(os.path.join(root, filename)))
                print('processing: %s ' %(filename))
                # precess
                method_stack = [['start', 0, False], ]  # level:(method,invocation counts, whether valid)
                for record in profile_file:
                    if profile_file.line_num==1:
                        continue
                    # update: delete the elements after it and record the invocation
                    level = int(record[-1].strip().strip("\""))
                    count = int(record[-2]) if len(record[-2])!=0 else 0
                    method_info = record[0][record[0].find(' ')+1:] if record[0].find('.java')!=-1 else record[0]
                    valid = False
                    if not method_info.endswith(')'):
                        valid = False
                    else:
                        m_name = method_info.split('(')[0].split('.')[-1]
                        c_package = method_info.split('(')[0][:-len(m_name)-1]  # org.apache.pdfbox.pdfparser.PDFParser
                        c_name = c_package.split('.')[-1]
                        c_package = c_package[:-(len(c_name) + 1)]
                        for method_record in project_info_record:  # (c_name, c_package, method names)
                            if c_name == method_record[0] and c_package == method_record[1] and \
                                    (m_name in method_record[2] or m_name=='<init>'):  # valid
                                valid = True
                                break
                        else:
                            # print('unknown method:', method_info)
                            valid = False

                    # update stack
                    if len(method_stack)>level:
                        del method_stack[level:]
                    method_stack.append([method_info, count, valid])

                    # record call.  the parent element is the last one
                    if method_stack[level-1][-1] and valid:
                        for i in range(len(callee_record)):
                            record = callee_record[i]
                            if record[0]==method_stack[level-1][0] and record[1]==method_info:
                                callee_record[i][2] += count
                                break
                        else:
                            callee_record.append([method_stack[level-1][0],method_info, count])

    out_result.writerows(callee_record)


def dump_invocation_all_result(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        out_path = '%s\\%s\\method_invocation_all_dev_part4.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        out_path = '%s\\%s\\method_invocation_all_evo.csv' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        out_path = '%s\\%s\\method_invocation_all_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    out_result = csv.writer(open(out_path, 'wb+'))
    # out_result.writerow(['class path', 'method name', 'method arguments', 'execution counts',
    #                      'calls: ',
    #                      'class path', 'method name',
    #                      'at: ',
    #                      'lines','invocation counts'])
    out_result.writerow(['method', 'method', 'invocation counts'])

    project_info_record = [] #(c_name, c_package, method names)
    project_info = csv.reader(open('%s\\%s\\project_info.csv' % (parameter.SUBJECT_ROOT, project)))
    for row in project_info:
        if project_info.line_num == 1:
            continue
        project_info_record.append((row[0], row[2], row[3].split(','))) #row[1]:'fontbox\src\main\java\org\apache\fontbox\ttf\TTFTable.java'

    if tests_source == 'D':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot-Part4\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        youkit_dir = '%s\\%s\\Yourkit-Snapshot-Evosuite\\' % (parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return

    callee_record = []  #[m1, m2, Invocation Count]

    # search yourkit file from folder
    for root, dirs, files in os.walk(youkit_dir):
        for filename in files:
            if filename.find('-Call-tree')!= -1:
                profile_file = csv.reader(open(os.path.join(root, filename)))
                print('processing: %s ' %(filename))
                # precess
                method_stack = [['start', 0, False], ]  # level:(method,invocation counts, whether valid)
                for record in profile_file:
                    if profile_file.line_num==1:
                        continue
                    # update: delete the elements after it and record the invocation
                    level = int(record[-1].strip().strip("\""))
                    count = int(record[-2]) if len(record[-2])!=0 else 0
                    method_info = record[0][record[0].find(' ')+1:] if record[0].find('.java')!=-1 else record[0]
                    valid = True
                    if not method_info.endswith(')'):
                        valid = False

                    if len(method_stack)>level:
                        del method_stack[level:]
                    method_stack.append([method_info, count, valid])

                    # record call.  the parent element is the last one
                    if method_stack[level-1][-1] and valid:
                        for i in range(len(callee_record)):
                            record = callee_record[i]
                            if record[0]==method_stack[level-1][0] and record[1]==method_info:
                                callee_record[i][2] += count
                                break
                        else:
                            callee_record.append([method_stack[level-1][0],method_info, count])

    out_result.writerows(callee_record)


def combine_invocation_results(project):
    record1 = csv.reader(open('%s\\%s\\method_invocation_dev.csv' % (parameter.SUBJECT_ROOT, project)))
    record2 = csv.reader(open('%s\\%s\\method_invocation_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    out_result = csv.writer(open('%s\\%s\\method_invocation_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    out_result.writerow(['method', 'method', 'invocation counts'])
    result_set = []
    for item in record1:
        if record1.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        result_set.append([method1, method2, count])
    for item in record2:
        if record2.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        for i in range(len(result_set)):
            exist = result_set[i]
            if item[0]==exist[0] and item[1]==exist[1]:
                result_set[i][2] += count
                break
        else:
            result_set.append([method1, method2, count])
    out_result.writerows(result_set)


def combine_invocation_all_results(project):
    record1 = csv.reader(open('%s\\%s\\method_invocation_all_dev.csv' % (parameter.SUBJECT_ROOT, project)))
    record2 = csv.reader(open('%s\\%s\\method_invocation_all_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    out_result = csv.writer(open('%s\\%s\\method_invocation_all_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    out_result.writerow(['method', 'method', 'invocation counts'])
    result_set = []
    for item in record1:
        if record1.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        result_set.append([method1, method2, count])
    for item in record2:
        if record2.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        for i in range(len(result_set)):
            exist = result_set[i]
            if item[0]==exist[0] and item[1]==exist[1]:
                result_set[i][2] += count
                break
        else:
            result_set.append([method1, method2, count])
    out_result.writerows(result_set)


def combine_two_invocation_results(file1, file2, outputfile):
    record1 = csv.reader(open(file1))
    record2 = csv.reader(open(file2))
    out_result = csv.writer(open(outputfile, 'wb+'))
    out_result.writerow(['method', 'method', 'invocation counts'])
    result_set = []
    for item in record1:
        if record1.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        result_set.append([method1, method2, count])
    for item in record2:
        if record2.line_num==1:
            continue
        method1 = item[0]
        method2 = item[1]
        count = int(item[2])
        for i in range(len(result_set)):
            exist = result_set[i]
            if item[0]==exist[0] and item[1]==exist[1]:
                result_set[i][2] += count
                break
        else:
            result_set.append([method1, method2, count])
    out_result.writerows(result_set)

def dump_performance(project):
    # tests by developers
    dump_time_all_result(project)
    # dump_time_result(project)
    # dump_invocation_result(project)
    # dump_invocation_all_result(project)
    #
    # # # tests by evosuite
    # dump_time_all_result(project, 'E')
    # dump_time_result(project, 'E')
    # dump_invocation_result(project, 'E')
    # dump_invocation_all_result(project, 'E')
    #
    # dump_time_all_result(project, 'D+E')
    # dump_time_result(project, 'D+E')
    # combine_invocation_results(project)
    # combine_invocation_all_results(project)


if __name__ == '__main__':
    # combine_two_invocation_results(
    #     'C:\Users\chenzhifei\Desktop\subjects\cxf-3.0.1\method_invocation_all_dev_part12.csv',
    #     'C:\Users\chenzhifei\Desktop\subjects\cxf-3.0.1\method_invocation_all_dev_part34.csv',
    #     'C:\Users\chenzhifei\Desktop\subjects\cxf-3.0.1\method_invocation_all_dev_part1234.csv',)

    # dump_performance('cxf-3.1.11-2017.4')
    dump_performance('cxf-3.0.1')

    # dump_performance('avro-1.8.1')
    # dump_performance('avro-1.6.0')
    # dump_performance('avro-1.3.0')
    #
    # dump_performance('ivy-2.0.0-2009.1')
    # dump_performance('ivy-2.1.0-2009.10')
    # dump_performance('ivy-2.2.0-2010.9')
    # dump_performance('ivy-2.3.0-2013.1')
    # dump_performance('ivy-2.4.0-2014.12')
    #
    #

    # dump_performance('pdfbox-1.8.4-2014.1')
    # dump_performance('pdfbox-1.8.6-2014.6')
    # dump_performance('pdfbox-1.8.8-2014.12')
    # dump_performance('pdfbox-1.8.10-2015.7')
    # dump_performance('pdfbox-1.8.11-2016.1')
    # dump_performance('pdfbox-2.0.0')
    # dump_performance('pdfbox-2.0.2-2016.6')
    # dump_performance('pdfbox-2.0.4-2016.12')





    # dump_time_result('avro', parameter.SUBJECT_DIR)
    # dump_invocation_result('avro', parameter.SUBJECT_DIR)

    # dump_time_result('pdfbox-1.8.4-2014.1')
    # dump_invocation_result('pdfbox-1.8.4-2014.1')
    # dump_invocation_all_result('pdfbox-1.8.4-2014.1')

    # dump_time_result('pdfbox-1.8.6-2014.6')
    # dump_invocation_result('pdfbox-1.8.6-2014.6')
    # dump_invocation_all_result('pdfbox-1.8.6-2014.6')
    #
    # dump_time_result('pdfbox-1.8.8-2014.12')
    # dump_invocation_result('pdfbox-1.8.8-2014.12')
    # dump_invocation_all_result('pdfbox-1.8.8-2014.12')
    #
    # dump_time_result('pdfbox-1.8.10-2015.7')
    # dump_invocation_result('pdfbox-1.8.10-2015.7')
    # dump_invocation_all_result('pdfbox-1.8.10-2015.7')
    #
    # dump_time_result('pdfbox-1.8.11-2016.1')
    # dump_invocation_result('pdfbox-1.8.11-2016.1')
    # dump_invocation_all_result('pdfbox-1.8.11-2016.1')
    #
    # dump_time_result('pdfbox-2.0.2-2016.6')
    # dump_invocation_result('pdfbox-2.0.2-2016.6')
    # dump_invocation_all_result('pdfbox-2.0.2-2016.6')
    #
    # dump_time_result('pdfbox-2.0.4-2016.12')
    # dump_invocation_result('pdfbox-2.0.4-2016.12')
    # dump_invocation_all_result('pdfbox-2.0.4-2016.12')


