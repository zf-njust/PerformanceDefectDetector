
FORMULAS = [
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',

    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.3 + 0.7 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',

    '((Size+Depth+Width)/3) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Depth+Width)/3) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Size+Width)/3) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Size+Depth)/3) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    #
    # '((Layer+Size+Depth+Width)/4) * ((OwnTime+Count)/2) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+Count)/2) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime)/2) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    #
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((Cyclomatic+FanIn+FanOut+Loop)/4)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+FanIn+FanOut+Loop)/4)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanOut+Loop)/4)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+Loop)/4)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.5 + 0.5 * ((LOC+Cyclomatic+FanIn+FanOut)/4)',

    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.6 + 0.4 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * 0.7 + 0.3 * ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    #
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime)/2) * ((LOC+Cyclomatic+FanIn+FanOut)/4)',
    # '0.33*((Layer+Size+Depth+Width)/4) + 0.33*((Time+OwnTime+Count)/3) + 0.33*((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '(Time+OwnTime+Count)/3',
    # '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3)',
    '((Layer+Size+Depth+Width)/4) + ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '((Time+OwnTime+Count)/3) + ((LOC+Cyclomatic+FanIn+FanOut+Loop)/5)',
    # '(LOC+Cyclomatic+FanIn+FanOut+Loop)/5',
    # 'Time',
    # 'OwnTime'
]


SUBJECT_ROOT = 'C:\\Users\\chenzhifei\\Desktop\\subjects'
DATA_ROOT = 'C:\\Users\chenzhifei\Desktop\source\subjects'

# LOG_ROOT = {'pdfbox': SUBJECT_ROOT+'\pdfbox-1.8.4-2014.1\git\\'}
GIT_ROOT = {'pdfbox': SUBJECT_ROOT+'\pdfbox-1.8.4-2014.1\git\\pdfbox',
            'avro': SUBJECT_ROOT+'\\avro-1.8.1\git\\avro',
            'ivy': SUBJECT_ROOT + '\\ivy-2.0.0-2009.1\git\\ant-ivy',
            'cxf': SUBJECT_ROOT + '\\cxf-3.1.11-2017.4\git\cxf'}


SOURECE_ROOT = {
    'avro-1.3.0': SUBJECT_ROOT + '\\avro-1.3.0\\avro-1.3.0-src',
    'avro-1.6.0': SUBJECT_ROOT + '\\avro-1.6.0\\avro-1.6.0-src',
    'avro-1.8.1': SUBJECT_ROOT + '\\avro-1.8.1\\avro-1.8.1',
    'ivy-2.0.0-2009.1': SUBJECT_ROOT + '\\ivy-2.0.0-2009.1\\ant-ivy-src',
    'ivy-2.1.0-2009.10': SUBJECT_ROOT + '\\ivy-2.1.0-2009.10\\ant-ivy-src',
    'ivy-2.2.0-2010.9': SUBJECT_ROOT + '\\ivy-2.2.0-2010.9\\ant-ivy-src',
    'ivy-2.3.0-2013.1': SUBJECT_ROOT + '\\ivy-2.3.0-2013.1\\ant-ivy-src',
    'ivy-2.4.0-2014.12': SUBJECT_ROOT + '\\ivy-2.4.0-2014.12\\ant-ivy-src',
    'pdfbox-1.8.4-2014.1': SUBJECT_ROOT + '\\pdfbox-1.8.4-2014.1\pdfbox-1.8.4-src\pdfbox-1.8.4',
    'pdfbox-1.8.6-2014.6': SUBJECT_ROOT + '\\pdfbox-1.8.6-2014.6\pdfbox-1.8.6-src',
    'pdfbox-1.8.8-2014.12': SUBJECT_ROOT + '\\pdfbox-1.8.8-2014.12\pdfbox-1.8.8-src',
    'pdfbox-1.8.10-2015.7': SUBJECT_ROOT + '\\pdfbox-1.8.10-2015.7\pdfbox-1.8.10-src',
    'pdfbox-1.8.11-2016.1': SUBJECT_ROOT + '\\pdfbox-1.8.11-2016.1\pdfbox-1.8.11-src',
    'pdfbox-2.0.0': SUBJECT_ROOT + '\\pdfbox-2.0.0\pdfbox-2.0.0-src',
    'pdfbox-2.0.2-2016.6': SUBJECT_ROOT + '\\pdfbox-2.0.2-2016.6\pdfbox-2.0.2-src',
    'pdfbox-2.0.4-2016.12': SUBJECT_ROOT + '\\pdfbox-2.0.4-2016.12\pdfbox-2.0.4-src'
}

