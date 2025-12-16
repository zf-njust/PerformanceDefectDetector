#generate evo tests

import os
import re


def traverseRoot(rootDir):
    os.chdir(rootDir)
    flag = False
    for root, dirs, files in os.walk(rootDir):
        for d in dirs:
            if d != 'classes':
                continue
            subrootDir = os.path.join(root, d)
            if not subrootDir.endswith('\\target\classes'):
                continue
            print subrootDir
            if subrootDir == 'C:\Users\chenzhifei\Desktop\subjects\cxf-3.0.1\\apache-cxf-3.0.1\\testutils\\target\classes':
                flag = True
            if flag:
                output = os.system('java -jar C:\Users\chenzhifei\Desktop\evosuite-lib\evosuite-1.0.3.jar -criterion method  -continuous  execute -Dctg_export_folder=evo -Dctg_time_per_class=1 -target %s' %subrootDir)



if __name__ == '__main__':
    # traverseRoot('C:\Users\chenzhifei\Desktop\subjects\cxf-2.1\\apache-cxf-2.1')
    traverseRoot('C:\Users\chenzhifei\Desktop\subjects\cxf-3.0.1\\apache-cxf-3.0.1')