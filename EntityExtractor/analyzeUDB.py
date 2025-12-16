# this is used in Python 3

import understand
import csv
import sys
sys.path.append('..')
import parameter
import time


def dump_project_info(project, projname, srcdir):
    db_path = '%s\\%s\\%s.udb' %(parameter.SUBJECT_ROOT, project, projname)
    out_path = '%s\\%s\\project_info.csv' %(parameter.SUBJECT_ROOT, project)
    out_result = csv.writer(open(out_path, 'w', encoding='utf8', newline=''))
    out_result.writerow(['class', 'path', 'package', 'methods'])
    db = understand.open(db_path)
    total_files_count = len(db.ents("File"))
    print('total files count: %d' %total_files_count)

    class_ents = db.ents("class ~unknown ~unresolved")
    for i in range(len(class_ents) - 1, -1, -1):
        if class_ents[i].library() != "":
            del class_ents[i]
            continue
        # if (class_ents[i].refs("java definein", "class")):
        #     del class_ents[i]
        #     continue
        # if (class_ents[i].refs("java definein", "method")):
        #     del class_ents[i]
        #     continue
    print('total java classes count: %d' %len(class_ents))

    for ent in class_ents:
        methods = ','.join([e.simplename() for e in ent.ents("Java Define", "method")])
        classname = ent.simplename()
        filepath = ent.parent().longname()[(len(srcdir)+1):]
        for e in ent.ents('containin'):
            if e.kind().check('Package'):
                package = e.longname()
                break
        else:
            print('cannot find package: ', classname)
            continue
        out_result.writerow([classname, filepath, package, methods])



def dump_method_metric(project, projname, srcdir):
    start = time.clock()
    db_path = '%s\\%s\\%s.udb' %(parameter.SUBJECT_ROOT, project, projname)
    out_path = '%s\\%s\\method_static_metric_loop.csv' %(parameter.SUBJECT_ROOT, project)
    out_result = csv.writer(open(out_path, 'w', encoding='utf8', newline=''))
    out_result.writerow(['method', 'LOC', 'Cyclomatic', 'FanIn', 'FanOut', 'Loop'])
    db = understand.open(db_path)

    loc = 0
    methods = 0


    class_ents = db.ents("class ~unknown ~unresolved")
    for i in range(len(class_ents) - 1, -1, -1):
        if class_ents[i].library() != "":
            del class_ents[i]
            continue

    for ent in class_ents:
        for e in ent.ents('containin'):
            if e.kind().check('Package'):
                break
        else:
            # print(ent.simplename())
            continue

        looplines = []
        for lexeme in ent.lexer():
            if lexeme.token() == 'Keyword' and (lexeme.text() == 'for' or lexeme.text() == 'while'):
                looplines.append(lexeme.line_begin())

        # filepath = ent.parent().longname()[(len(srcdir)+1):]
        # print (ent.parent().longname())
        # print ([i.ent().simplename() for i in ent.refs("Java Define", "method")])
        # print([i.simplename() for i in ent.ents("Java Define", "method")])
        method_lines = []
        for ref in ent.refs("Java Define"):
            method_lines.append(ref.line())
        method_lines.sort()
        # if ent.parent().longname()=="C:\\Users\chenzhifei\Desktop\subjects\\avro-1.8.1\\avro-1.8.1-src\lang\java\\avro\src\main\java\org\\apache\\avro\Schema.java":
        #     print(looplines)
        #     print(method_lines)
        for ref in ent.refs("Java Define", "method"):
            e = ref.ent()
            line = ref.line()
            method_index = method_lines.index(line)
            Loop = 0
            for loopline in looplines:
                if loopline>=line and ((method_index+1)==len(method_lines) or loopline<method_lines[method_index+1]):
                    Loop += 1
            # if ent.parent().longname() == "C:\\Users\chenzhifei\Desktop\subjects\\avro-1.8.1\\avro-1.8.1-src\lang\java\\avro\src\main\java\org\\apache\\avro\Schema.java":
            #     print(e.simplename(), line, Loop)
            # method_name = e.simplename()
            parameters = e.parameters(False).replace(',',', ')
            LOC = e.metric(("CountLineCode",))["CountLineCode"]
            Cyclomatic = e.metric(("Cyclomatic",))["Cyclomatic"]
            FanIn = e.metric(("CountInput",))["CountInput"]
            FanOut = e.metric(("CountOutput",))["CountOutput"]

            try:
                loc += LOC
            except:
                print(e.longname())
                continue
            methods += 1

            out_result.writerow(['%s(%s)' % (e.longname(), parameters), LOC, Cyclomatic, FanIn, FanOut, Loop])
    print(loc, methods)
    print("UDB Time used:", (time.clock() - start))

