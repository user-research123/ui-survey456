#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'rb') as f:
    lines = f.readlines()
    line_1304 = lines[1303]  # 0-indexed
    print("Line 1304 bytes:", line_1304)
    print("Line 1304 decoded:", line_1304.decode('utf-8'))
    if b'4\xe6\x9c\x887\xe6\x97\xa5' in line_1304:
        print("Contains: 4 月 7 日 (NO SPACE)")
    if b'4\xe6\x9c\x88 7\xe6\x97\xa5' in line_1304:
        print("Contains: 4 月 7 日 (WITH SPACE)")
    if b'4\xe6\x9c\x888\xe6\x97\xa5' in line_1304:
        print("Contains: 4 月 8 日")
