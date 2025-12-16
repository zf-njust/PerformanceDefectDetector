import csv
import sys
sys.path.append('..')
import parameter

def get_record(project, filename):
    record = []
    record_file = csv.reader(open('%s//%s//%s.csv' % (parameter.SUBJECT_ROOT, project, filename)))
    for item in record_file:
        if record_file.line_num == 1:
            continue
        if item[0].find('Test')!=-1 or item[0].find('test')!=-1 or item[1].find('Test')!=-1 or item[1].find('test')!=-1:
            continue
        record.append(item)
    return record


def isequal_parameters(parameters1, parameters2):
    # print(parameters1, parameters2)
    parameters1 = parameters1[:].replace(' ', '')
    parameters2 = parameters2[:].replace(' ', '')
    # '<>'
    while parameters1.find('<')!=-1:
        parameters1 = parameters1[0:(parameters1.index('<'))]+parameters1[(parameters1.index('>')+1):]
    while parameters2.find('<')!=-1:
        parameters2 = parameters2[0:(parameters2.index('<'))]+parameters2[(parameters2.index('>')+1):]
    # ...
    parameters1 = parameters1.replace('...', '[]')
    parameters2 = parameters2.replace('...', '[]')
    # print(parameters1,parameters2)
    if parameters1 == parameters2:
        return True

    parameters1_array = parameters1.split(',')
    parameters2_array = parameters2.split(',')
    if len(parameters1_array) != len(parameters2_array):
        return False
    for index in range(len(parameters1_array)):
        p1 = parameters1_array[index]
        p2 = parameters2_array[index]
        if p1.find('$')==-1 and p1.find('.')==-1 and p2.find('$')==-1 and p2.find('.')==-1:
            if p1==p2:
                continue
            else:
                return False
        p1 = p1.replace('$', '.')
        p2 = p2.replace('$', '.')
        if p1==p2 or p1 in p2.split('.') or p2 in p1.split('.'):
            continue
        else:
            return False
    return True


def isequal_parameters_relax(parameters1, parameters2):
    # print(parameters1, parameters2)
    parameters1 = parameters1[:].replace(' ', '')
    parameters2 = parameters2[:].replace(' ', '')
    # '<>'
    while parameters1.find('<')!=-1:
        parameters1 = parameters1[0:(parameters1.index('<'))]+parameters1[(parameters1.index('>')+1):]
    while parameters2.find('<')!=-1:
        parameters2 = parameters2[0:(parameters2.index('<'))]+parameters2[(parameters2.index('>')+1):]
    # ...
    parameters1 = parameters1.replace('...', '[]')
    parameters2 = parameters2.replace('...', '[]')
    # print(parameters1,parameters2)
    if parameters1 == parameters2:
        return True

    parameters1_array = parameters1.split(',')
    parameters2_array = parameters2.split(',')
    if len(parameters1_array) != len(parameters2_array):
        return False
    for index in range(len(parameters1_array)):
        p1 = parameters1_array[index]
        p2 = parameters2_array[index]
        if p1=='Object' or p2=='Object':
            continue
        if p1.find('$')==-1 and p1.find('.')==-1 and p2.find('$')==-1 and p2.find('.')==-1:
            if p1==p2:
                continue
            else:
                return False
        p1 = p1.replace('$', '.')
        p2 = p2.replace('$', '.')
        if p1==p2 or p1 in p2.split('.') or p2 in p1.split('.'):
            continue
        else:
            return False
    return True



