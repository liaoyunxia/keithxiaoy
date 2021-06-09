import os
import re


project_name = os.path.basename(os.path.dirname(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

paths = '{}/jk_p2p_app'.format(BASE_DIR)
print('project_name={}'.format(paths))
count = 0

for (root, dirs, files) in os.walk(paths):
    for file_name in files:
        # print('file_name={}'.format(file_name))

        ends = os.path.splitext(file_name)[-1]
        if ends in ['.log', '.pyc', '.mo', '.ico', '.png',
                    '.svg', '.gif', '.woff', '.jpg', '.eot',
                    '.woff2', '.ttf', '.otf', '.pdf', '.js',
                    ]:
            continue

        if not file_name.startswith('.') \
                and not file_name.startswith('search_chinese.') \
                and '.git' not in root\
                and '.idea' not in root:

            with open(os.path.join(root, file_name), 'r+') as f:
                # print('FILE：{},'.format(os.path.join(root, file_name)))
                s0 = f.readlines()
                f.close()
                zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
                line = []
                for index, str in enumerate(s0):
                    match = zh_pattern.search(str)
                    if match:
                        line.append(index)
                if line:
                    count += 1
                    print('index={}, FILE：{}, line={}, '.format(count, os.path.join(root, file_name), line))
