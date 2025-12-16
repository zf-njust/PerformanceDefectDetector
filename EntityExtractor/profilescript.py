# import csv
#
# def dump_invocation_all_result(project):
#     out_path = 'method_invocation_all.csv'
#     out_result = csv.writer(open(out_path, 'wb+'))
#     # out_result.writerow(['class path', 'method name', 'method arguments', 'execution counts',
#     #                      'calls: ',
#     #                      'class path', 'method name',
#     #                      'at: ',
#     #                      'lines','invocation counts'])
#     out_result.writerow(['method', 'method', 'invocation counts'])
#
#     project_info_record = [] #(c_name, c_package, method names)
#     project_info = csv.reader(open('project_info.csv'))
#     for row in project_info:
#         if project_info.line_num == 1:
#             continue
#         project_info_record.append((row[0], row[2], row[3].split(','))) #row[1]:'fontbox\src\main\java\org\apache\fontbox\ttf\TTFTable.java'
#
#     if tests_source == 'D':
#         youkit_dir = '%s\\%s\\Yourkit-Snapshot-Part1\\' % (parameter.SUBJECT_ROOT, project)
#     elif tests_source == 'E':
#         youkit_dir = '%s\\%s\\Yourkit-Snapshot-Evosuite\\' % (parameter.SUBJECT_ROOT, project)
#     elif tests_source == 'D+E':
#         youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
#     else:
#         print 'error!'
#         return
#
#     callee_record = []  #[m1, m2, Invocation Count]
#
#     # search yourkit file from folder
#     for root, dirs, files in os.walk(youkit_dir):
#         for filename in files:
#             if filename.find('-Call-tree')!= -1:
#                 profile_file = csv.reader(open(os.path.join(root, filename)))
#                 print('processing: %s ' %(filename))
#                 # precess
#                 method_stack = [['start', 0, False], ]  # level:(method,invocation counts, whether valid)
#                 for record in profile_file:
#                     if profile_file.line_num==1:
#                         continue
#                     # update: delete the elements after it and record the invocation
#                     level = int(record[-1].strip().strip("\""))
#                     count = int(record[-2]) if len(record[-2])!=0 else 0
#                     method_info = record[0][record[0].find(' ')+1:] if record[0].find('.java')!=-1 else record[0]
#                     valid = True
#                     if not method_info.endswith(')'):
#                         valid = False
#
#                     if len(method_stack)>level:
#                         del method_stack[level:]
#                     method_stack.append([method_info, count, valid])
#
#                     # record call.  the parent element is the last one
#                     if method_stack[level-1][-1] and valid:
#                         for i in range(len(callee_record)):
#                             record = callee_record[i]
#                             if record[0]==method_stack[level-1][0] and record[1]==method_info:
#                                 callee_record[i][2] += count
#                                 break
#                         else:
#                             callee_record.append([method_stack[level-1][0],method_info, count])
#
#     out_result.writerows(callee_record)
#
#
# def combine_two_invocation_results(file1, file2, outputfile):
#     record1 = csv.reader(open(file1))
#     record2 = csv.reader(open(file2))
#     out_result = csv.writer(open(outputfile, 'wb+'))
#     out_result.writerow(['method', 'method', 'invocation counts'])
#     result_set = []
#     for item in record1:
#         if record1.line_num==1:
#             continue
#         method1 = item[0]
#         method2 = item[1]
#         count = int(item[2])
#         result_set.append([method1, method2, count])
#     for item in record2:
#         if record2.line_num==1:
#             continue
#         method1 = item[0]
#         method2 = item[1]
#         count = int(item[2])
#         for i in range(len(result_set)):
#             exist = result_set[i]
#             if item[0]==exist[0] and item[1]==exist[1]:
#                 result_set[i][2] += count
#                 break
#         else:
#             result_set.append([method1, method2, count])
#     out_result.writerows(result_set)
#
#
# if __name__ == '__main__':
