import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

f_units = open('laitokset.txt', 'r', encoding='utf-8')

f_out = open('course_urls.txt', 'w', encoding='utf-8')

for line in f_units:
    print('Unit: ' + line)
    url = 'https://mycourses.aalto.fi/course/index.php?categoryid=' + line.rstrip() + '&perpage=100&browse=courses&page='
    had_courses = True
    n = 0
    while(had_courses):
        page_url = url + str(n)
        print(page_url)
        local_filename, headers = urllib.request.urlretrieve(page_url)
        html = open(local_filename, encoding='utf-8')
        content = html.read()
        had_more = True
        position = 0
        while(had_more):
            search = 'enrolmenticons"><a href="https://mycourses.aalto.fi/course/view.php?id='
            start = content.find(search, position)
            if(start != -1):
                start += len(search)
                end = content.find('>', start) - 1
                f_out.write(content[start:end] + '\n')
                position = end
            else:
                had_more = False
                if(position == 0):
                    had_courses = False
        n += 1

f_out.close
