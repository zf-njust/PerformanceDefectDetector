import csv

package_file = csv.reader(open('C:\Users\chenzhifei\Desktop\subjects\cxf-2.1\project_info.csv'))

out_file = open('C:\Users\chenzhifei\Desktop\subjects\cxf-2.1\package_list.txt', 'w+')

s = ''

for log in package_file:
	if package_file.line_num == 1:
		continue
	filename = log[0]
	if filename.find('Test')==-1:
		continue
	package = log[2]
	item = package + '.' + filename
	if s=='':
		s += item
	else:
		s += '||' + item

out_file.write(s+'\n')
