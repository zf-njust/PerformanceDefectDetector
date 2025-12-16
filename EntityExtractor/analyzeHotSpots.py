import csv
import os
import os.path
import sys
sys.path.append('..')
import parameter

def dump_hotspots_result(project):

    out_result = csv.writer(open('%s\\%s\\hotspots.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    out_result.writerow(['method', 'Time', 'Count'])
    youkit_dir = '%s\\%s\\' % (parameter.SUBJECT_ROOT, project)
    out_record = {}

    # search yourkit file from folder
    for root, dirs, files in os.walk(youkit_dir):
        for filename in files:
            if filename.find('-CPU-hot-spots.csv')!= -1:
                profile_file = csv.reader(open(os.path.join(root, filename)))
                print('processing: %s ' %(filename))
                # precess
                # record format: org.apache.pdfbox.pdfparser.PDFParser.<init>(InputStream, RandomAccess, boolean) PDFParser.java
                for record in profile_file:  # method, Time(ms), Avg. Time(ms), Own Time(ms), Count
                    if profile_file.line_num == 1:
                        continue
                    method = record[0][: -len(record[0].split(' ')[-1])-1]
                    if len(method)==0:
                        continue
                    if method in out_record.keys():
                        out_record[method] = [out_record[method][0]+int(record[1]),
                                                 out_record[method][1]+int(record[2])]
                    else:
                        out_record[method] = [int(record[1]), int(record[2])]

    ranked_full_methods = sorted(out_record.keys(), key=lambda d: out_record[d][0], reverse=True)
    for key in ranked_full_methods:
        out_result.writerow([key, out_record[key][0], out_record[key][1]])


if __name__ == '__main__':
    # dump_hotspots_result('avro-1.6.0')
    # dump_hotspots_result('ivy-2.0.0-2009.1')
    # dump_hotspots_result('pdfbox-1.8.4-2014.1')
    dump_hotspots_result('cxf-3.0.1')