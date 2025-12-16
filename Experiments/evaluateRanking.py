import sys
sys.path.append('..')
import parameter
import csv
import datetime
import computeRanking
import computeSpace

TOTAL_REF_METHODS = {
    'avro': 21,
    'ivy':61,
    'pdfbox':621
}

TOTAL_COV_METHODS = {
    'avro': 659,
    'ivy':2174,
    'pdfbox':4164
}

TOTAL_METHODS = {
    'avro': 1238,
    'ivy':4673,
    'pdfbox':8352
}

def NumberofMethodsSummary(project, version):
    print '\n'
    print project, version
    class_record = csv.reader(open('%s\%s\project_info.csv' % (parameter.SUBJECT_ROOT, version)))
    VersionDate = datetime.datetime.strptime(parameter.VERSION_DATE[version], "%Y-%m-%d %H:%M:%S")
    Path2Class = {}
    for record in class_record:
        if class_record.line_num == 1:
            continue
        Path2Class[record[1]] = record[2]+'.'+record[0] #x/z/a.java -> XX.XX.a
    Method2Issues = {}
    Issues2Date = {}
    refactored_methods_record = csv.reader(open(parameter.DATA_ROOT + '\\%s\\all_refactored_methods.csv' % project))
    for record in refactored_methods_record:
        if refactored_methods_record.line_num==1:
            continue
        date = datetime.datetime.strptime(record[4], "%Y-%m-%d %H:%M:%S")
        if record[2] not in Issues2Date.keys():
            Issues2Date[record[2]] = date
        elif date > Issues2Date[record[2]]:
            Issues2Date[record[2]] = date
        path = record[0].replace('/', '\\')
        if path not in Path2Class.keys():
            continue
        full_method = Path2Class[path]+'.'+record[1] # XX.XX.a.ff(x,x)
        simple_method = full_method[: -len(record[1].split('(')[-1])-1]
        if simple_method not in Method2Issues.keys():
            Method2Issues[simple_method] = [record[2]]
        elif record[2] not in Method2Issues[simple_method]:
            Method2Issues[simple_method].append(record[2])
    # print all_issues
    print 'all issues: %d' %(len(Issues2Date.keys()))


    Max_Methods = []
    Max_Issues = []
    Total_Methods = 0
    all_methods_dev_record = csv.reader(open('%s\\%s\\method_all_metrics_dev.csv' % (parameter.SUBJECT_ROOT, version)))
    for record in all_methods_dev_record:
        if all_methods_dev_record.line_num==1:
            continue
        Total_Methods += 1
        exist_method = record[0][: -len(record[0].split('(')[-1]) - 1]
        if exist_method in Method2Issues.keys():
            for issue in Method2Issues[exist_method]:
                if Issues2Date[issue] > VersionDate:
                    if issue not in Max_Issues:
                        Max_Issues.append(issue)
                    # if exist_method not in Max_Methods:
                    Max_Methods.append(exist_method)
                    # else:
                    #     print exist_method, issue
    print Max_Issues
    print 'total methods: %d, refactored methods: %d, density: %f, all covered issues: %d' \
          %(Total_Methods, len(Max_Methods), 1.0*len(Max_Methods)/Total_Methods, len(Max_Issues))


    Dev_Methods = []
    Dev_Issues = []
    Total_Dev_Methods = 0
    dev_methods_record = csv.reader(open('%s\\%s\\method_valid_metrics_dev.csv' % (parameter.SUBJECT_ROOT, version)))
    for record in dev_methods_record:
        if dev_methods_record.line_num==1:
            continue
        Total_Dev_Methods += 1
        dev_method = record[0][: -len(record[0].split('(')[-1]) - 1]
        if dev_method in Method2Issues.keys():
            Dev_Methods.append(dev_method)
            for issue in Method2Issues[dev_method]:
                if issue not in Dev_Issues:
                    if Issues2Date[issue] > VersionDate:
                        Dev_Issues.append(issue)
                    # else:
                    #     print dev_method, issue
    print 'total dev methods: %d, dev covered issues: %d' %(Total_Dev_Methods, len(Dev_Issues))

    Dev_Evo_Methods = []
    Dev_Evo_Issues = []
    Total_Dev_Evo_Methods = 0
    dev_evo_methods_record = csv.reader(open('%s\\%s\\method_valid_metrics_dev_evo.csv' % (parameter.SUBJECT_ROOT, version)))
    for record in dev_evo_methods_record:
        if dev_evo_methods_record.line_num==1:
            continue
        Total_Dev_Evo_Methods += 1
        dev_evo_method = record[0][: -len(record[0].split('(')[-1]) - 1]
        if dev_evo_method in Method2Issues.keys():
            Dev_Evo_Methods.append(dev_evo_method)
            for issue in Method2Issues[dev_evo_method]:
                if issue not in Dev_Evo_Issues:
                    if Issues2Date[issue] > VersionDate:
                        Dev_Evo_Issues.append(issue)
                    # else:
                    #     print dev_evo_method, issue
    print 'total dev+evo methods: %d, dev+evo covered issues: %d' %(Total_Dev_Evo_Methods, len(Dev_Evo_Issues))

    return Method2Issues, Total_Methods, Max_Issues


