# Layer, Caller Invocations, Callee Invocations, Callers, Callees

import csv
import os
import sys
sys.path.append('..')
import parameter

def analyze_layer(project):
    Method2Layer = {}
    for root, dirs, files in os.walk("%s\\%s\\DRHCluster" %(parameter.SUBJECT_ROOT, project)):
        for name in files:
            if name.startswith('Layer') and name.endswith('.csv'):
                layer_record = csv.reader(open(os.path.join(root, name)))
                for record in layer_record:
                    if layer_record.line_num == 1 or record[0]=='Average' or record[0]=='Standard Deviation':
                        continue
                    Method2Layer[record[0]] = int(name.lstrip('Layer').rstrip('.csv'))
    return Method2Layer


def analyze_invocation(project, mode='A', tests_source='D'):
    Method2Callers = {}
    Method2Callees = {}
    Method2CallerInvocations = {}
    Method2CalleeInvocations = {}
    if mode == 'A':
        if tests_source == 'D':
            call_record = csv.reader(open('%s//%s//method_invocation_all_dev.csv' % (parameter.SUBJECT_ROOT, project)))
        elif tests_source == 'E':
            call_record = csv.reader(open('%s//%s//method_invocation_all_evo.csv' % (parameter.SUBJECT_ROOT, project)))
        elif tests_source == 'D+E':
            call_record = csv.reader(open('%s//%s//method_invocation_all_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
        else:
            print 'error!'
            return
    elif mode == 'S':
        if tests_source == 'D':
            call_record = csv.reader(open('%s//%s//method_invocation_dev.csv' % (parameter.SUBJECT_ROOT, project)))
        elif tests_source == 'E':
            call_record = csv.reader(open('%s//%s//method_invocation_evo.csv' % (parameter.SUBJECT_ROOT, project)))
        elif tests_source == 'D+E':
            call_record = csv.reader(open('%s//%s//method_invocation_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
        else:
            print 'error!'
            return

    for record in call_record:
        if call_record.line_num == 1:
            continue
        method1, method2, count = record[0], record[1], int(record[2])
        if method1 not in Method2Callees.keys(): # called by it
            Method2Callees[method1] = 1
            Method2CalleeInvocations[method1] = count
        else:
            Method2Callees[method1] += 1
            Method2CalleeInvocations[method1] += count
        if method2 not in Method2Callers.keys(): # the method which called it
            Method2Callers[method2] = 1
            Method2CallerInvocations[method2] = count
        else:
            Method2Callers[method2] += 1
            Method2CallerInvocations[method2] += count
    return Method2Callers, Method2Callees, Method2CallerInvocations, Method2CalleeInvocations


def dump_arch_info(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        out_path = '%s//%s//method_arch_dev.csv' %(parameter.SUBJECT_ROOT, project)
    elif tests_source == 'E':
        out_path = '%s//%s//method_arch_evo.csv' %(parameter.SUBJECT_ROOT, project)
    elif tests_source == 'D+E':
        out_path = '%s//%s//method_arch_dev_evo.csv' %(parameter.SUBJECT_ROOT, project)
    else:
        print 'error!'
        return
    out_record = csv.writer(open(out_path, 'wb+'))
    out_record.writerow(['class path','method name','method arguments','Layer','Callees', 'CalleeInvocations','Callers','CallerInvocations'])
    Method2Layer = analyze_layer(project)
    Method2Callers, Method2Callees, Method2CallerInvocations, Method2CalleeInvocations = analyze_invocation(project, 'A', tests_source)
    method2callers, method2callees, method2callerInvocations, method2calleeInvocations = analyze_invocation(project, 'S', tests_source)
    if tests_source == 'D':
        method_record = csv.reader(open('%s//%s//method_time_dev.csv' % (parameter.SUBJECT_ROOT, project)))
    elif tests_source == 'E':
        method_record = csv.reader(open('%s//%s//method_time_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    elif tests_source == 'D+E':
        method_record = csv.reader(open('%s//%s//method_time_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    else:
        print 'error!'
        return
    class_record = csv.reader(open('%s//%s//project_info.csv' % (parameter.SUBJECT_ROOT, project)))
    Path2Package = {}
    for record in class_record:
        if class_record.line_num == 1:
            continue
        Path2Package[record[1]] = record[2]
    for record in method_record:
        if method_record.line_num == 1:
            continue
        path, methodname, arguments = record[0], record[1], record[2]
        if methodname.find('Test')!=-1 or methodname.find('test')!=-1 or \
                        path.find('Test') != -1 or path.find('test') != -1:
            continue
        package = Path2Package[path]
        classname = path.split('\\')[-1][:-5]
        method = '%s.%s.%s(%s)' %(package, classname, methodname, arguments)
        #check valid
        Layer = ''
        Callees, CalleeInvocations, Callers, CallerInvocations = 0,0,0,0
        callees, calleeInvocations, callers, callerInvocations = 0,0,0,0
        layer_count = 0
        for m in Method2Layer.keys():
            if method.find(m) != -1:
                layer_count += 1
                Layer = Method2Layer[m]
        if layer_count > 1:
            print('error layer in method', method, layer_count)
        callee_count = 0
        for m in Method2Callees.keys():
            if method.find(m)!=-1:
                callee_count+=1
                Callees = Method2Callees[m]
                CalleeInvocations = Method2CalleeInvocations[m]
                callees = method2callees[m] if m in method2callees else ''
                calleeInvocations = method2calleeInvocations[m] if m in method2callees else ''
        if callee_count>1:
            print('error callee in method', method, callee_count)
        caller_count = 0
        for m in Method2Callers.keys():
            if method.find(m)!=-1:
                caller_count+=1
                Callers = Method2Callers[m]
                CallerInvocations = Method2CallerInvocations[m]
                callers = method2callers[m] if m in method2callers else ''
                callerInvocations = method2callerInvocations[m] if m in method2callers else ''
        if caller_count>1:
            print('error caller in method', method, caller_count)
        if callee_count==0 and caller_count==0:
            print('error in caller&callee', method)
        out_record.writerow([record[0], record[1], record[2], Layer,
                             Callees, CalleeInvocations, Callers, CallerInvocations,
                             callees, calleeInvocations, callers, callerInvocations])


if __name__ == "__main__":
    # dump_arch_info('avro-1.8.1', 'D')
    # dump_arch_info('avro-1.8.1', 'D+E')

    dump_arch_info('avro-1.6.0', 'D')
    dump_arch_info('avro-1.6.0', 'D+E')

    dump_arch_info('avro-1.3.0', 'D')
    dump_arch_info('avro-1.3.0', 'D+E')

    # dump_arch_info('pdfbox-1.8.4-2014.1')
    # dump_arch_info('pdfbox-1.8.6-2014.6')
    # dump_arch_info('pdfbox-1.8.8-2014.12')
    # dump_arch_info('pdfbox-1.8.10-2015.7', 'D+E')
    # dump_arch_info('pdfbox-1.8.11-2016.1')
    # dump_arch_info('pdfbox-2.0.0', 'D')
    # dump_arch_info('pdfbox-2.0.0', 'D+E')
    # dump_arch_info('pdfbox-2.0.2-2016.6')
    # dump_arch_info('pdfbox-2.0.4-2016.12')