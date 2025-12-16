import csv
import sys
sys.path.append('..')
sys.path.append('../EntityExtractor')
import parameter
import analyzeRefactoring
import computeRanking
import computeSpace


def getMethodPerfInfo(method2space, method2score, method):
    if method not in method2space.keys():
        return method2score[method], None, None
    space = method2space[method]
    space_size = len(space)
    space_score = sum([method2score[m] for m in space])/space_size
    return method2score[method], space_size, space_score



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


def check_mapped_method(method, all_methods):
    for m in all_methods:
        if m.replace(' ', '') == method.replace(' ', ''):
            return m
    for m in all_methods:
        name1 = m.split('(')[0]
        parameters1 = m.split('(')[1].split(')')[0].replace(' ', '')
        name2 = method.split('(')[0]
        parameters2 = method.split('(')[1].split(')')[0].replace(' ', '')
        if name1 == name2 and isequal_parameters(parameters1, parameters2):
            # print method, m
            return m
    for m in all_methods:
        if m[: -len(m.split('(')[-1])-1] == method[: -len(method.split('(')[-1])-1]:
            # print method, m
            return m
    else:
        return None



def evaluateChange(project, version1, version2):
    out_record = csv.writer(open(parameter.DATA_ROOT+'\\%s\\score_changes_%s_%s.csv' % (project, version1, version2), 'wb+'))
    out_record.writerow(['method1','method2','method_score1','method_score2','space_size1','space_size2','space_score1','space_score2'])

    refactoring_methods = analyzeRefactoring.getRefactoredMethods(project, version1, version2)

    pattern_record1 = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, version1)))
    method2space1 = {}
    all_methods1 = computeSpace.getValidMethodList(version1)
    for record in pattern_record1:
        if pattern_record1.line_num == 1:
            continue
        space = record[2].split('; ')
        for m in space:
            # if m=='org.apache.pdfbox.cos.COSBoolean.COSBoolean(boolean)':
            #     print 'yes appear'
            if m not in all_methods1:
                continue
            if m not in method2space1.keys():
                method2space1[m] = []
            method2space1[m].extend([i for i in space if i not in method2space1[m] and i in all_methods1])
    pattern_record2 = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, version2)))
    method2space2 = {}
    all_methods2 = computeSpace.getValidMethodList(version2)
    for record in pattern_record2:
        if pattern_record2.line_num == 1:
            continue
        space = record[2].split('; ')
        for m in space:
            if m not in all_methods2:
                continue
            if m not in method2space2.keys():
                method2space2[m] = []
            method2space2[m].extend([i for i in space if i not in method2space2[m] and i in all_methods2])

    for formulas in parameter.FORMULAS:
        print 'formulas: ', formulas
        changed_score = []
        changed_space_size = []
        changed_space_score = []
        _, method2score1 = computeRanking.getRankedFullMethods(project, version1, formulas)
        # print method2score1
        _, method2score2 = computeRanking.getRankedFullMethods(project, version2, formulas)
        # print method2score2
        for (method1, method2) in refactoring_methods:
            method1 = check_mapped_method(method1, method2score1.keys())
            method2 = check_mapped_method(method2, method2score2.keys())
            if method1 is None or method2 is None:
                # print 'no!!'
                continue
            # print method1, method2, method2score1.keys()
            method_score1, space_size1, space_score1 = getMethodPerfInfo(method2space1, method2score1, method1)
            method_score2, space_size2, space_score2 = getMethodPerfInfo(method2space2, method2score2, method2)
            changed_score.append(method_score2-method_score1)
            if space_size1 is not None and space_size2 is not None:
                changed_space_size.append(space_size2 - space_size1)
                changed_space_score.append(space_score2 - space_score1)
                # print 'method1:', method1, 'method_score1:', method_score1, 'space_size1:', space_size1, 'space_score1:', space_score1
                # print 'method2:', method2, 'method_score2:', method_score2, 'space_size2:', space_size2, 'space_score2:', space_score2
            out_record.writerow([method1,method2,method_score1,method_score2,space_size1,space_size2,space_score1,space_score2])
        print 'Total refactoring methods:', len(refactoring_methods), '  Valid refactoring methods:', len(changed_score)
        print 'Number of performance score (the lower, the better): lower %d, equal %d, higher %d'\
                %(len([i for i in changed_score if i < 0]),
                  len([i for i in changed_score if i == 0]),
                  len([i for i in changed_score if i > 0]))
        print 'Number of space size (the lower, the better): lower %d, equal %d, higher %d' \
              % (len([i for i in changed_space_size if i < 0]),
                 len([i for i in changed_space_size if i == 0]),
                 len([i for i in changed_space_size if i > 0]))
        print 'Number of space score (the lower, the better): lower %d, equal %d, higher %d' \
              % (len([i for i in changed_space_score if i < 0]),
                 len([i for i in changed_space_score if i == 0]),
                 len([i for i in changed_space_score if i > 0]))


