import csv
import sys
sys.path.append('..')
import parameter
import numpy
import time


def isequal_methodname(name0, name1):
    if name0 == name1:
        return True
    classname0 = name0.split('.')[-2]
    classname1 = name1.split('.')[-2]
    if name0.replace('<init>', classname0)==name1.replace('<init>', classname1):
        return True
    else:
        return False


def isequal_parameters(parameters0, parameters1):
    # print(parameters1, parameters2)
    if parameters1 == parameters0:
        return True

    # '<>'
    while parameters1.find('<')!=-1:
        parameters1 = parameters1[0:(parameters1.index('<'))]+parameters1[(parameters1.index('>')+1):]
    while parameters0.find('<')!=-1:
        parameters0 = parameters0[0:(parameters0.index('<'))]+parameters0[(parameters0.index('>')+1):]
    # ...
    parameters1 = parameters1.replace('...', '[]')
    parameters0 = parameters0.replace('...', '[]')
    # print(parameters1,parameters2)
    if parameters1 == parameters0:
        return True

    parameters1_array = parameters1.split(',')
    parameters0_array = parameters0.split(',')
    if len(parameters1_array) != len(parameters0_array):
        return False
    for index in range(len(parameters1_array)):
        p1 = parameters1_array[index]
        p0 = parameters0_array[index]
        if p1.find('$')==-1 and p1.find('.')==-1 and p0.find('$')==-1 and p0.find('.')==-1:
            if p1 == p0:
                continue
            else:
                return False
        p1 = p1.replace('$', '.')
        p0 = p0.replace('$', '.')
        if p1==p0 or p1 in p0.split('.') or p0 in p1.split('.'):
            continue
        else:
            return False
    return True



# HIGH_THRESHOLD = 95
# LOW_THRESHOLD = 10


def getThresholds(dataset):
    # low, high = numpy.percentile(dataset, [10, 95])
    newdataset = numpy.array([i for i in dataset if i>0])
    if len(newdataset)==0:
        lower_bound = 0
        upper_bound = 0
    else:
        quartile_1 = numpy.percentile(newdataset, 25)
        quartile_3 = numpy.percentile(newdataset, 75)
        iqr = quartile_3 - quartile_1
        lower_bound = quartile_1 - (iqr * 3.0)
        upper_bound = quartile_3 + (iqr * 3.0)
    # return int(max(low, lower_bound)), int(max(high, upper_bound))
    return int(lower_bound), int(upper_bound)

    # return max(0, int(numpy.percentile(newdataset, 10))), int(numpy.percentile(newdataset, 90))


def adaptThresholds(dataset, wholedataset):
    if len(dataset)<10:
        return getThresholds(wholedataset)
    else:
        return getThresholds(dataset)

# def isSelfRecursion(method, method2dynamiccallees):
#     call_list = detectCyclicInvoc([], method, method2dynamiccallees)
#     if len(call_list) == 1:
#         return True
#     else:
#         return False


def findCyclicInvoc(methods, circle_methods, method2dynamiccallees, visited_methods):
    for method in methods:
        # print 'visiting: ', method
        if method not in visited_methods.keys():
            print 'not finding:', method
            continue
        if not visited_methods[method]:
            detectCyclicInvoc([], method, circle_methods, method2dynamiccallees, visited_methods)

# yes:len>1, selfRecur:len=1, no:len=0
def detectCyclicInvoc(call_list, method, circle_methods, method2dynamiccallees, visited_methods):
    # print call_list, method
    visited_methods[method] = True
    if len(call_list) == 0:
        method_list = [method]
    else:
        method_list = call_list[:] + [method]
    if method not in method2dynamiccallees.keys():
        return []
    callees = method2dynamiccallees[method]
    for m in callees:
        if m == method_list[0]:
            circle_methods.append(method_list[:])
            # print 'circle: ', method_list[:]
            return method_list
        elif m in method_list:
            circle_methods.append(method_list[method_list.index(m):])
            # print 'circle: ', method_list[method_list.index(m):]
            continue
        if visited_methods[m]:
            continue
        new_list = detectCyclicInvoc(method_list, m, circle_methods, method2dynamiccallees, visited_methods)
        if len(new_list) == 0:
            continue
        else:
            return new_list
    else:
        return []


