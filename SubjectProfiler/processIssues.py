import csv
import sys
sys.path.append('..')
import parameter

# project = PDFBOX AND (text ~ slow OR text ~ performance OR text ~ hang OR text ~ latency OR text ~ throughput OR text ~ speed OR text ~ optimization OR text ~ responsive OR text ~ fast OR text ~ wast OR text ~ efficien OR text ~ unnecessary OR text ~ redundan) ORDER BY created ASC, cf[10010] DESC

# project = PDFBOX AND (description ~ slow OR description ~ performance OR description ~ hang OR description ~ latency OR description ~ throughput OR description ~ speed OR description ~ optimization OR description ~ responsive OR description ~ fast OR description ~ wast OR description ~ efficien OR description ~ unnecessary OR description ~ redundan OR description ~ time) ORDER BY created ASC, cf[10010] DESC

include_keywords = ('performance', 'slow',  # MSR 2012
                    'latency', 'throughput',  # PLDI 2012
                    'speed', 'optimization', 'responsive', 'fast',
                    'wast', 'efficien', 'unnecessar', 'redundan',
                    'too many times', 'a lot of time', 'too much time'
            )



def process_issue_files(project):
    issues_paths = parameter.ISSUE_PATHS[project]
    issue_final_path = csv.writer(open(parameter.ISSUE_PATH[project], 'wb+'))
    issue_final_path.writerow(['Project', 'Key', 'Summary', 'Issue Type', 'Status', 'Priority', 'Resolution',
                               'Assignee', 'Reporter', 'Creator', 'Created', 'Last Viewed', 'Updated', 'Resolved',
                               'Affects Version/s', 'Fix Version/s', 'Component/s', 'Due Date', 'Votes', 'Watchers',
                               'Images', 'Original Estimate', 'Remaining Estimate', 'Time Spent', 'Work Ratio',
                               'Sub-Tasks', 'Linked Issues', 'Environment', 'Description'])
    for path in issues_paths:
        record = csv.reader(open(path))
        for issue in record:
            if record.line_num == 1:
                continue
            issue_final_path.writerow(issue[0:29])



def extract_keywords_issues(project):
    issue_final_path = csv.writer(open(parameter.KEYWORDS_ISSUE_PATH[project], 'wb+'))
    issue_final_path.writerow(['Project', 'Key', 'Summary', 'Issue Type', 'Status', 'Priority', 'Resolution',
                               'Assignee', 'Reporter', 'Creator', 'Created', 'Last Viewed', 'Updated', 'Resolved',
                               'Affects Version/s', 'Fix Version/s', 'Component/s', 'Due Date', 'Votes', 'Watchers',
                               'Images', 'Original Estimate', 'Remaining Estimate', 'Time Spent', 'Work Ratio',
                               'Sub-Tasks', 'Linked Issues', 'Environment', 'Description'])
    record = csv.reader(open(parameter.ISSUE_PATH[project]))
    for issue in record:
        if record.line_num == 1:
            continue
        for kw in include_keywords:
            if issue[2].lower().find(kw)!=-1 or issue[28].lower().find(kw)!=-1:
                issue_final_path.writerow(issue)
                print kw
                break



if __name__ == "__main__":
    # process_issue_files('pdfbox')
    # extract_keywords_issues('pdfbox')

    # process_issue_files('avro')
    # extract_keywords_issues('avro')

    # process_issue_files('ivy')
    # extract_keywords_issues('ivy')

    process_issue_files('cxf')
    extract_keywords_issues('cxf')