def evaluatePatternChange(project, version1, version2):
    out_record = csv.writer(open(parameter.DATA_ROOT+'\\%s\\score_pattern_changes_%s_%s.csv' % (project, version1, version2), 'wb+'))
    out_record.writerow(['method1','method2','method_score1','method_score2'])
    out_record2 = csv.writer(
        open(parameter.DATA_ROOT + '\\%s\\score_seed_changes_%s_%s.csv' % (project, version1, version2), 'wb+'))
    out_record2.writerow(['method1', 'method2', 'method_score1', 'method_score2'])

    refactoring_methods = analyzeRefactoring.getRefactoredMethods(project, version1, version2)

    pattern_record1 = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, version1)))
    # method2space1 = computeSpace.getSeed2ValidSpace(version1)
    all_methods1 = computeSpace.getValidMethodList(version1)
    method2space1 = {}
    for record in pattern_record1:
        if pattern_record1.line_num == 1:
            continue
        space = record[2].split('; ')
        for m in space:
            if m not in all_methods1:
                continue
            if m not in method2space1.keys():
                method2space1[m] = []
            method2space1[m].extend([i for i in space if i not in method2space1[m] and i in all_methods1])

    pattern_record2 = csv.reader(open('%s//%s//method_patterns_full.csv' % (parameter.SUBJECT_ROOT, version2)))
    # method2space2 = computeSpace.getSeed2ValidSpace(version2)
    all_methods2 = computeSpace.getValidMethodList(version2)
    method2space2 = {}
    for record in pattern_record2:
        if pattern_record2.line_num == 1:
            continue
        space = record[2].split('; ')
        for m in space:
            if m not in all_methods2:
                continue
            if m not in method2space2.keys():
                method2space2[m] = []
            method2space2[m].extend([i for i in space if i not in method2space2[m] and i in all_methods2])

    for formulas in parameter.FORMULAS:
        print 'formulas: ', formulas
        changed_score = []
        visited_methods = []
        visited_methods2 = []
        _, method2score1 = computeRanking.getRankedFullMethods(project, version1, formulas)
        # print method2score1
        _, method2score2 = computeRanking.getRankedFullMethods(project, version2, formulas)
        # print method2score2
        for (method1, method2) in refactoring_methods:
            method1 = check_mapped_method(method1, method2score1.keys())
            method2 = check_mapped_method(method2, method2score2.keys())
            if method1 is None or method2 is None or method1 in visited_methods:
                # print 'no!!'
                continue
            if method1 not in visited_methods2:
                out_record2.writerow([method1, method2, method2score1[method1], method2score2[method2]])
                visited_methods2.append(method1)
            if method1 not in method2space1.keys() or method2 not in method2space2.keys():
                if method1 not in visited_methods:
                    out_record.writerow([method1, method2, method2score1[method1], method2score2[method2]])
                    changed_score.append(method2score2[method2]-method2score1[method1])
                    visited_methods.append(method1)
                continue
            space = method2space1[method1]
            for m in space:
                if m in method2score2.keys() and m not in visited_methods:
                    out_record.writerow([m, m, method2score1[m], method2score2[m]])
                    changed_score.append(method2score2[m] - method2score1[m])
                    visited_methods.append(m)

        print 'Total pattern methods:', len(changed_score)
        print 'Number of performance score (the lower, the better): lower %d, equal %d, higher %d'\
                %(len([i for i in changed_score if i < 0]),
                  len([i for i in changed_score if i == 0]),
                  len([i for i in changed_score if i > 0]))




if __name__ == '__main__':
    evaluateChange('avro', 'avro-1.6.0', 'avro-1.8.1')
    # evaluateChange('ivy', 'ivy-2.0.0-2009.1', 'ivy-2.4.0-2014.12')
    # evaluateChange('pdfbox', 'pdfbox-1.8.4-2014.1', 'pdfbox-2.0.4-2016.12')

    evaluatePatternChange('avro', 'avro-1.6.0', 'avro-1.8.1')
    # evaluatePatternChange('ivy', 'ivy-2.0.0-2009.1', 'ivy-2.4.0-2014.12')
    # evaluatePatternChange('pdfbox', 'pdfbox-1.8.4-2014.1', 'pdfbox-2.0.4-2016.12')