def evaluateRankedFullMethods(project, Ranked_Full_Methods, Method2Issues, Total_Methods, Max_Issues):
    print '................evaluating ranked methods.......................'
    out_record = csv.writer(open('evaluation_result.csv', 'wb+'))
    out_record.writerow(['method', 'issue'])

    cover_record = csv.writer(open(project+'_method_cover.csv', 'wb+'))

    # Top5Number = int(Total_Methods*0.05)
    Top5Number = 110
    Top10Number = 166
    Top20Number = 126
    IssuesbyTop5 = []
    IssuesbyTop10 = []
    IssuesbyTop20 = []
    CoveredIssues = []
    RefMethodsbyTop5 = []
    RefMethodsbyTop10 = []
    RefMethodsbyTop20 = []
    CoveredRefMethods = []
    count = 0
    for full_method in Ranked_Full_Methods:
        count += 1
        simple_method = full_method[: -len(full_method.split('(')[-1]) - 1]

        if hasOtherMethod(full_method, Ranked_Full_Methods):
            cover_record.writerow([count, len(CoveredRefMethods)])
            continue
        # for m in Ranked_Full_Methods:
        #     sm = m[: -len(m.split('(')[-1]) - 1]
        #     if simple_method==sm and m!=full_method:
        #         continue

        valid_issues = []

        if simple_method in Method2Issues.keys():

            for issue in Method2Issues[simple_method]:
                # change condition here!!!
                if issue not in Max_Issues:
                    # print issue
                    continue
                # print count, issue, full_method
                if issue not in CoveredIssues:
                    CoveredIssues.append(issue)
                valid_issues.append(issue)
                if full_method not in CoveredRefMethods:
                    CoveredRefMethods.append(full_method)
                if count <= Top5Number:
                    if issue not in IssuesbyTop5:
                        IssuesbyTop5.append(issue)
                    if full_method not in RefMethodsbyTop5:
                        # print count, full_method, issue
                        RefMethodsbyTop5.append(full_method)
                if count <= Top10Number:
                    if issue not in IssuesbyTop10:
                        IssuesbyTop10.append(issue)
                    if full_method not in RefMethodsbyTop10:
                        RefMethodsbyTop10.append(full_method)
                if count <= Top20Number:
                    if issue not in IssuesbyTop20:
                        IssuesbyTop20.append(issue)
                    if full_method not in RefMethodsbyTop20:
                        RefMethodsbyTop20.append(full_method)
        out_record.writerow([full_method, ', '.join(valid_issues)])
        cover_record.writerow([count, len(CoveredRefMethods)])
    # print 'total covered issues: %d, 5(%d) covered issues: %d, 10(%d) covered issues: %d, 20(%d) covered issues: %d' \
    #       %(len(CoveredIssues), Top5Number, len(IssuesbyTop5), Top10Number, len(IssuesbyTop10),Top20Number, len(IssuesbyTop20))
    for i in range(count+1, TOTAL_COV_METHODS[project]+1):
        cover_record.writerow([i, len(CoveredRefMethods)])

    # cover_record.writerow(
    #     [TOTAL_COV_METHODS[project], TOTAL_METHODS[project], len(CoveredRefMethods), TOTAL_REF_METHODS[project]])

    print 'total covered methods: %d, Top 5 covered methods: %d/%d=%f, Top 10 covered methods: %d/%d=%f, Top 20 covered methods: %d/%d=%f' \
          % (len(CoveredRefMethods), Top5Number, len(RefMethodsbyTop5), 1.0*len(RefMethodsbyTop5)/Top5Number,
             Top10Number, len(RefMethodsbyTop10), 1.0*len(RefMethodsbyTop10)/Top10Number,
             Top20Number, len(RefMethodsbyTop20), 1.0*len(RefMethodsbyTop20)/Top20Number)


