import sqlite3
import wordninja
from bottle import route, run, template, request, static_file, redirect, bottle

APP = bottle.Bottle()
@APP.get('/')
def index():
    return redirect("/hello/")


@APP.get('/hello/')
def index():
    form = request.GET.decode('gbk')
    keyword = form.get("keyword", "")
    cut = list(wordninja.split(keyword))
    page_id_list = get_page_id_list_from_key_word_cut(cut)
    page_list = get_page_list_from_page_id_list(page_id_list)
    page_list = sort_page_list(page_list, cut)
    context = {
        "page_list": page_list[:20],
        "keyword": keyword
    }
    return template(searcher.html, context)

def sort_page_list(page_list, cut):
    con_list = []
    for page in page_list:
        url = page[2]
        words = page[1]
        title = page[3]
        vector = words.split(" ")
        same = 0
        for i in vector:
            if i in cut:
                same += 1
        cos = same / (len(vector)*len(cut))
        con_list.append([cos, url, words, title])
    con_list = sorted(con_list, key=lambda i: i[0], reverse=True)
    return con_list

def get_page_list_from_page_id_list(page_id_list):
    id_list = "("
    for k in page_id_list:
        id_list += "%s,"%k
    id_list = id_list.strip(",") + ")"
    conn = sqlite3.connect(data5.db")
    c = conn.cursor()
    sql = "select * " \
          + "from page_info  " \
          + "where id in " + id_list + ";"
    res = c.execute(sql)
    res = [r for r in res]
    return res
def get_page_id_list_from_key_word_cut(cut):
    keyword = "("
    for k in cut:
        if k == " ":
            continue
        keyword += "'%s',"%k
    keyword = keyword.strip(",") + ")"
    conn = sqlite3.connect(data5.db")
    c = conn.cursor()
    sql = "select page_id " \
          + "from page_index  " \
          + "where keyword in " + keyword + ";"
    res = c.execute(sql)
    res = [r[0] for r in res]
    return res

if __name__ == '__main__':
    bottle.run(application=APP)
