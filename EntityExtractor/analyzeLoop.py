import csv
import os
import sys
import subprocess
sys.path.append('..')
import parameter


def copyFile(dest, source):
    dest_file = open(dest, 'w')
    src_file = open(source)
    src = src_file.read()
    dest_file.write(src)
    dest_file.close()
    src_file.close()


def getMethodLoops(project):
    out_path = '%s\\%s\\method_loop.csv' % (parameter.SUBJECT_ROOT, project)
    out_result = csv.writer(open(out_path, 'wb+'))
    out_result.writerow(['method', 'loop'])
    os.chdir(parameter.SOOT_JAR_ROOT)
    project_dir = parameter.SOURECE_ROOT[project]
    names = []
    for root, dirs, files in os.walk(project_dir):
        for name in files:
            filename = os.path.join(root, name)

            if filename.endswith('.java')and filename.find('test')==-1 and filename.find('Test')==-1 and name.endswith('.java'):
                if name in names:
                    print name
                else:
                    names.append(name)
            #
            # if filename.endswith('.class') and filename.find('test')==-1 and filename.find('Test')==-1:
            #     print filename
            #     copyFile('C:\Users\chenzhifei\Desktop\workspace\MethodAnalyser\\bin\\%s.class' %name.strip('.class'), filename)
            #     output = subprocess.Popen('java -jar soot-loop.jar %s' %name.strip('.class'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #     for line in output.stdout.readlines():
            #         print line


if __name__ == '__main__':

    getMethodLoops('avro-1.8.1')
    # getMethodLoops('avro-1.6.0')
    # getMethodLoops('avro-1.3.0')
    #
    # getMethodLoops('ivy-2.0.0-2009.1')
    # getMethodLoops('ivy-2.1.0-2009.10')
    # getMethodLoops('ivy-2.2.0-2010.9')
    # getMethodLoops('ivy-2.3.0-2013.1')
    # getMethodLoops('ivy-2.4.0-2014.12')
    #
    # getMethodLoops('pdfbox-1.8.4-2014.1')
    # getMethodLoops('pdfbox-1.8.6-2014.6')
    # getMethodLoops('pdfbox-1.8.8-2014.12')
    # getMethodLoops('pdfbox-1.8.10-2015.7')
    # getMethodLoops('pdfbox-1.8.11-2016.1')
    # getMethodLoops('pdfbox-2.0.0')
    # getMethodLoops('pdfbox-2.0.2-2016.6')
    # getMethodLoops('pdfbox-2.0.4-2016.12')

    # copyFile(parameter.SOOT_JAR_ROOT+'\\temp.java', 'C:\Users\chenzhifei\Desktop\java\TestInvoke.java')