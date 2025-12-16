import csv
import os
import sys
sys.path.append('..')
import parameter
csv.field_size_limit(500 * 1024 * 1024)

# not include the commits with the changes of more than 100 files.


def getMethodChanges(project):
    commit_log_record = csv.reader(open(parameter.DATA_ROOT+'\\%s\change_log.csv' %project))
    changed_method_log = csv.writer(open(parameter.DATA_ROOT+'\\%s\change_method_log.csv' % project, 'wb+'))
    changed_method_log.writerow(['hash','author','date','title','file','methods'])

    commit_log = [] # (commit, author, time, message, files, number of files)
    for record in commit_log_record:
        if commit_log_record.line_num==1 or len(record)==0:
            continue
        commit_log.append(record[:])

    for i in range(len(commit_log)):
        change_log = commit_log[i]
        current_commit = change_log[0]
        # filter too early unstable commits:
        if (project=='pdfbox' and current_commit=='24572c4ab') or \
            (project=='avro' and current_commit=='2b43cbdc'):
            break
        # no java file change
        if len(change_log)<5 or len(change_log[4])==0:
            continue
        if int(change_log[5])>50:
            continue
        # processing for each commit.........
        origin_commit = commit_log[i+1][0]
        # for test/debug
        # if current_commit != '4be4d1d79':
        #     continue
        changed_files = change_log[4].replace('[','').replace(']','').replace(' ','').replace('\'','').split(',')
        for changed_file in changed_files:
            # print "now %s" % os.getcwd()
            changed_methods = []
            os.chdir(parameter.GIT_ROOT[project])
            origin_file_exist = os.system('git show ' + origin_commit + ":" + changed_file + ' > ' + parameter.ORIGIN_FILE)
            if origin_file_exist == 0:
                current_file_exist = os.system('git show ' + current_commit + ":" + changed_file + ' > ' + parameter.CURRENT_FILE)
                if current_file_exist == 0:
                    print current_commit, origin_commit, changed_file
                    os.chdir(parameter.CHANGE_JAR_ROOT)
                    output = os.popen('java -jar changedistiller.jar -f %s %s' % (
                    parameter.ORIGIN_FILE, parameter.CURRENT_FILE))
                    info = output.readlines()
                    for line in info:
                        line = line.strip('\r\n')
                        changed_methods.append(line)
            # print '; '.join(changed_methods)
            changed_method_log.writerow([change_log[0], change_log[1], change_log[2], change_log[3],
                                        changed_file, '; '.join(changed_methods)])


if __name__ == '__main__':
    # getMethodChanges('pdfbox')
    # getMethodChanges('avro')
    # getMethodChanges('ivy')
    getMethodChanges('cxf')