def evaluateRankedMethodSpace(Ranked_Full_Methods, Method2Space, Method2Pattern, Method2Issues, Total_Methods, Max_Issues):
    print '................evaluating ranked methods with space.......................'
    out_record = csv.writer(open('evaluation_result.csv', 'wb+'))
    out_record.writerow(['method', 'pattern', 'space', 'target', 'issue'])

    Top5Number = int(Total_Methods * 0.05)
    Top10Number = int(Total_Methods * 0.1)
    Top20Number = int(Total_Methods * 0.2)
    IssuesbyTop5 = []
    IssuesbyTop10 = []
    IssuesbyTop20 = []
    CoveredIssues = []
    SpaceMethodsbyTop5 = []
    SpaceMethodsbyTop10 = []
    SpaceMethodsbyTop20 = []
    SpaceRefMethodsbyTop5 = []
    SpaceRefMethodsbyTop10 = []
    SpaceRefMethodsbyTop20 = []
    RefMethodsbyTop5 = []
    RefMethodsbyTop10 = []
    RefMethodsbyTop20 = []
    CoveredRefMethods = []
    count = 0
    spacecount = 0
    for seed in Ranked_Full_Methods:
        count += 1
        solved_targets = []
        solved_issues = []
        patterns = []
        space = []

        if seed in Method2Space.keys():
            patterns = Method2Pattern[seed]
            space = Method2Space[seed]
            for m in Method2Space[seed]:
                spacecount += 1
                # if m in Method2Space.keys():
                #     space.extend([i for i in Method2Space[m] if i not in space])
                if count <= Top5Number:
                    if m not in SpaceMethodsbyTop5:
                        SpaceMethodsbyTop5.append(m)
                if count <= Top10Number:
                    if m not in SpaceMethodsbyTop10:
                        SpaceMethodsbyTop10.append(m)
                if count <= Top20Number:
                    if m not in SpaceMethodsbyTop20:
                        SpaceMethodsbyTop20.append(m)
            candidates = space
        else:
            candidates = [seed]

        for full_method in candidates:
            simple_method = full_method[: -len(full_method.split('(')[-1]) - 1]
            if simple_method in Method2Issues.keys():
                for issue in Method2Issues[simple_method]:
                    # change condition here!!!
                    if issue not in Max_Issues:
                        continue
                    solved_targets.append(full_method)
                    solved_issues.append(issue)
                    # print count, issue, full_method, Ranked_Full_Methods.index(full_method)+1
                    if issue not in CoveredIssues:
                        CoveredIssues.append(issue)
                    if full_method not in CoveredRefMethods:
                        CoveredRefMethods.append(full_method)
                    if count <= Top5Number:
                        if issue not in IssuesbyTop5:
                            IssuesbyTop5.append(issue)
                        if full_method not in RefMethodsbyTop5:
                            RefMethodsbyTop5.append(full_method)
                        if seed in Method2Space.keys():
                            if full_method not in SpaceRefMethodsbyTop5:
                                SpaceRefMethodsbyTop5.append(full_method)
                    if count <= Top10Number:
                        if issue not in IssuesbyTop10:
                            IssuesbyTop10.append(issue)
                        if full_method not in RefMethodsbyTop10:
                            RefMethodsbyTop10.append(full_method)
                        if seed in Method2Space.keys():
                            if full_method not in SpaceRefMethodsbyTop10:
                                SpaceRefMethodsbyTop10.append(full_method)
                    if count <= Top20Number:
                        if issue not in IssuesbyTop20:
                            IssuesbyTop20.append(issue)
                        if full_method not in RefMethodsbyTop20:
                            RefMethodsbyTop20.append(full_method)
                        if seed in Method2Space.keys():
                            if full_method not in SpaceRefMethodsbyTop20:
                                SpaceRefMethodsbyTop20.append(full_method)
        out_record.writerow([seed, ', '.join(patterns), ', '.join(space), ', '.join(solved_targets), ', '.join(solved_issues)])
    print 'total covered issues: %d, 5(%d) covered issues: %d, 10(%d) covered issues: %d, 20(%d) covered issues: %d' \
          % (len(CoveredIssues), Top5Number, len(IssuesbyTop5), Top10Number, len(IssuesbyTop10), Top20Number,
             len(IssuesbyTop20))
    print 'total covered methods: %d, 5(%d) covered methods: %d, 10(%d) covered methods: %d, 20(%d) covered methods: %d' \
          % (len(CoveredRefMethods), Top5Number, len(RefMethodsbyTop5),
             Top10Number, len(RefMethodsbyTop10),
             Top20Number, len(RefMethodsbyTop20))
    print 'space number: %d, Top 5: %d/%d, Top 10: %d/%d, Top 20: %d/%d' \
          % (spacecount, len(SpaceMethodsbyTop5), len(SpaceRefMethodsbyTop5),
             len(SpaceMethodsbyTop10), len(SpaceRefMethodsbyTop10),
             len(SpaceMethodsbyTop20), len(SpaceRefMethodsbyTop20))


