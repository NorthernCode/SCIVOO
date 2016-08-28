import urllib.request

f_courses = open('course_urls.txt', 'r', encoding='utf-8')

f_out = open('course_data.csv', 'w', encoding='utf-8')

for line in f_courses:
    print('Course: ' + line)
    url = 'https://mycourses.aalto.fi/course/info.php?lang=en&id=' + line.rstrip()
    print(page_url)

    local_filename, headers = urllib.request.urlretrieve(page_url)
    html = open(local_filename, encoding='utf-8')
    content = html.read()
    position = 0

    f_out.write(line + ';')

    search = 'Schedule:</b>'
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
        position = end
    else:
        f_out.write(';')

    search = 'Teaching Period:</b>'
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')

    search = 'Credits:</b>'
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + '\n')

    f_out.write('\n')




f_out.close
