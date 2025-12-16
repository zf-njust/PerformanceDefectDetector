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






def combine_metrics_valid(project, tests_source='D'):
    arch_metric = get_record(project, 'method_arch')
    if tests_source == 'D':
        per_metric = get_record(project, 'method_time_all_dev')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_dev.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
        out_all_record = csv.writer(open('%s//%s//method_all_metrics_dev.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'E':
        per_metric = get_record(project, 'method_time_all_evo')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
        out_all_record = csv.writer(open('%s//%s//method_all_metrics_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    elif tests_source == 'D+E':
        per_metric = get_record(project, 'method_time_all_dev_evo')
        out_record = csv.writer(open('%s//%s//method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
        out_all_record = csv.writer(open('%s//%s//method_all_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    else:
        print('error!')
        return

    static_metric = csv.reader(open('%s//%s//method_static_metric_loop.csv' % (parameter.SUBJECT_ROOT, project)))
    out_record.writerow(['method',
                         'Layer', 'Size', 'upperDepth', 'upperWidth', 'lowerDepth', 'lowerWidth',
                         'LOC', 'Cyclomatic', 'FanIn', 'FanOut', 'Loop',
                         'Time', 'OwnTime', 'Count'
                         ])
    out_all_record.writerow(['method',
                         'Layer', 'Size', 'upperDepth', 'upperWidth', 'lowerDepth', 'lowerWidth',
                         'LOC', 'Cyclomatic', 'FanIn', 'FanOut', 'Loop',
                         'Time', 'OwnTime', 'Count'
                         ])
    # class_record = csv.reader(open('%s//%s//project_info.csv' % (parameter.SUBJECT_ROOT, project)))
    # Path2Package = {}
    # for record in class_record:
    #     if class_record.line_num == 1:
    #         continue
    #     Path2Package[record[1]] = record[2]
    for record in static_metric:
        if static_metric.line_num == 1:
            continue
        if record[0].split('.')[-2].startswith('(') or record[0].find('Test') != -1 or record[0].find('test') != -1:
            continue
        print static_metric.line_num, record
        newrow = [record[0]]
        name = record[0].split('(')[0]
        parameters = record[0].split('(')[1].split(')')[0].replace(' ', '')
        # architecture
        for item in arch_metric:
            name1 = item[0].split('(')[0]
            parameters1 = item[0].split('(')[1].split(')')[0].replace(' ', '')
            if isequal_methodname(name, name1) and isequal_parameters(parameters, parameters1):
                newrow.extend([item[1], item[2], item[3], item[4], item[5], item[6]])
                arch_metric.remove(item)
                break
        else:
            for item in arch_metric:
                name1 = item[0].split('(')[0]
                parameters1 = item[0].split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name, name1) and len(parameters)>0 and len(parameters1)>0 and \
                                parameters.count(',')==parameters1.count(','):
                    # print record, item
                    newrow.extend([item[1], item[2], item[3], item[4], item[5], item[6]])
                    arch_metric.remove(item)
                    break
            else:
                newrow.extend(['','','','','',''])
        newrow.extend([record[1], record[2], record[3], record[4], record[5]])
        # performance
        for item in per_metric:
            name1 = item[0].split('(')[0]
            parameters1 = item[0].split('(')[1].split(')')[0].replace(' ', '')
            if isequal_methodname(name, name1) and isequal_parameters(parameters, parameters1):
                newrow.extend([item[1], item[2], item[3]])
                per_metric.remove(item)
                break
        else:
            for item in per_metric:
                name1 = item[0].split('(')[0]
                parameters1 = item[0].split('(')[1].split(')')[0].replace(' ', '')
                if isequal_methodname(name, name1) and len(parameters)>0 and len(parameters1)>0 and \
                                parameters.count(',')==parameters1.count(','):
                    # print record, item
                    newrow.extend([item[1], item[2], item[3]])
                    per_metric.remove(item)
                    break
            else:
                newrow.extend(['', '', ''])
        if '' not in newrow:
            out_record.writerow(newrow)
        out_all_record.writerow(newrow)

    # print len(arch_metric), len([i for i in per_metric if i[0].startswith('org.apache.')])

    # for item in arch_metric:
    #     print('arch_metric missing:', item)
    # for item in per_metric:
    #     if item[0].startswith('org.apache.'):
    #         print('per_metric missing:', item)

if __name__ == '__main__':
    combine_metrics_valid('cxf-3.0.1', 'D')

    # combine_metrics_valid('avro-1.8.1', 'D')
    # combine_metrics_valid('avro-1.8.1', 'D+E')
    #
    # combine_metrics_valid('avro-1.6.0', 'D')
    # combine_metrics_valid('avro-1.6.0', 'D+E')
    #
    # combine_metrics_valid('avro-1.3.0', 'D')
    # combine_metrics_valid('avro-1.3.0', 'D+E')
    #
    # combine_metrics_valid('ivy-2.0.0-2009.1', 'D')
    # combine_metrics_valid('ivy-2.0.0-2009.1', 'D+E')
    #
    # combine_metrics_valid('ivy-2.1.0-2009.10', 'D')
    # combine_metrics_valid('ivy-2.1.0-2009.10', 'D+E')
    #
    # combine_metrics_valid('ivy-2.2.0-2010.9', 'D')
    # combine_metrics_valid('ivy-2.2.0-2010.9', 'D+E')
    #
    # combine_metrics_valid('ivy-2.3.0-2013.1', 'D')
    # combine_metrics_valid('ivy-2.3.0-2013.1', 'D+E')
    #
    # combine_metrics_valid('ivy-2.4.0-2014.12', 'D')
    # combine_metrics_valid('ivy-2.4.0-2014.12', 'D+E')
    #
    #
    # combine_metrics_valid('pdfbox-1.8.4-2014.1', 'D')
    # combine_metrics_valid('pdfbox-1.8.4-2014.1', 'D+E')
    # combine_metrics_valid('pdfbox-1.8.6-2014.6', 'D')
    # combine_metrics_valid('pdfbox-1.8.6-2014.6', 'D+E')
    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D')
    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D+E')
    # combine_metrics_valid('pdfbox-1.8.11-2016.1', 'D')
    # combine_metrics_valid('pdfbox-1.8.11-2016.1', 'D+E')
    # combine_metrics_valid('pdfbox-2.0.0', 'D')
    # combine_metrics_valid('pdfbox-2.0.0', 'D+E')
    # combine_metrics_valid('pdfbox-2.0.2-2016.6', 'D')
    # combine_metrics_valid('pdfbox-2.0.2-2016.6', 'D+E')
    # combine_metrics_valid('pdfbox-2.0.4-2016.12', 'D')
    # combine_metrics_valid('pdfbox-2.0.4-2016.12', 'D+E')




    #
    # combine_metrics_all('pdfbox-1.8.6-2014.6')
    # combine_metrics_valid('pdfbox-1.8.6-2014.6')
    #
    # combine_metrics_all('pdfbox-1.8.8-2014.12')
    # combine_metrics_valid('pdfbox-1.8.8-2014.12')

    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D')
    # combine_metrics_valid('pdfbox-1.8.10-2015.7', 'D+E')

    # combine_metrics_all('pdfbox-1.8.11-2016.1')
    # combine_metrics_valid('pdfbox-1.8.11-2016.1')



    # #
    # combine_metrics_all('pdfbox-2.0.2-2016.6')
    # combine_metrics_valid('pdfbox-2.0.2-2016.6')
    # #


    # print(isequal_parameters('COSBase, PreflightContext, List, Map', 'COSBase, PreflightContext, List<AbstractActionManager>, Map<COSObjectKey, Boolean>'))
    # print(isequal_parameters('PDFOperator, List', 'PDFOperator, List < COSBase >'))
    # print(isequal_parameters('CharSequence, Parser$SyntaxHandler', 'CharSequence, SyntaxHandler'))
    # print(isequal_parameters('CFFParser$DictData, String, Number', 'DictData, String, Number'))
    # print(isequal_parameters('CFFCharset$Entry','Entry'))
    # print(isequal_parameters('Token.Kind','Token$Kind'))
    # print(isequal_parameters('GlyphRenderer$Point, GlyphRenderer$Point','int,int'))