#formulas elements: Layer, Size, Depth(upperDepth+LowerDepth), Width(upperWidth+lowerWidth),
#                   LOC, Cyclomatic, FanIn, FanOut,
#                   Time, OwnTime, Count
# FORMULAS = [
#     '((Layer+Size+Depth+Width)/4) * ((Time+OwnTime+Count)/3) * ((LOC+Cyclomatic+FanIn+FanOut)/4)',
#     '0.4*((Layer+Size+Depth+Width)/4) + 0.4*((Time+OwnTime+Count)/3) + 0.2*((LOC+Cyclomatic+FanIn+FanOut)/4)',
#     '(Time+OwnTime+Count)/3'
# ]


def hasOtherMethod(full_method, full_method_list):
    if full_method not in full_method_list:
        return False
    index = full_method_list.index(full_method)
    simple_method = full_method[: -len(full_method.split('(')[-1]) - 1]
    if index==len(full_method_list)-1:
        return False
    for i in range(index+1, len(full_method_list)):
        fm = full_method_list[i]
        sm = fm[: -len(fm.split('(')[-1]) - 1]
        if sm==simple_method:
            return True
    return False



def evaluateRankedOnlySpace(project, Space2Score, Method2Pattern, Method2Space, Method2Issues, Total_Methods, Max_Issues):
    print '................evaluating space.......................'
    out_record = csv.writer(open(project+'_evaluation_result_space.csv', 'wb+'))
    out_record.writerow(['method', 'pattern', 'space', 'score', 'target', 'issue'])

    cover_record = csv.writer(open(project+'_method_cover.csv', 'wb+'))


    # Top5Number = int(Total_Methods*0.05)
    Top25Number = 25
    Top50Number = 50
    Top100Number = 100
    Top150Number = 150
    IssuesbyTop25 = []
    IssuesbyTop50 = []
    IssuesbyTop100 = []
    IssuesbyTop150 = []
    CoveredIssues = []
    SpaceMethodsbyTop25 = []
    SpaceMethodsbyTop50 = []
    SpaceMethodsbyTop100 = []
    SpaceMethodsbyTop150 = []
    SpaceRefMethodsbyTop25 = []
    SpaceRefMethodsbyTop50 = []
    SpaceRefMethodsbyTop100 = []
    SpaceRefMethodsbyTop150 = []
    CoveredMethods = []
    CoveredRefMethods = []
    spacecount = 0
    count = 0

    Ranked_Seed = sorted(Space2Score.keys(), key=lambda d: Space2Score[d], reverse=True)

    for seed in Ranked_Seed:
        spacecount += 1
        solved_targets = []
        solved_issues = []
        patterns = Method2Pattern[seed] if seed in Method2Pattern.keys() else []
        space = Method2Space[seed]
        for full_method in space:
            if full_method in CoveredMethods:
                continue
            CoveredMethods.append(full_method)
            count += 1

            # if m in Method2Space.keys():
            #     space.extend([i for i in Method2Space[m] if i not in space])
            if spacecount <= Top25Number:
                if full_method not in SpaceMethodsbyTop25:
                    SpaceMethodsbyTop25.append(full_method)

            if spacecount <= Top50Number:
                if full_method not in SpaceMethodsbyTop50:
                    SpaceMethodsbyTop50.append(full_method)
            if spacecount <= Top100Number:
                if full_method not in SpaceMethodsbyTop100:
                    SpaceMethodsbyTop100.append(full_method)
            if spacecount <= Top150Number:
                if full_method not in SpaceMethodsbyTop150:
                    SpaceMethodsbyTop150.append(full_method)
            # if hasOtherMethod(full_method, Total_Methods):
            #     cover_record.writerow([count, len(CoveredRefMethods)])
            #     continue
            simple_method = full_method[: -len(full_method.split('(')[-1]) - 1]
            if simple_method in Method2Issues.keys():
                for issue in Method2Issues[simple_method]:
                    # change condition here!!!
                    if issue not in Max_Issues:
                        # print issue
                        continue
                    solved_targets.append(full_method)
                    solved_issues.append(issue)
                    # print count, issue, full_method, Ranked_Full_Methods.index(full_method)+1

                    if issue not in CoveredIssues:
                        CoveredIssues.append(issue)
                    if full_method not in CoveredRefMethods:
                        CoveredRefMethods.append(full_method)
                    if spacecount <= Top25Number:
                        if issue not in IssuesbyTop25:
                            IssuesbyTop25.append(issue)
                        if full_method not in SpaceRefMethodsbyTop25:
                            SpaceRefMethodsbyTop25.append(full_method)
                            # print spacecount, count, full_method, issue
                    if spacecount <= Top50Number:
                        if issue not in IssuesbyTop50:
                            IssuesbyTop50.append(issue)
                        if full_method not in SpaceRefMethodsbyTop50:
                            SpaceRefMethodsbyTop50.append(full_method)
                    if spacecount <= Top100Number:
                        if issue not in IssuesbyTop100:
                            IssuesbyTop100.append(issue)
                        if full_method not in SpaceRefMethodsbyTop100:
                            SpaceRefMethodsbyTop100.append(full_method)
                    if spacecount <= Top150Number:
                        if issue not in IssuesbyTop150:
                            IssuesbyTop150.append(issue)
                        if full_method not in SpaceRefMethodsbyTop150:
                            SpaceRefMethodsbyTop150.append(full_method)
            cover_record.writerow([count, len(CoveredRefMethods)])
        out_record.writerow([seed, ', '.join(patterns), ', '.join(space), Space2Score[seed],
                             ', '.join(solved_targets), ', '.join(solved_issues)])
    # print 'total covered issues: %d, 25(%d) covered issues: %d, 50(%d) covered issues: %d, 20(%d) covered issues: %d' \
    #       % (len(CoveredIssues), Top5Number, len(IssuesbyTop5), Top10Number, len(IssuesbyTop10), Top20Number,
    #          len(IssuesbyTop20))
    # cover_record.writerow([len(CoveredMethods), TOTAL_METHODS[project], len(CoveredRefMethods), TOTAL_REF_METHODS[project]])
    print 'total covered methods: %d/%d, Top 25: %d/%d=%f, Top 50: %d/%d=%f, Top 100: %d/%d=%f, Top 150: %d/%d=%f' \
          % (len(CoveredRefMethods), len(CoveredMethods),
             len(SpaceRefMethodsbyTop25),len(SpaceMethodsbyTop25),  1.0*len(SpaceRefMethodsbyTop25)/len(SpaceMethodsbyTop25),
             len(SpaceRefMethodsbyTop50),len(SpaceMethodsbyTop50), 1.0*len(SpaceRefMethodsbyTop50)/len(SpaceMethodsbyTop50),
             len(SpaceRefMethodsbyTop100),len(SpaceMethodsbyTop100),  1.0*len(SpaceRefMethodsbyTop100)/len(SpaceMethodsbyTop100),
             len(SpaceRefMethodsbyTop150),len(SpaceMethodsbyTop150),  1.0 * len(SpaceRefMethodsbyTop150)/len(SpaceMethodsbyTop150))
    print '................end evaluating space.......................'

