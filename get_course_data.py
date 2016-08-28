import urllib.request

f_courses = open('course_urls.txt', 'r', encoding='utf-8')

f_out = open('course_data.csv', 'w', encoding='utf-8')

for line in f_courses:
    print('Course: ' + line)
    page_url = 'https://mycourses.aalto.fi/course/info.php?lang=en&id=' + line.rstrip()
    print(page_url)

    local_filename, headers = urllib.request.urlretrieve(page_url)
    html = open(local_filename, encoding='utf-8')
    content = html.read()

    f_out.write(line.rstrip() + ';')

    search = 'summary_left'
    start = content.find(search)
    search = '<p'
    start = content.find(search, start)
    search = '>'
    start = content.find(search, start)

    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        split = content[start:end].split(' ')
        f_out.write(split[0] + ';')
        start += len(split[0]) + 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')

    search = '<p'
    start = content.find(search, start)
    search = '>'
    start = content.find(search, start)

    if(start != -1):
        start += len(search) + len(split[0]) + 1
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')

    search = '<p'
    start = content.find(search, start)
    search = '>'
    start = content.find(search, start)

    if(start != -1):
        start += len(search) + len(split[0]) + 1
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')



    search = 'Schedule:</b> '
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')

    search = 'Teaching Period:</b> '
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end] + ';')
    else:
        f_out.write(';')

    search = 'Credits:</b> '
    start = content.find(search)
    if(start != -1):
        start += len(search)
        end = content.find('<', start) - 1
        f_out.write(content[start:end])

    f_out.write('\n')




f_out.close