def combine_metrics_all(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        per_metric = get_record(project, 'method_time_dev')
        arch_metric = get_record(project, 'method_arch')
        out_record = csv.writer(open('%s//%s//method_all_metrics_dev.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'E':
        per_metric = get_record(project, 'method_time_evo')
        arch_metric = get_record(project, 'method_arch')
        out_record = csv.writer(open('%s//%s//method_all_metrics_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'D+E':
        per_metric = get_record(project, 'method_time_dev_evo')
        arch_metric = get_record(project, 'method_arch')
        out_record = csv.writer(open('%s//%s//method_all_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    else:
        print 'error!'
        return

    static_metric = csv.reader(open('%s//%s//method_static_metric.csv' % (parameter.SUBJECT_ROOT, project)))
    out_record.writerow(['class path','method name','method arguments','module'
                         'LOC', 'Cyclomatic', 'FanIn', 'FanOut'
                         'Time', 'OwnTime', 'Count',
                         'Layer', 'Size', 'upperDepth', 'upperWidth', 'lowerDepth', 'lowerWidth'
                         ])
    for record in static_metric:
        if static_metric.line_num == 1:
            continue
        if record[0].find('Test')!=-1 or record[0].find('test')!=-1 or record[1].find('Test')!=-1 or record[1].find('test')!=-1:
            continue
        # construction method
        if record[1] == record[0].split('\\')[-1][:-5]:
            record[1] = '<init>'
        newrow = record[:]
        # performance
        for item in per_metric:
            if item[0]==record[0] and item[1]==record[1] and isequal_parameters(item[2], record[2]):
                newrow.extend([item[3], item[4], item[5]])
                per_metric.remove(item)
                break
        else:
            for item in per_metric:
                if item[0] == record[0] and item[1] == record[1] and isequal_parameters_relax(item[2], record[2]):
                    newrow.extend([item[3], item[4], item[5]])
                    per_metric.remove(item)
                    break
            else:
                newrow.extend(['','',''])
        # architecture
        for item in arch_metric:
            if item[0] == record[0] and item[1] == record[1] and isequal_parameters(item[2], record[2]):
                newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                arch_metric.remove(item)
                break
        else:
            for item in arch_metric:
                if item[0] == record[0] and item[1] == record[1] and isequal_parameters_relax(item[2], record[2]):
                    newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                    arch_metric.remove(item)
                    break
            else:
                newrow.extend(['','','','',''])
        out_record.writerow(newrow)

    for record in per_metric:
        newrow = record[0:3]+['','']+record[3:]
        # architecture
        for item in arch_metric:
            if item[0] == record[0] and item[1] == record[1] and item[2]==record[2]:
                newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                arch_metric.remove(item)
                break
        else:
            newrow.extend(['','','','',''])
        out_record.writerow(newrow)

    for item in arch_metric:
        print('method_arch missing:', item)


def combine_metrics_valid(project, tests_source='D'):  #tests_source: Developers, Evosuite, M
    if tests_source == 'D':
        per_metric = get_record(project, 'method_time_dev')
        arch_metric = get_record(project, 'method_arch_dev')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_dev.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'E':
        per_metric = get_record(project, 'method_time_evo')
        arch_metric = get_record(project, 'method_arch_evo')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'D+E':
        per_metric = get_record(project, 'method_time_dev_evo')
        arch_metric = get_record(project, 'method_arch_dev_evo')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    else:
        print 'error!'
        return
    static_metric = csv.reader(open('%s//%s//method_static_metric.csv' % (parameter.SUBJECT_ROOT, project)))
    out_record.writerow(['class path', 'method name', 'method arguments',
                         'LOC', 'Cyclomatic',
                         'Time', 'OwnTime', 'Count',
                         'Layer', 'Callees', 'CalleeInvocations', 'Callers', 'CallerInvocations'
                         ])
    for record in static_metric:
        if static_metric.line_num == 1:
            continue
        if record[0].find('Test') != -1 or record[0].find('test') != -1 or record[1].find('Test') != -1 or record[
            1].find('test') != -1:
            continue
        # construction method
        if record[1] == record[0].split('\\')[-1][:-5]:
            record[1] = '<init>'
        newrow = record[:]
        # performance
        for item in per_metric:
            if item[0] == record[0] and item[1] == record[1] and isequal_parameters(item[2], record[2]):
                newrow.extend([item[3], item[4], item[5]])
                per_metric.remove(item)
                break
        else:
            for item in per_metric:
                if item[0] == record[0] and item[1] == record[1] and isequal_parameters_relax(item[2], record[2]):
                    newrow.extend([item[3], item[4], item[5]])
                    per_metric.remove(item)
                    break
            else:
                newrow.extend(['','',''])

        # architecture
        for item in arch_metric:
            if item[0] == record[0] and item[1] == record[1] and isequal_parameters(item[2], record[2]):
                newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                arch_metric.remove(item)
                break
        else:
            for item in arch_metric:
                if item[0] == record[0] and item[1] == record[1] and isequal_parameters_relax(item[2], record[2]):
                    newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                    arch_metric.remove(item)
                    break
            else:
                newrow.extend(['','','','',''])

        for i in newrow[5:]:
            if i != '':
                out_record.writerow(newrow)
                break

    for record in per_metric:
        newrow = record[0:3] + ['', ''] + record[3:]
        # architecture
        for item in arch_metric:
            if item[0] == record[0] and item[1] == record[1] and item[2] == record[2]:
                newrow.extend([item[3], item[4], item[5], item[6], item[7]])
                arch_metric.remove(item)
                break
        else:
            newrow.extend(['', '', '', '', ''])
        out_record.writerow(newrow)

    for item in arch_metric:
        print('method_arch missing:', item)


if __name__ == '__main__':
    combine_metrics_all('avro-1.8.1', 'D')
    combine_metrics_valid('avro-1.8.1', 'D')
    combine_metrics_all('avro-1.8.1', 'D+E')
    combine_metrics_valid('avro-1.8.1', 'D+E')

    combine_metrics_all('avro-1.6.0', 'D')
    combine_metrics_valid('avro-1.6.0', 'D')
    combine_metrics_all('avro-1.6.0', 'D+E')
    combine_metrics_valid('avro-1.6.0', 'D+E')

    combine_metrics_all('avro-1.3.0', 'D')
    combine_metrics_valid('avro-1.3.0', 'D')
    combine_metrics_all('avro-1.3.0', 'D+E')
    combine_metrics_valid('avro-1.3.0', 'D+E')


    # combine_metrics_all('pdfbox-1.8.4-2014.1')
    # combine_metrics_valid('pdfbox-1.8.4-2014.1')
    #
    # combine_metrics_all('pdfbox-1.8.6-2014.6')
    # combine_metrics_valid('pdfbox-1.8.6-2014.6')
    #
    # combine_metrics_all('pdfbox-1.8.8-2014.12')
    # combine_metrics_valid('pdfbox-1.8.8-2014.12')

    # combine_metrics_all('pdfbox-1.8.10-2015.7', 'D')
    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D')
    # combine_metrics_all('pdfbox-1.8.10-2015.7', 'D+E')
    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D+E')

    # combine_metrics_all('pdfbox-1.8.11-2016.1')
    # combine_metrics_valid('pdfbox-1.8.11-2016.1')

    # combine_metrics_all('pdfbox-2.0.0', 'D')
    # combine_metrics_valid('pdfbox-2.0.0', 'D')
    # combine_metrics_all('pdfbox-2.0.0', 'D+E')
    # combine_metrics_valid('pdfbox-2.0.0', 'D+E')

    # #
    # combine_metrics_all('pdfbox-2.0.2-2016.6')
    # combine_metrics_valid('pdfbox-2.0.2-2016.6')
    # #
    # combine_metrics_all('pdfbox-2.0.4-2016.12')
    # combine_metrics_valid('pdfbox-2.0.4-2016.12')

    # print(isequal_parameters('COSBase, PreflightContext, List, Map', 'COSBase, PreflightContext, List<AbstractActionManager>, Map<COSObjectKey, Boolean>'))
    # print(isequal_parameters('PDFOperator, List', 'PDFOperator, List < COSBase >'))
    # print(isequal_parameters('CharSequence, Parser$SyntaxHandler', 'CharSequence, SyntaxHandler'))
    # print(isequal_parameters('CFFParser$DictData, String, Number', 'DictData, String, Number'))
    # print(isequal_parameters('CFFCharset$Entry','Entry'))
    # print(isequal_parameters('Token.Kind','Token$Kind'))
    # print(isequal_parameters('GlyphRenderer$Point, GlyphRenderer$Point','int,int'))