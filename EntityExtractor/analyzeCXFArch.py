import csv


def get_layer(project):
    Method2Layer = {}
    layer_record = open(parameter.LAYER_SOURCE[project]).readlines()
    # layer_record = open('C:\Users\chenzhifei\Desktop\pp\pdfbox-1.8.4-2014.1\DRHCluster\pdfbox_DRH.clsx').readlines()
    layer = -1
    count = 0
    group_layer = 0
    for line in layer_record:
        if line.startswith('<group'):
            group_layer += 1
        elif line.startswith('</group>'):
            group_layer -= 1
        if group_layer==2 and line.startswith('<group name=\"L'+str(layer+1)):
            if layer!=-1 or count!=0:
                print layer, count
            layer = int(line.rstrip().lstrip('<group name=\"L').rstrip('\">'))
            count = 0
        if line.startswith('<item name='):
            method = line.rstrip().lstrip('<item name=\"').rstrip('\" />')
            if method.startswith('vro.examples.baseball'):
                method = 'a'+method
            Method2Layer[method] = layer
            count += 1
        if group_layer==2 and line.startswith('<group name="I0">'):
            print layer, count
            layer = -1
            count = 0
    print layer, count
    return Method2Layer


def get_butterfly(project):
    Method2Butterfly = {}
    space_record = csv.reader(open(parameter.BUTTERFLY_ROOT[project]+'summary_formated.csv'))
    for record in space_record:
        if space_record.line_num == 1:
            continue
        try:
            Method2Butterfly[record[1]] = [int(i) for i in record[2:]]
        except:
            print project, record
    return Method2Butterfly


def dump_arch_metric(project):
    Method2Layer = get_layer(project)
    Method2Butterfly = get_butterfly(project)
    out_record = csv.writer(open('%s\\%s\\method_arch.csv' % (parameter.SUBJECT_ROOT, project), 'wb+'))
    out_record.writerow(['method', 'layer', 'size', 'upperDepth', 'upperWidth', 'lowerDepth', 'lowerWidth'])
    for method in Method2Butterfly.keys():
        if method not in Method2Layer.keys():
            print 'Error in Layer', method
    for method in Method2Layer.keys():
        layer = Method2Layer[method]
        if method not in Method2Butterfly.keys():
            print 'Error in Butterfly', method
        else:
            out_record.writerow([method, layer] + Method2Butterfly[method])

if __name__ == '__main__':
    dump_arch_metric('cxf-3.0.1')

    # dump_arch_metric('avro-1.3.0')
    # dump_arch_metric('avro-1.6.0')
    # dump_arch_metric('avro-1.8.1')

    # dump_arch_metric('ivy-2.0.0-2009.1')
    # dump_arch_metric('ivy-2.1.0-2009.10')
    # dump_arch_metric('ivy-2.2.0-2010.9')
    # dump_arch_metric('ivy-2.3.0-2013.1')
    # dump_arch_metric('ivy-2.4.0-2014.12')

    # dump_arch_metric('pdfbox-1.8.4-2014.1')
    # dump_arch_metric('pdfbox-1.8.6-2014.6')
    # dump_arch_metric('pdfbox-1.8.8-2014.12')
    # dump_arch_metric('pdfbox-1.8.10-2015.7')
    # dump_arch_metric('pdfbox-1.8.11-2016.1')
    # dump_arch_metric('pdfbox-2.0.0')
    # dump_arch_metric('pdfbox-2.0.2-2016.6')
    # dump_arch_metric('pdfbox-2.0.4-2016.12')