def computeSeedSpaceScore(method2space, method2score):
    seedspace2score = {}
    for seed in method2space:
        newspace = [method2score[i] for i in method2space[seed] if i in method2score.keys()]
        size = len(newspace)
        score = sum(newspace)
        seedspace2score[seed] = 1.0*score/size
    return seedspace2score


def computeAllSeedSpaceScore(seeds, method2space, method2score):
    seedspace2score = {}
    newmethod2space = {}
    for seed in seeds:
        if seed not in method2space.keys():
            seedspace2score[seed] = method2score[seed]
            newmethod2space[seed] = [seed]
        else:
            newspace = [method2score[i] for i in method2space[seed] if i in method2score.keys()]
            size = len(newspace)
            score = sum(newspace)
            seedspace2score[seed] = 1.0*score/size
            newmethod2space[seed] = method2space[seed]
    return seedspace2score, newmethod2space



def evaluate(project, version):
    Method2Issues, Total_Methods, Max_Issues = NumberofMethodsSummary(project, version)
    for formulas in parameter.FORMULAS:
        print 'formulas: ', formulas

        # print 'evaluating dev... '
        # Dev_Ranked_Methods, _ = computeRanking.getRankedFullMethods(project, version, formulas)
        # evaluateRankedFullMethods(Dev_Ranked_Methods, Method2Issues, Total_Methods, Max_Issues)
        # Dev_Ranked_Method_Space, Dev_Extended_Seeds, Seed2Pattern= computeSpace.computeSeedSpace(version, Dev_Ranked_Methods)
        # evaluateRankedMethodSpace(Dev_Ranked_Method_Space, Method2Issues, Total_Methods, Max_Issues)
        # evaluateRankedFullMethods(Dev_Extended_Seeds, Method2Issues, Total_Methods, Max_Issues)

        # print 'evaluating dev+evo... '
        Dev_Evo_Ranked_Methods, Method2Score = computeRanking.getRankedFullMethods(project, version, formulas)
        # evaluateRankedFullMethods(project, Dev_Evo_Ranked_Methods, Method2Issues, Total_Methods, Max_Issues)
        Dev_Evo_Ranked_Method_Space, Dev_Evo_Extended_Seeds, Method2Space, Method2Pattern = computeSpace.computeSeedSpace(version, Dev_Evo_Ranked_Methods)
        # evaluateRankedMethodSpace(Dev_Evo_Ranked_Methods, Method2Space, Method2Pattern, Method2Issues, Total_Methods, Max_Issues)
        # evaluateRankedFullMethods(Dev_Evo_Extended_Seeds, Method2Issues, Total_Methods, Max_Issues)
        # Space2Score = computeSeedSpaceScore(Method2Space, Method2Score)
        # evaluateRankedOnlySpace(Space2Score, Method2Pattern, Method2Space, Method2Issues, Total_Methods, Max_Issues)
        AllSpace2Score,  AllMethod2Space = computeAllSeedSpaceScore(Dev_Evo_Ranked_Methods, Method2Space, Method2Score)
        evaluateRankedOnlySpace(project, AllSpace2Score, Method2Pattern, AllMethod2Space, Method2Issues, Dev_Evo_Ranked_Methods, Max_Issues)



