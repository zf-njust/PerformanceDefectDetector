import csv
import sys
sys.path.append('..')
sys.path.append('Experiments')
import parameter
import evaluateRanking


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


def getValidMethodList(version):
    valid_methods = []
    metric_record = csv.reader(open('%s//%s//method_all_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, version)))
    for record in metric_record:
        if metric_record.line_num==1:
            continue
        valid_methods.append(record[0])
    return valid_methods

def getValidHotSpots(version):
    valid_methods = getValidMethodList(version)
    hotspots = []
    hotsplot_record = csv.reader(open('%s\\%s\\hotspots.csv' % (parameter.SUBJECT_ROOT, version)))
    for record in hotsplot_record:
        if hotsplot_record.line_num==1:
            continue
        m = record[0]
        # print m
        if m in valid_methods:
            hotspots.append(m)
            # print m
            continue
        name1 = m.split('(')[0]
        parameters1 = m.split('(')[1].split(')')[0].replace(' ', '')
        for valid_method in valid_methods:
            name2 = valid_method.split('(')[0]
            parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
            if isequal_methodname(name1, name2) and isequal_parameters(parameters1, parameters2):
                hotspots.append(valid_method)
                # print valid_method
                break
        else:
            for valid_method in valid_methods:
                name2 = valid_method.split('(')[0]
                parameters2 = valid_method.split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name1, name2) and len(parameters1)>0 and len(parameters2)>0 and \
                                parameters1.count(',')==parameters2.count(','):
                    # print valid_method
                    hotspots.append(valid_method)
                    break
            else:
                if m.startswith('org.apache.'):
                    print m
                    hotspots.append(m)
                # else:
                #     print 'No finding ', m
    return hotspots


def evaluate(project, version):
    Method2Issues, Total_Methods, Max_Issues = evaluateRanking.NumberofMethodsSummary(project, version)
    hotspots = getValidHotSpots(version)
    print 'Number of Hotspots:', len(hotspots)
    count = 0
    totalcount = 0
    for full_method in hotspots:
        simple_method = full_method[: -len(full_method.split('(')[-1]) - 1]
        totalcount += 1
        if totalcount>106:
            break
        if simple_method in Method2Issues.keys():

            for issue in Method2Issues[simple_method]:
                # change condition here!!!
                if issue not in Max_Issues:
                    # print issue
                    continue
                count += 1
                break
    print "Refactoring Methods:", count


if __name__ == '__main__':
    # evaluate('avro', 'avro-1.6.0')
    # evaluate('ivy', 'ivy-2.0.0-2009.1')
    # evaluate('pdfbox', 'pdfbox-1.8.4-2014.1')
    evaluate('cxf', 'cxf-3.0.1')