# VERSIONS = {
#     'pdfbox':('pdfbox-1.8.4-2014.1', 'pdfbox-1.8.6-2014.6', 'pdfbox-1.8.8-2014.12',
#               'pdfbox-1.8.10-2015.7', 'pdfbox-1.8.11-2016.1', 'pdfbox-2.0.2-2016.6', 'pdfbox-2.0.4-2016.12')
# }

ISSUE_ROOT = {
    'pdfbox': DATA_ROOT + '\pdfbox\issues\\',
    'avro': DATA_ROOT + '\\avro\issues\\',
    'ivy': DATA_ROOT + '\\ivy\issues\\',
    'cxf': DATA_ROOT + '\\cxf\issues\\',
}

ISSUE_PATHS = {
    'pdfbox': (ISSUE_ROOT['pdfbox']+'ASF JIRA (1).csv', ISSUE_ROOT['pdfbox']+'ASF JIRA (2).csv',
               ISSUE_ROOT['pdfbox']+'ASF JIRA (3).csv', ISSUE_ROOT['pdfbox']+'ASF JIRA (4).csv'),
    'avro': (ISSUE_ROOT['avro']+'ASF JIRA.csv', ISSUE_ROOT['avro']+'ASF JIRA(1).csv',
             ISSUE_ROOT['avro'] + 'ASF JIRA(2).csv'),
    'ivy': (ISSUE_ROOT['ivy']+'ASF JIRA.csv', ISSUE_ROOT['ivy']+'ASF JIRA (1).csv'),
    'cxf': (ISSUE_ROOT['cxf']+'ASF JIRA.csv', ISSUE_ROOT['cxf']+'ASF JIRA (1).csv',
            ISSUE_ROOT['cxf'] + 'ASF JIRA (2).csv', ISSUE_ROOT['cxf'] + 'ASF JIRA (3).csv',
            ISSUE_ROOT['cxf'] + 'ASF JIRA (4).csv', ISSUE_ROOT['cxf'] + 'ASF JIRA (5).csv',
            ISSUE_ROOT['cxf'] + 'ASF JIRA (6).csv', ISSUE_ROOT['cxf'] + 'ASF JIRA (7).csv',),
}

ISSUE_PATH = {
    'pdfbox': ISSUE_ROOT['pdfbox']+'all_issues.csv',
    'avro': ISSUE_ROOT['avro']+'all_issues.csv',
    'ivy': ISSUE_ROOT['ivy']+'all_issues.csv',
    'cxf': ISSUE_ROOT['cxf']+'all_issues.csv'
}

KEYWORDS_ISSUE_PATH = {
    'pdfbox': ISSUE_ROOT['pdfbox']+'keywords_issues.csv',
    'avro': ISSUE_ROOT['avro']+'keywords_issues.csv',
    'ivy': ISSUE_ROOT['ivy']+'keywords_issues.csv',
    'cxf': ISSUE_ROOT['cxf']+'keywords_issues.csv',
}

CHANGE_JAR_ROOT = 'C:\\Users\chenzhifei\Desktop\sealuzh-tools-changedistiller-feee5be3724a\out\\artifacts\changedistiller_jar'
SOOT_JAR_ROOT = 'C:\\Users\chenzhifei\Desktop'

GIT_SHOW_DIFFERENT_FILES_LIST_COMMAND = "git show --pretty=\"format:\" --name-only "

ORIGIN_FILE = 'C:\\Users\chenzhifei\Desktop\source\SubjectProfiler\\useless\\file_origin.java'
CURRENT_FILE = 'C:\\Users\chenzhifei\Desktop\source\SubjectProfiler\\useless\\file_current.java'

LAYER_SOURCE = {
    'avro-1.3.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.3.0-method.clxs',
    'avro-1.6.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.6.0-method.clxs',
    'avro-1.8.1': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.8.1-method.clxs',
    'ivy-2.0.0-2009.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.0.0-method.clxs',
    'ivy-2.1.0-2009.10': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.1.0-method.clxs',
    'ivy-2.2.0-2010.9': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.2.0-method.clxs',
    'ivy-2.3.0-2013.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.3.0-method.clxs',
    'ivy-2.4.0-2014.12': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.4.0-method.clxs',
    'pdfbox-1.8.4-2014.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.4-method.clxs',
    'pdfbox-1.8.6-2014.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.6-method.clxs',
    'pdfbox-1.8.8-2014.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.8-method.clxs',
    'pdfbox-1.8.10-2015.7': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.10-method.clxs',
    'pdfbox-1.8.11-2016.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.11-method.clxs',
    'pdfbox-2.0.0': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.0-method.clxs',
    'pdfbox-2.0.2-2016.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.2-method.clxs',
    'pdfbox-2.0.4-2016.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.4-method.clxs',
    'cxf-3.0.1': DATA_ROOT + '\\cxf\cxf-static-analysis\cxf-3.0.1-method.clxs'
}