if __name__ == '__main__':


    # evaluate('avro', 'avro-1.3.0')
    # evaluate('avro', 'avro-1.6.0')
    # evaluate('avro', 'avro-1.8.1')
    # evaluate('ivy', 'ivy-2.0.0-2009.1')
    # evaluate('ivy', 'ivy-2.1.0-2009.10')
    # evaluate('ivy', 'ivy-2.2.0-2010.9')
    # evaluate('ivy', 'ivy-2.3.0-2013.1')
    # evaluate('ivy', 'ivy-2.4.0-2014.12')
    # evaluate('pdfbox', 'pdfbox-1.8.4-2014.1')
    # evaluate('pdfbox', 'pdfbox-1.8.10-2015.7')
    # evaluate('pdfbox', 'pdfbox-2.0.0')
    evaluate('pdfbox', 'pdfbox-2.0.4-2016.12')

    # evaluate('cxf', 'cxf-3.0.1')






    # dumpAllRefactoredMethods('pdfbox')
    # dumpAllRefactoredMethods('avro')
    # dumpAllRefactoredMethods('ivy')

    # NumberofMethodsSummary('cxf', 'cxf-3.0.1')


    # Method2Issues = NumberofMethodsSummary('avro', 'avro-1.6.0')
    # Method2Issues = NumberofMethodsSummary('avro', 'avro-1.8.1')


