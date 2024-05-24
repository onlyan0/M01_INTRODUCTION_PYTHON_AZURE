# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def exec():
    import json, re, csv
    from collections import defaultdict

    with open('10K.github.json', encoding='utf-8') as f, open('bulatov_res.csv', 'w', encoding='utf-8',
                                                              newline='') as o:
        t = f.readlines()
        d = {}
        for obj in t:
            j = json.loads(obj)
            if j.get('type') == 'PushEvent' and j.get('payload', {}).get('commits'):
                c = j.get('payload', {}).get('commits')
                for com in c:
                    author = com.get('author', {}).get('name')
                    message =  re.sub(r'[\.\,\-\;\|\:\?\!\(\)\{\}]', '', com.get('message', '').lower())
                    m = message.split()
                    if len(m) > 2:
                        for i in range(len(m) - 2):
                            d.setdefault(author, defaultdict(int))[tuple(m[i:i + 3])] += 1
        w = csv.writer(o, delimiter=';', quoting=csv.QUOTE_ALL)
        w.writerow(['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram'])
        for auth, data in d.items():
            l = [auth] + [' '.join(list(key)) for key, cnt in
                          sorted(data.items(), key=lambda x: (x[1], x[0]), reverse=True)[:5]]
            l += [''] * (6 - len(l))
            w.writerow(l)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