STATIC_CALL_FILE = {
    'avro-1.3.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.3.0-method-calls.txt',
    'avro-1.6.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.6.0-method-calls.txt',
    'avro-1.8.1': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.8.1-method-calls.txt',
    'ivy-2.0.0-2009.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.0.0-method-calls.txt',
    'ivy-2.1.0-2009.10': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.1.0-method-calls.txt',
    'ivy-2.2.0-2010.9': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.2.0-method-calls.txt',
    'ivy-2.3.0-2013.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.3.0-method-calls.txt',
    'ivy-2.4.0-2014.12': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.4.0-method-calls.txt',
    'pdfbox-1.8.4-2014.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.4-method.dsm',
    'pdfbox-1.8.6-2014.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.6-method-calls.txt',
    'pdfbox-1.8.8-2014.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.8-method-calls.txt',
    'pdfbox-1.8.10-2015.7': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.10-method-calls.txt',
    'pdfbox-1.8.11-2016.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.11-method-calls.txt',
    'pdfbox-2.0.0': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.0-method-calls.txt',
    'pdfbox-2.0.2-2016.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.2-method-calls.txt',
    'pdfbox-2.0.4-2016.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.4-method-calls.txt',
    'cxf-3.0.1': DATA_ROOT + '\\cxf\cxf-static-analysis\cxf-3.0.1-method-calls.txt'

}

VERSION_DATE = {
    'avro-1.3.0': '2010-05-10 21:58:52',
    'avro-1.6.0': '2011-11-01 18:10:51',
    'avro-1.8.1': '2016-05-14 17:38:52',
    'ivy-2.0.0-2009.1': '2009-01-18 22:08:59',
    'ivy-2.1.0-2009.10': '2009-09-25 22:18:07',
    'ivy-2.2.0-2010.9': '2010-09-23 21:53:29',
    'ivy-2.3.0-2013.1': '2013-01-21 20:12:28',
    'ivy-2.4.0-2014.12': '2014-12-13 16:58:00',
    'pdfbox-1.8.4-2014.1': '2014-01-27 17:58:00',
    'pdfbox-1.8.6-2014.6': '2014-06-19 11:52:20',
    'pdfbox-1.8.8-2014.12': '2014-12-24 13:19:44',
    'pdfbox-1.8.10-2015.7': '2015-07-18 15:24:08',
    'pdfbox-1.8.11-2016.1': '2016-01-14 17:44:20',
    'pdfbox-2.0.0': '2016-03-14 17:22:09',
    'pdfbox-2.0.2-2016.6': '2016-06-06 17:14:02',
    'pdfbox-2.0.4-2016.12': '2016-12-12 17:36:09',
    'cxf-3.0.1': '2010-07-15 14:16:03',
    'cxf-3.1.11-2017.4': '2017-04-05 16:02:48'
}

BUTTERFLY_ROOT = {
    'avro-1.3.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.3.0-allButterFly\\',
    'avro-1.6.0': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.6.0-allButterFly\\',
    'avro-1.8.1': DATA_ROOT + '\\avro\\avro-static-analysis\\avro-1.8.1-allButterFly\\',
    'ivy-2.0.0-2009.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.0.0-allButterFly\\',
    'ivy-2.1.0-2009.10': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.1.0-allButterFly\\',
    'ivy-2.2.0-2010.9': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.2.0-allButterFly\\',
    'ivy-2.3.0-2013.1': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.3.0-allButterFly\\',
    'ivy-2.4.0-2014.12': DATA_ROOT + '\\ivy\\ivy-static-analysis\\ivy-2.4.0-allButterFly\\',
    'pdfbox-1.8.4-2014.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.4-allButterFly\\',
    'pdfbox-1.8.6-2014.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.6-allButterFly\\',
    'pdfbox-1.8.8-2014.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.8-allButterFly\\',
    'pdfbox-1.8.10-2015.7': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.10-allButterFly\\',
    'pdfbox-1.8.11-2016.1': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-1.8.11-allButterFly\\',
    'pdfbox-2.0.0': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.0-allButterFly\\',
    'pdfbox-2.0.2-2016.6': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.2-allButterFly\\',
    'pdfbox-2.0.4-2016.12': DATA_ROOT + '\\pdfbox\pdfbox-static-analysis\pdfbox-2.0.4-allButterFly\\',
    'cxf-3.0.1': DATA_ROOT + '\\cxf\cxf-static-analysis\cxf-3.0.1-allButterFly\\'
}