def getProjectMetric(proj_name, proj_root, src_name):
    dump_project_info(proj_root, proj_name, '%s\\%s\\%s' %(parameter.SUBJECT_ROOT, proj_root, src_name))
    dump_method_metric(proj_root, proj_name, '%s\\%s\\%s' %(parameter.SUBJECT_ROOT, proj_root, src_name))


if __name__ == '__main__':
    # getProjectMetric('ivy', 'ivy-2.0.0-2009.1', 'ant-ivy-src')
    # getProjectMetric('ivy', 'ivy-2.1.0-2009.10', 'ant-ivy-src')
    # getProjectMetric('ivy', 'ivy-2.2.0-2010.9', 'ant-ivy-src')
    # getProjectMetric('ivy', 'ivy-2.3.0-2013.1', 'ant-ivy-src')
    # getProjectMetric('ivy', 'ivy-2.4.0-2014.12', 'ant-ivy-src')
    # getProjectMetric('cxf', 'cxf-3.0.1', 'apache-cxf-3.0.1-src')


    # getProjectMetric('avro', 'avro-1.3.0', 'avro-1.3.0-src')
    # getProjectMetric('avro', 'avro-1.6.0', 'avro-1.6.0-src')
    # getProjectMetric('avro', 'avro-1.8.1', 'avro-1.8.1-src')
    # #
    #
    # dump_project_info('pdfbox-2.0.0', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.0\pdfbox-2.0.0-src')
    # dump_method_metric('pdfbox-2.0.0', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.0\pdfbox-2.0.0-src')
    #
    # dump_project_info('pdfbox-1.8.4-2014.1', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.4-src\pdfbox-1.8.4')
    # dump_project_info('pdfbox-1.8.6-2014.6', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.6-2014.6\pdfbox-1.8.6-src')
    # dump_project_info('pdfbox-1.8.8-2014.12', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.8-2014.12\pdfbox-1.8.8-src')
    # dump_project_info('pdfbox-1.8.10-2015.7', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.10-2015.7\pdfbox-1.8.10-src')
    # dump_project_info('pdfbox-1.8.11-2016.1', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.11-2016.1\pdfbox-1.8.11-src')
    # dump_project_info('pdfbox-2.0.2-2016.6', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.2-2016.6\pdfbox-2.0.2-src')
    # dump_project_info('pdfbox-2.0.4-2016.12', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.4-2016.12\pdfbox-2.0.4-src')
    #
    # dump_method_metric('pdfbox-1.8.4-2014.1', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.4\pdfbox-1.8.4-src')
    # dump_method_metric('pdfbox-1.8.6-2014.6', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.6-2014.6\pdfbox-1.8.6-src')
    # dump_method_metric('pdfbox-1.8.8-2014.12', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.8-2014.12\pdfbox-1.8.8-src')
    # dump_method_metric('pdfbox-1.8.10-2015.7', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.10-2015.7\pdfbox-1.8.10-src')
    # dump_method_metric('pdfbox-1.8.11-2016.1', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-1.8.11-2016.1\pdfbox-1.8.11-src')
    # dump_method_metric('pdfbox-2.0.2-2016.6', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.2-2016.6\pdfbox-2.0.2-src')
    # dump_method_metric('pdfbox-2.0.4-2016.12', 'pdfbox', parameter.SUBJECT_ROOT + '\pdfbox-2.0.4-2016.12\pdfbox-2.0.4-src')

    # getProjectMetric('cxf', 'cxf-2.1', '\\apache-cxf-2.1-src')
    getProjectMetric('cxf', 'cxf-3.1.11-2017.4', '\\apache-cxf-3.1.11-src')