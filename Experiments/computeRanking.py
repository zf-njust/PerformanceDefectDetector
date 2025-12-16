import csv
import os
import sys
sys.path.append('..')
import parameter
import time

MIN_NORMALIZED = 0.0000000000001

def normalized_metric(metric, metrics_list):
    if metric==min(metrics_list):
        return MIN_NORMALIZED
    else:
        return 1.0*(metric-min(metrics_list))/(max(metrics_list)-min(metrics_list))


#formulas elements: Layer, Size, Depth(upperDepth+LowerDepth), Width(upperWidth+lowerWidth),
#                   LOC, Cyclomatic, FanIn, FanOut,
#                   Time, OwnTime, Count
def getRankedFullMethods(project, version, formulas):
    start = time.clock()
    metric_file = csv.reader(open('%s\\%s\method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, version)))
    # 0:'method',
    # 1:'Layer', 2:'Size', 3:'upperDepth', 4:'upperWidth', 5:'lowerDepth', 6:'lowerWidth',
    # 7:'LOC', 8:'Cyclomatic', 9:'FanIn', 10:'FanOut', 11:'Loop,
    # 12:'Time', 13:'OwnTime', 14:'Count'
    method2metrics = {}
    method2normalizedmetrics = {}
    method2score = {}
    layer_record, size_record, depth_record, width_record, \
    loc_record, cyclomatic_record, fanin_record, fanout_record, loop_record,\
    time_record, owntime_record, count_record = [[], [], [], [], [], [], [], [], [], [], [], []]
    for record in metric_file:
        if metric_file.line_num==1:
            continue
        method2metrics[record[0]] = [int(record[1]), int(record[2]), int(record[3])+int(record[5]),
                                     int(record[4])+int(record[6]), int(record[7]), int(record[8]), int(record[9]),
                                     int(record[10]), int(record[11]), int(record[12]), int(record[13]), int(record[14])]
        layer_record.append(int(record[1]))
        size_record.append(int(record[2]))
        depth_record.append(int(record[3])+int(record[5]))
        width_record.append(int(record[4])+int(record[6]))
        loc_record.append(int(record[7]))
        cyclomatic_record.append(int(record[8]))
        fanin_record.append(int(record[9]))
        fanout_record.append(int(record[10]))
        loop_record.append(int(record[11]))
        time_record.append(int(record[12]))
        owntime_record.append(int(record[13]))
        count_record.append(int(record[14]))
    for method in method2metrics.keys():
        metrics = method2metrics[method]
        # print metrics
        Layer = metrics[0]
        maxlayer = max(layer_record)+1
        if Layer==-1:
            Layer = MIN_NORMALIZED
        else:
            Layer = 1-1.0*Layer/maxlayer
        Size = normalized_metric(metrics[1], size_record)
        Depth = normalized_metric(metrics[2], depth_record)
        Width = normalized_metric(metrics[3], width_record)
        LOC = normalized_metric(metrics[4], loc_record)
        Cyclomatic = normalized_metric(metrics[5], cyclomatic_record)
        FanIn = normalized_metric(metrics[6], fanin_record)
        FanOut = normalized_metric(metrics[7], fanout_record)
        Loop = normalized_metric(metrics[8], loop_record)
        # Time = normalized_metric(metrics[8]/metrics[10], time_record)
        # OwnTime = normalized_metric(metrics[9]/metrics[10], owntime_record)
        Time = normalized_metric(metrics[9], time_record)
        OwnTime = normalized_metric(metrics[10], owntime_record)
        Count = normalized_metric(metrics[11], count_record)
        method2normalizedmetrics[method] = [Layer,Size,Depth,Width,LOC,Cyclomatic,FanIn,FanOut,Loop,Time,OwnTime,Count]
        score = eval(formulas)
        method2score[method] = score


    ranked_file = csv.writer(open(parameter.DATA_ROOT + '\\%s\\score_%s.csv' % (project, version), 'wb+'))
    ranked_file.writerow(['method','Layer','Size','Depth','Width','LOC','Cyclomatic','FanIn','FanOut', 'Loop',
                          'Time','OwnTime','Count', 'N_Layer','N_Size','N_Depth','N_Width',
                          'N_LOC','N_Cyclomatic','N_FanIn','N_FanOut','N_Loop',
                          'N_Time','N_OwnTime','N_Count',
                          'score'])
    ranked_full_methods = sorted(method2score.keys(), key=lambda d: method2score[d], reverse=True)

    for method in ranked_full_methods:
        metrics = method2metrics[method]
        normalizedmetrics = method2normalizedmetrics[method]
        ranked_file.writerow([method]+metrics+normalizedmetrics+[method2score[method]])

    print("Ranking Time used:", project, version, (time.clock() - start))
    # print ranked_full_methods
    return ranked_full_methods, method2score