def getAllMethodList(project):
    valid_methods = []
    metric_record = csv.reader(open('%s//%s//method_all_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    for record in metric_record:
        if metric_record.line_num==1:
            continue
        valid_methods.append(record[0])
    return valid_methods


def getValidMethodList(project):
    valid_methods = []
    metric_record = csv.reader(open('%s//%s//method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    for record in metric_record:
        if metric_record.line_num==1:
            continue
        valid_methods.append(record[0])
    return valid_methods


def readMethodStaticRelations(project):
    Static_Relations = [] #[method1, method2]
    Method2Callers = {}
    Method2Callees = {}
    static_call_record = [line.rstrip() for line in open(parameter.STATIC_CALL_FILE[project]).readlines()]
    number = int(static_call_record[1])
    methods = static_call_record[number+2:]
    valid_methods = getAllMethodList(project)
    unvalid = []
    for index in range(len(methods)):
        m = methods[index]
        if m in valid_methods:
            continue
        name1 = m.split('(')[0]
        parameters1 = m.split('(')[1].split(')')[0].replace(' ', '')
        for valid_method in valid_methods:
            name2 = valid_method.split('(')[0]
            parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
            if isequal_methodname(name1, name2) and isequal_parameters(parameters1, parameters2):
                if m.find('<')==-1 and valid_method.find('<')==-1:
                    print m, valid_method
                methods[index] = valid_method
                break
        else:
            for valid_method in valid_methods:
                name2 = valid_method.split('(')[0]
                parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name1, name2) and len(parameters1)>0 and len(parameters2)>0 and \
                                parameters1.count(',')==parameters2.count(','):
                    print m, valid_method
                    methods[index] = valid_method
                    break
            else:
                # print 'MethodStaticRelations: no finding ', m
                unvalid.append(m)

    for i in range(2, number+2):
        relation = static_call_record[i].rstrip().split(' ')
        if methods[i-2] in unvalid:
            continue
        for index in range(number):
            if methods[index] in unvalid:
                continue
            if int(relation[index])==1:
                # if methods[index]=='org.apache.pdfbox.pdmodel.graphics.xobject.PDXObjectImage.getMask()':
                #     print methods[i-2]
                Static_Relations.append([methods[i-2], methods[index]])
                if methods[index] not in Method2Callers.keys():
                    Method2Callers[methods[index]] = [methods[i-2]]
                else:
                    Method2Callers[methods[index]].append(methods[i - 2])
                if methods[i-2] not in Method2Callees.keys():
                    Method2Callees[methods[i-2]] = [methods[index]]
                else:
                    Method2Callees[methods[i-2]].append(methods[index])
    return Static_Relations, Method2Callers, Method2Callees


def unifyMethodDynamicAllRelations(project):
    invocation_record = csv.reader(
        open('%s//%s//method_invocation_all_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    invocation_new_record = csv.writer(
        open('%s//%s//method_invocation_all_unified_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    valid_methods = getAllMethodList(project)
    for record in invocation_record:
        if invocation_record.line_num == 1:
            invocation_new_record.writerow(record)
            continue
        caller = record[0]
        callee = record[1]
        if caller.count('(')!=1 or caller.count(')')!=1 or callee.count('(')!=1 or callee.count(')')!=1:
            # print project, 'error record:', record
            continue
        if caller not in valid_methods:
            name1 = caller.split('(')[0]
            parameters1 = caller.split('(')[1].split(')')[0].replace(' ', '')
            for valid_method in valid_methods:
                name2 = valid_method.split('(')[0]
                parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name1, name2) and isequal_parameters(parameters1, parameters2):
                    # if caller.find('<') == -1 and valid_method.find('<') == -1:
                    #     print caller, valid_method
                    caller = valid_method
                    break
            else:
                for valid_method in valid_methods:
                    name2 = valid_method.split('(')[0]
                    parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                    if isequal_methodname(name1, name2) and len(parameters1) > 0 and len(parameters2) > 0 and \
                                    parameters1.count(',') == parameters2.count(','):
                    #     print caller, valid_method
                        caller = valid_method
                        break
        if callee not in valid_methods:
            name1 = callee.split('(')[0]
            parameters1 = callee.split('(')[1].split(')')[0].replace(' ', '')
            for valid_method in valid_methods:
                name2 = valid_method.split('(')[0]
                parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name1, name2) and isequal_parameters(parameters1, parameters2):
                    # if callee.find('<') == -1 and valid_method.find('<') == -1:
                    #     print callee, valid_method
                    callee = valid_method
                    break
            else:
                for valid_method in valid_methods:
                    name2 = valid_method.split('(')[0]
                    parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                    if isequal_methodname(name1, name2) and len(parameters1) > 0 and len(parameters2) > 0 and \
                                    parameters1.count(',') == parameters2.count(','):
                        # print callee, valid_method
                        callee = valid_method
                        break
        invocation_new_record.writerow([caller, callee, int(record[2])])




def readMethodDynamicAllRelations(project, Method2Layer):
    Dynamic_All_Relatins = [] #[method1, method2, counts]
    Method2Callers = {}
    Method2Callees = {}
    invocation_record = csv.reader(open('%s//%s//method_invocation_all_unified_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    # valid_methods = getValidMethodList(project)
    Layer2Calls = {}
    for record in invocation_record:
        if invocation_record.line_num == 1:
            continue
        caller = record[0]
        callee = record[1]
        calls = int(record[2])
        Dynamic_All_Relatins.append([caller, callee, calls])
        if callee not in Method2Callers.keys():
            Method2Callers[callee] = [caller]
        else:
            Method2Callers[callee].append(caller)
        if caller not in Method2Callees.keys():
            Method2Callees[caller] = [callee]
        else:
            Method2Callees[caller].append(callee)
        if callee in Method2Layer.keys():  # valid callee
            layer = Method2Layer[callee]
            if layer not in Layer2Calls.keys():
                Layer2Calls[layer] = [calls]
            else:
                Layer2Calls[layer].append(calls)
    low_calls_threshold, high_calls_threshold = {}, {}
    for layer in Layer2Calls.keys():
        # low_calls_threshold[layer], high_calls_threshold[layer] = getThresholds(Layer2Calls[layer])
        low_calls_threshold[layer], high_calls_threshold[layer] = adaptThresholds(Layer2Calls[layer], [i[2] for i in Dynamic_All_Relatins])
    Thresholds = {'HighCalls': high_calls_threshold, 'LowCalls': low_calls_threshold}
    return Dynamic_All_Relatins, Method2Callers, Method2Callees, Thresholds


def readMethodMetrics(project):
    Method2Time = {}
    Method2OwnTime = {}
    Method2Counts = {}
    Method2Layer = {}
    Layer2Time = {}
    Layer2OwnTime = {}
    Layer2Counts = {}
    metric_record = csv.reader(open('%s//%s//method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project)))
    length = 0
    for record in metric_record:
        if metric_record.line_num==1:
            length = len(record)
            continue
        if len(record)!=length:
            print record
        method = record[0]
        layer = int(record[1])
        time = int(record[-3])
        owntime = int(record[-2])
        counts = int(record[-1])
        Method2Time[method] = time
        Method2OwnTime[method] = owntime
        Method2Counts[method] = counts
        Method2Layer[method] = layer
        if layer not in Layer2Time.keys():
            Layer2Time[layer] = [time]
            Layer2OwnTime[layer] = [owntime]
            Layer2Counts[layer] = [counts]
        else:
            Layer2Time[layer].append(time)
            Layer2OwnTime[layer].append(owntime)
            Layer2Counts[layer].append(counts)
    low_time_threshold, high_time_threshold = {}, {}
    low_owntime_threshold, high_owntime_threshold = {}, {}
    low_counts_threshold, high_counts_threshold = {}, {}
    for layer in Layer2Time.keys():
        low_time_threshold[layer], high_time_threshold[layer] = adaptThresholds(Layer2Time[layer], Method2Time.values())
        low_owntime_threshold[layer], high_owntime_threshold[layer] = adaptThresholds(Layer2OwnTime[layer], Method2OwnTime.values())
        low_counts_threshold[layer], high_counts_threshold[layer] = adaptThresholds(Layer2Counts[layer], Method2Counts.values())

        # low_time_threshold[layer], high_time_threshold[layer] = getThresholds(Layer2Time[layer])
        # low_owntime_threshold[layer], high_owntime_threshold[layer] = getThresholds(Layer2OwnTime[layer])
        # low_counts_threshold[layer], high_counts_threshold[layer] = getThresholds(Layer2Counts[layer])
    Thresholds = {'HighTime': high_time_threshold, 'LowTime': low_time_threshold,
                  'HighOwnTime': high_owntime_threshold, 'LowOwnTime': low_owntime_threshold,
                  'HighCounts': high_counts_threshold, 'LowCounts': low_counts_threshold}
    return Method2OwnTime, Method2Time, Method2Counts, Method2Layer, Thresholds


# def getButterflySpace(project, method):
#     pass
#
#
# def getProblematicSpace(project, method):
#     pass

# def search4Seeds(seed_methods, full_space_methods):
#     Seed2ProSpace = {}
#     if
#     for seed in seed_methods:
#         Seed2ProSpace[seed] = [seed]


def mytestCircle(project):
    Method2OwnTime, Method2Time, Method2Counts, Thresholds1 = readMethodMetrics(project)
    Dynamic_All_Relatins, Method2DynamicAllCallers, Method2DynamicAllCallees, Thresholds2 = readMethodDynamicAllRelations(project)
    methods = Method2OwnTime.keys()
    visited_methods = {}
    circle_methods = {}
    for item in Dynamic_All_Relatins:
        if item[0] not in visited_methods.keys():
            visited_methods[item[0]] = False
            circle_methods[item[0]] = []
        if item[1] not in visited_methods.keys():
            visited_methods[item[1]] = False
            circle_methods[item[1]] = []
    findCyclicInvoc(methods, circle_methods, Method2DynamicAllCallees, visited_methods)
    for item in circle_methods.keys():
        if len(circle_methods[item])>0:
            print item, circle_methods[item]

def collectInfo4Project(project):
    start = time.clock()
    print 'processing:', project
    pattern_record = csv.writer(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    pattern_record.writerow(['method', 'pattern', 'space'])
    # valid_methods = getValidMethodList(project)
    Method2OwnTime, Method2Time, Method2Counts, Method2Layer, Thresholds1 = readMethodMetrics(project)
    # Static_Relations, Method2StaticCallers, Method2StaticCallees = readMethodStaticRelations(project)
    Dynamic_All_Relatins, Method2DynamicAllCallers, Method2DynamicAllCallees, Thresholds2 = readMethodDynamicAllRelations(project, Method2Layer)
    Thresholds = dict(Thresholds1.items() + Thresholds2.items())
    # for m in Thresholds.keys():
    #     print m, Thresholds[m]
    methods = Method2OwnTime.keys()
    visited_methods = {}
    circle_methods = []
    for item in Dynamic_All_Relatins:
        if item[0] not in visited_methods.keys():
            visited_methods[item[0]] = False
            # circle_methods[item[0]] = []
        if item[1] not in visited_methods.keys():
            visited_methods[item[1]] = False
            # circle_methods[item[1]] = []
    findCyclicInvoc(methods, circle_methods, Method2DynamicAllCallees, visited_methods)
    # Method_Patterns = []  # method, patternkind, promspace

    nonpattern_count = 0
    pattern_counts = {'HotCyclic':0, 'HotRecur':0, 'HotExec':0, 'FreqExec':0, 'HotCallee':0}
    pattern_sizes = {'HotCyclic': 0, 'HotRecur': 0, 'HotExec': 0, 'FreqExec': 0, 'HotCallee': 0}
    # print Method2DynamicAllCallers['org.apache.pdfbox.pdmodel.graphics.xobject.PDXObjectImage.getMask()']
    # print Method2DynamicAllCallees['org.apache.pdfbox.pdmodel.graphics.xobject.PDXObjectImage.getMask()']
    # print Method2StaticCallers['org.apache.pdfbox.pdmodel.graphics.xobject.PDXObjectImage.getMask()']
    # print Method2StaticCallees['org.apache.pdfbox.pdmodel.graphics.xobject.PDXObjectImage.getMask()']
    count = 0
    for method in methods:
        isPattern = False
        count+=1
        print 'detecting', count, method
        # Pattern 1. Cyclic Invocations
        # Condition: m is in an invocation cycle & High Time of m & High execution_count of m
        # Space: All the methods in the cycle
        cyclicInvoc_result = []
        for circle in circle_methods:
            if method in circle:
                cyclicInvoc_result = circle
                break
        layer = Method2Layer[method]
        if len(cyclicInvoc_result)>1 and Method2Time[method]>=Thresholds['HighTime'][layer] \
                and Method2Counts[method]>=Thresholds['HighCounts'][layer]:
            # print method, 'HotCyclic', cyclicInvoc_result
            isPattern = True
            pattern_record.writerow([method, 'HotCyclic', '; '.join(cyclicInvoc_result)])
            pattern_counts['HotCyclic'] += 1
            pattern_sizes['HotCyclic'] += len(cyclicInvoc_result)
        # Pattern 2. Expensive Recursion
        # Condition: Self-Invocation & High Time of m & High execution_count of m
        # Space: m + Problematic_Space (the methods calling m with High Time)
        if method in Method2DynamicAllCallers.keys() and method in Method2DynamicAllCallers[method]:
            if Method2Time[method]>=Thresholds['HighTime'][layer]\
                    and Method2Counts[method]>=Thresholds['HighCounts'][layer]:
                if method in Method2DynamicAllCallers.keys():
                    prom_space = [i for i in Method2DynamicAllCallers[method] \
                                  if i!=method and i in methods
                                  and Method2Time[i]>=Thresholds['HighTime'][Method2Layer[i]]]
                    # if len(prom_space) != 0:
                    isPattern = True
                    pattern_record.writerow([method, 'HotRecur', '; '.join([method] + prom_space)])
                    pattern_counts['HotRecur'] += 1
                    pattern_sizes['HotRecur'] += len(prom_space)+1
                    # print method, 'HotRecur', [method]+prom_space
        # Pattern 3. Frequent Invocations
        # Condition:  High execution_count of m
        # Space: m + Problematic_Space (the methods calling m with high invocation_count)
        elif Method2Counts[method]>=Thresholds['HighCounts'][layer]:
            if method in Method2DynamicAllCallers.keys():
                prom_space = []
                for caller in Method2DynamicAllCallers[method]:
                    for (m1, m2, calls) in Dynamic_All_Relatins:
                        if m1==caller and m2==method:
                            if calls>=Thresholds['HighCalls'][layer]:
                                prom_space.append(caller)
                            break
                # if len(prom_space) != 0:
                isPattern = True
                pattern_record.writerow([method, 'FreqExec', '; '.join([method] + prom_space)])
                pattern_counts['FreqExec'] += 1
                pattern_sizes['FreqExec'] += len(prom_space)+1
                # print method, 'FreqExec', [method] + prom_space
        # Pattern 4. Expensive Own Execution
        # Condition: High OwnTime of m
        # Space: m + Problematic_Space (the methods calling m with High Time)
        elif Method2OwnTime[method]>=Thresholds['HighOwnTime'][layer]:
            if method in Method2DynamicAllCallers.keys():
                prom_space = [i for i in Method2DynamicAllCallers[method] \
                        if i!=method and i in methods and Method2Time[i] >= Thresholds['HighTime'][Method2Layer[i]]]
                # if len(prom_space) != 0:
                isPattern = True
                pattern_record.writerow([method, 'HotExec', '; '.join([method] + prom_space)])
                pattern_counts['HotExec'] += 1
                pattern_sizes['HotExec'] += len(prom_space) + 1
                # print method, 'HotExec', [method] + prom_space
        # Pattern 5. Expensive Callee Execution
        # Condition: Not High OwnTime & High Time of m
        # Space: m + Problematic_Space (the methods called by m with High Time)
        elif Method2Time[method]>=Thresholds['HighTime'][layer]:
            if method in Method2DynamicAllCallees.keys():
                prom_space = [i for i in Method2DynamicAllCallees[method] \
                        if i!=method and i in methods and Method2Time[i] >= Thresholds['HighTime'][Method2Layer[i]]]
                # if len(prom_space)!=0:
                isPattern = True
                pattern_record.writerow([method, 'HotCallee', '; '.join([method] + prom_space)])
                pattern_counts['HotCallee'] += 1
                pattern_sizes['HotCallee'] += len(prom_space) + 1
                # print method, 'HotCallee', [method] + prom_space

        if not isPattern:
            nonpattern_count += 1

    for pattern in pattern_counts.keys():
        if pattern_counts[pattern]==0:
            print pattern, 0, 0
        else:
            print pattern, pattern_counts[pattern], 1.0*pattern_sizes[pattern]/pattern_counts[pattern]
    print 'Non Pattern: ', nonpattern_count

    print("Space used:", (time.clock() - start))
    # Method2OverallSpace = {}
    # for method in methods:




def computeSeedSpace(project, ranked_full_seeds):
    seed2space = {}  #filter one-element-space
    seed2pattern = {}
    ranked_seed_space = [] # [space], [space]
    ranked_extended_seeds = [] # m, m
    total_methods = getAllMethodList(project)
    pattern_record = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, project)))
    for record in pattern_record:
        if pattern_record.line_num == 1:
            continue
        method = record[0]
        space = record[2].split('; ')
        if method not in seed2space.keys():
            seed2space[method] = space
            seed2pattern[method] = [record[1]]
        else:
            seed2space[method].extend(space)
            seed2pattern[method].append(record[1])
    for method in seed2space.keys():
        space = seed2space[method]
        new_space = []
        for i in space:
            if i not in new_space and i in total_methods:
                new_space.append(i)
        seed2space[method] = new_space
    for seed in ranked_full_seeds:
        if seed in seed2space.keys():
            ranked_seed_space.append(seed2space[seed])
            for m in seed2space[seed]:
                if m not in ranked_extended_seeds:
                    ranked_extended_seeds.append(m)
        else:
            ranked_seed_space.append([seed])
            if seed not in ranked_extended_seeds:
                ranked_extended_seeds.append(seed)
    # tem_record = csv.writer(open('temp.csv', 'wb+'))
    # for i in range(len(ranked_full_seeds)):
    #     tem_record.writerow([ranked_full_seeds[i], ranked_seed_space[i], ranked_extended_seeds[i]])
    # print len(ranked_full_seeds), ranked_full_seeds
    # print len(ranked_seed_space), ranked_seed_space
    # print len(ranked_extended_seeds), [i for i in ranked_extended_seeds if i not in ranked_full_seeds], ranked_extended_seeds
    return ranked_seed_space, ranked_extended_seeds, seed2space, seed2pattern



def getSeed2ValidSpace(project):
    seed2space = {}  # filter one-element-space
    total_methods = getAllMethodList(project)
    pattern_record = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, project)))
    for record in pattern_record:
        if pattern_record.line_num == 1:
            continue
        method = record[0]
        space = record[2].split('; ')
        if method not in seed2space.keys():
            seed2space[method] = space
        else:
            seed2space[method].extend(space)
    for method in seed2space.keys():
        space = seed2space[method]
        new_space = []
        for i in space:
            if i not in new_space and i in total_methods:
                new_space.append(i)
        seed2space[method] = new_space
    return seed2space




if __name__ == '__main__':
    # print isSelfRecursion('A')
    # mytestCircle('pdfbox-1.8.4-2014.1')

    # collectInfo4Project('avro-1.3.0')
    # collectInfo4Project('avro-1.6.0')
    # collectInfo4Project('avro-1.8.1')
    # collectInfo4Project('ivy-2.0.0-2009.1')
    # collectInfo4Project('ivy-2.1.0-2009.10')
    # collectInfo4Project('ivy-2.2.0-2010.9')
    # collectInfo4Project('ivy-2.3.0-2013.1')
    # collectInfo4Project('ivy-2.4.0-2014.12')
    # collectInfo4Project('pdfbox-1.8.4-2014.1')
    # collectInfo4Project('pdfbox-1.8.10-2015.7')
    # collectInfo4Project('pdfbox-2.0.0')
    # collectInfo4Project('pdfbox-2.0.4-2016.12')

    collectInfo4Project('cxf-3.0.1')

    # unifyMethodDynamicAllRelations('cxf-3.1.11-2017.4')

    # unifyMethodDynamicAllRelations('pdfbox-1.8.4-2014.1')
    # # unifyMethodDynamicAllRelations('pdfbox-1.8.6-2014.6')
    # unifyMethodDynamicAllRelations('pdfbox-1.8.10-2015.7')
    # # unifyMethodDynamicAllRelations('pdfbox-1.8.11-2016.1')
    # unifyMethodDynamicAllRelations('pdfbox-2.0.0')
    # # unifyMethodDynamicAllRelations('pdfbox-2.0.2-2016.6')
    # unifyMethodDynamicAllRelations('pdfbox-2.0.4-2016.12')
    #
    # unifyMethodDynamicAllRelations('avro-1.8.1')
    # unifyMethodDynamicAllRelations('avro-1.6.0')
    # unifyMethodDynamicAllRelations('avro-1.3.0')
    #
    # unifyMethodDynamicAllRelations('ivy-2.0.0-2009.1')
    # unifyMethodDynamicAllRelations('ivy-2.1.0-2009.10')
    # unifyMethodDynamicAllRelations('ivy-2.2.0-2010.9')
    # unifyMethodDynamicAllRelations('ivy-2.3.0-2013.1')
    # unifyMethodDynamicAllRelations('ivy-2.4.0-2014.12')

