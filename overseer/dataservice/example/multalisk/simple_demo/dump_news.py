# -*- coding: utf-8 -*-
"""
    database transformation for news project used by multliask/adapter
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import time
from datetime import date, timedelta

import MySQLdb
import pymongo
from redis import StrictRedis

# from multalisk.ext.adapter import Adapter


R_DB = {
    'host': '10.132.11.144',
    'db': 'stat_EN',
    'user': 'dolphin',
    'passwd': 'dolphin_stat@logsvr',
    'charset': 'utf8',
    'use_unicode': True,
}

W_DB = {
    'host': '127.0.0.1',
    'db': 'news_report',
    'user': 'root',
    'passwd': 'P@55word',
    'charset': 'utf8',
    'use_unicode': True,
}

MONGO_LOCALE_DCT = {'tr-tr': '54.93.65.152',
                    'ru-ru': '54.93.65.152',
                    'ja-jp': '10.132.11.144',
                    'ar-sa': '52.74.106.7'}
MONGO_PORT = 27017

REDIS_ADDR = {'host': '127.0.0.1', 'port': 6379, 'db': 7}


def check_table(locale, w_conn, news_type=''):
    if news_type:
        news_type = '_%s' % news_type
    cur_w = w_conn.cursor()
    origin_table_name = "report_origin_%s%s" % (
        locale.replace('-', '_'), news_type)
    type_sum_table_name = "report_type_sum_%s%s" % (
        locale.replace('-', '_'), news_type)
    category_sum_table_name = "report_category_sum_%s%s" % (locale.replace(
        '-', '_'), news_type)
    priority_sum_table_name = "report_priority_sum_%s%s" % (locale.replace(
        '-', '_'), news_type)
    source_sum_table_name = "report_source_sum_%s%s" % (
        locale.replace('-', '_'), news_type)
    news_sum_table_name = "report_news_sum_%s%s" % (
        locale.replace('-', '_'), news_type)

    try:
        sql_str = "create table if not exists %s (\
              `news_id` bigint(20) unsigned NOT NULL,\
              `category` smallint(5) NOT NULL,\
              `priority` smallint(5) NOT NULL,\
              `source` varchar(128) NOT NULL,\
              `top_click` int(11) NOT NULL DEFAULT '0',\
              `recommend_click` int(11) NOT NULL DEFAULT '0',\
              `home_click` int(11) NOT NULL DEFAULT '0',\
              `push_click` int(11) NOT NULL DEFAULT '0',\
              `top_show` int(11) NOT NULL DEFAULT '0',\
              `recommend_show` int(11) NOT NULL DEFAULT '0',\
              `home_show` int(11) NOT NULL DEFAULT '0',\
              `push_show` int(11) NOT NULL DEFAULT '0',\
              `date` varchar(30) NOT NULL,\
              PRIMARY KEY (`news_id`, `date`)) \
              ENGINE=InnoDB DEFAULT CHARSET=utf8" % origin_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (\
          `type` varchar(32) NOT NULL,\
          `click` int(11) NOT NULL DEFAULT '0',\
          `show` int(11) NOT NULL DEFAULT '0',\
          `date` varchar(30) NOT NULL,\
          PRIMARY KEY (`type`,`date`)) ENGINE=InnoDB \
          DEFAULT CHARSET=utf8" % type_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (\
          `category` smallint(5) NOT NULL,\
          `top_click` int(11) NOT NULL DEFAULT '0',\
          `top_show` int(11) NOT NULL DEFAULT '0',\
          `recommend_click` int(11) NOT NULL DEFAULT '0',\
          `recommend_show` int(11) NOT NULL DEFAULT '0',\
          `home_click` int(11) NOT NULL DEFAULT '0',\
          `home_show` int(11) NOT NULL DEFAULT '0',\
          `push_click` int(11) NOT NULL DEFAULT '0',\
          `push_show` int(11) NOT NULL DEFAULT '0',\
          `date` varchar(30) NOT NULL,\
          PRIMARY KEY (`category`,`date`)) ENGINE=InnoDB \
          DEFAULT CHARSET=utf8" % category_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (\
          `priority` smallint(5) NOT NULL,\
          `top_click` int(11) NOT NULL DEFAULT '0',\
          `top_show` int(11) NOT NULL DEFAULT '0',\
          `recommend_click` int(11) NOT NULL DEFAULT '0',\
          `recommend_show` int(11) NOT NULL DEFAULT '0',\
          `home_click` int(11) NOT NULL DEFAULT '0',\
          `home_show` int(11) NOT NULL DEFAULT '0',\
          `push_click` int(11) NOT NULL DEFAULT '0',\
          `push_show` int(11) NOT NULL DEFAULT '0',\
          `date` varchar(30) NOT NULL,\
          PRIMARY KEY (`priority`,`date`)) ENGINE=InnoDB \
          DEFAULT CHARSET=utf8" % priority_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (\
          `source` varchar(128) NOT NULL,\
          `category` smallint(5) NOT NULL,\
          `top_click` int(11) NOT NULL DEFAULT '0',\
          `top_show` int(11) NOT NULL DEFAULT '0',\
          `recommend_click` int(11) NOT NULL DEFAULT '0',\
          `recommend_show` int(11) NOT NULL DEFAULT '0',\
          `home_click` int(11) NOT NULL DEFAULT '0',\
          `home_show` int(11) NOT NULL DEFAULT '0',\
          `push_click` int(11) NOT NULL DEFAULT '0',\
          `push_show` int(11) NOT NULL DEFAULT '0',\
          `date` varchar(30) NOT NULL,\
          PRIMARY KEY (`source`,`date`)) ENGINE=InnoDB \
          DEFAULT CHARSET=utf8" % source_sum_table_name
        cur_w.execute(sql_str)

        sql_str = "create table if not exists %s (\
          `news_id` bigint(20) unsigned NOT NULL,\
          `category` smallint(5) NOT NULL,\
          `priority` smallint(5) NOT NULL,\
          `source` varchar(128) NOT NULL,\
          `top_click` int(11) NOT NULL DEFAULT '0',\
          `top_show` int(11) NOT NULL DEFAULT '0',\
          `recommend_click` int(11) NOT NULL DEFAULT '0',\
          `recommend_show` int(11) NOT NULL DEFAULT '0',\
          `home_click` int(11) NOT NULL DEFAULT '0',\
          `home_show` int(11) NOT NULL DEFAULT '0',\
          `push_click` int(11) NOT NULL DEFAULT '0',\
          `push_show` int(11) NOT NULL DEFAULT '0',\
          `total_click` int(11) NOT NULL DEFAULT '0',\
          `total_show` int(11) NOT NULL DEFAULT '0',\
          `date` varchar(30) NOT NULL,\
          INDEX `index_date` (`date`), \
          PRIMARY KEY (`news_id`,`date`)) ENGINE=InnoDB DEFAULT\
          CHARSET=utf8" % news_sum_table_name
        cur_w.execute(sql_str)

        w_conn.commit()
    except Exception as e:
        print 'check table error:%s' % e
    cur_w.close()


def fill_data(infos, field_str, date_str, locale, r_conn, w_conn,
              news_type=''):
    source_prefix = 'new_' if news_type else ''
    cur = r_conn.cursor()
    cur_w = w_conn.cursor()
    if news_type:
        news_type = '_%s' % news_type
    cur.execute("select wid from News_show_%s where country='%s' \
        order by wid" % (date_str, locale))
    res = cur.fetchall()
    news_id_list = [int(res_tuple[0]) for res_tuple in res]

    table_name = "report_origin_%s%s" % (
        locale.replace('-', '_'), news_type)
    type_sum_table_name = "report_type_sum_%s%s" % (
        locale.replace('-', '_'), news_type)
    category_sum_table_name = "report_category_sum_%s%s" % (locale.replace(
        '-', '_'), news_type)
    priority_sum_table_name = "report_priority_sum_%s%s" % (locale.replace(
        '-', '_'), news_type)
    source_sum_table_name = "report_source_sum_%s%s" % (
        locale.replace('-', '_'), news_type)
    news_sum_table_name = "report_news_sum_%s%s" % (
        locale.replace('-', '_'), news_type)

    for news_id_start in range(len(news_id_list))[::10000]:
        news_ids = news_id_list[news_id_start:news_id_start + 10000]
        mongo_time = time.time()
        mongo_res = infos.find(
            {'_id': {'$in': news_ids}},
            {'category': 1, 'status': 1, 'news.linksources': 1})
        print 'query mongo time is %s' % (time.time() - mongo_time)
        result_to_write = [row for row in mongo_res]
        result_to_write.sort(key=lambda item: int(item['_id']))
        [row.update({'source': row['news']['linksources'][0]['blockId']})
         for row in result_to_write]
        sql_str = "select wid, count from %sClassify_show_%s where wid \
        in %s and source = 'home' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids)))
        query_mysql_time = time.time()
        try:
            cur.execute(sql_str)
        except Exception as e:
            print e
            print sql_str
        home_show_tuple = cur.fetchall()
        home_show_list = [row for row in home_show_tuple]
        home_show_list.sort(key=lambda item: int(item[0]))
        for show_row in home_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'home_show': show_row[1]})
                    break
        cur.execute("select wid, count from %sClassify_show_%s \
            where wid in %s and source = 'top' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        top_show_tuple = cur.fetchall()
        top_show_list = [row for row in top_show_tuple]
        top_show_list.sort(key=lambda item: int(item[0]))
        for show_row in top_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'top_show': show_row[1]})
                    break
        cur.execute("select wid, count from %sClassify_show_%s \
            where wid in %s and source = 'push' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        push_show_tuple = cur.fetchall()
        push_show_list = [row for row in push_show_tuple]
        push_show_list.sort(key=lambda item: int(item[0]))
        for show_row in push_show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'push_show': show_row[1]})
                    break
        cur.execute("select wid, count from %sClassify_weibo_%s \
            where wid in %s and source = 'home' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'home_click': click_row[1]})
                    break
        cur.execute("select wid, count from %sClassify_weibo_%s \
            where wid in %s and source = 'top' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'top_click': click_row[1]})
                    break
        cur.execute("select wid, count from %sClassify_weibo_%s \
            where wid in %s and source = 'push' order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'push_click': click_row[1]})
                    break
        cur.execute("select wid, count from %sP_1_show_%s \
            where wid in %s order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        show_tuple = cur.fetchall()
        show_list = [row for row in show_tuple]
        show_list.sort(key=lambda item: int(item[0]))
        for show_row in show_list:
            for row in result_to_write:
                if int(row['_id']) == int(show_row[0]):
                    row.update({'recommend_show': show_row[1]})
                    break
        cur.execute("select wid, count from %sP_1_weibo_%s \
            where wid in %s order by wid" % (
            source_prefix, date_str, str(tuple(news_ids))))
        click_tuple = cur.fetchall()
        click_list = [row for row in click_tuple]
        click_list.sort(key=lambda item: int(item[0]))
        for click_row in click_list:
            for row in result_to_write:
                if int(row['_id']) == int(click_row[0]):
                    row.update({'recommend_click': click_row[1]})
                    break
        print 'query mysql time is %s' % (time.time() - query_mysql_time)
        start_time = time.time()
        for result in result_to_write:
            try:
                # insert into origin table
                cur_w.execute("insert into %s (news_id, category, priority, \
                    source, top_click, recommend_click, home_click, \
                    push_click, top_show, recommend_show, home_show, \
                    push_show, date) values(\
                    %s,%s,%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,'%s')" % (
                    table_name, result['_id'], result.get('category', 0),
                    result['status'] if result['status'] else -100,
                    result.get('source', ''), result.get('top_click', 0),
                    result.get('recommend_click', 0),
                    result.get('home_click', 0),
                    result.get('push_click', 0), result.get('top_show', 0),
                    result.get('recommend_show', 0),
                    result.get('home_show', 0),
                    result.get('push_show', 0), field_str))
                # insert into type_sum table
                sql_str = "insert into %s (type, click, `show`, date) values(\
                    '%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'top', result.get(
                        'top_click', 0), result.get('top_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,\
                `show`=`show`+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0))
                cur_w.execute(sql_str)

                sql_str = "insert into %s (type, click, `show`, date) \
                values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'recommend',
                    result.get('recommend_click', 0), result.get(
                        'recommend_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,\
                `show`=`show`+%s" % (result.get('recommend_click', 0),
                                     result.get('recommend_show', 0))
                cur_w.execute(sql_str)

                sql_str = "insert into %s (type, click, `show`, date)\
                 values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'home', result.get('home_click', 0),
                    result.get('home_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,\
                `show`=`show`+%s" % (
                    result.get('home_click', 0), result.get('home_show', 0))
                cur_w.execute(sql_str)

                sql_str = "insert into %s (type, click, `show`, date) \
                values('%s',%s,%s,'%s')" % (
                    type_sum_table_name, 'push', result.get('push_click', 0),
                    result.get('push_show', 0), field_str)
                sql_str += "on duplicate key update click=click+%s,\
                `show`=`show`+%s" % (
                    result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)

                # insert into category_sum table
                sql_str = "insert into %s (category, top_click, top_show, \
                    recommend_click, recommend_show, home_click, home_show, \
                    push_click, push_show, date) values(\
                    %s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (
                    category_sum_table_name, result.get('category', 0),
                    result.get('top_click', 0), result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0),
                    field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,\
                top_show=top_show+%s,recommend_click=recommend_click+%s,\
                recommend_show=recommend_show+%s,home_click=home_click+%s,\
                home_show=home_show+%s,push_click=push_click+%s,\
                push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0),
                    result.get('home_show', 0), result.get('push_click', 0),
                    result.get('push_show', 0))
                cur_w.execute(sql_str)

                # insert into priority_sum table
                sql_str = "insert into %s (priority, top_click,\
                    top_show, recommend_click, recommend_show, home_click,\
                    home_show, push_click, push_show, date) values(\
                    %s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (
                    priority_sum_table_name, result['status'] if result[
                        'status'] else -100, result.get('top_click', 0),
                    result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0),
                    field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,\
                top_show=top_show+%s,recommend_click=recommend_click+%s,\
                recommend_show=recommend_show+%s,home_click=home_click+%s,\
                home_show=home_show+%s,push_click=push_click+%s,\
                push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)

                # insert into source_sum table
                sql_str = "insert into %s (source, category, top_click,\
                    top_show, recommend_click, recommend_show, home_click,\
                    home_show, push_click, push_show, date) values(\
                    '%s', %s, %s, %s, %s, %s, %s,%s, %s, %s, '%s')" % (
                    source_sum_table_name, result.get('source', ''),
                    result.get('category', 0), result.get('top_click', 0),
                    result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0),
                    field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,\
                top_show=top_show+%s,recommend_click=recommend_click+%s,\
                recommend_show=recommend_show+%s,home_click=home_click+%s,\
                home_show=home_show+%s,push_click=push_click+%s,\
                push_show=push_show+%s" % (
                    result.get('top_click', 0), result.get('top_show', 0),
                    result.get('recommend_click', 0),
                    result.get('recommend_show', 0),
                    result.get('home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0))
                cur_w.execute(sql_str)

                # insert into news_sum table
                total_click = result.get('top_click', 0) + result.get(
                    'home_click', 0) + result.get('push_click', 0)
                total_show = result.get(
                    'top_show', 0) + result.get('home_show', 0) + result.get(
                    'push_show', 0)
                sql_str = "insert into %s (news_id, source, category, \
                    priority, top_click, top_show, recommend_click, \
                    recommend_show, home_click, home_show, push_click, \
                    push_show, total_click, total_show, date) values(\
                    %s, '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                    '%s')" % (news_sum_table_name, result['_id'],
                              result.get('source', ''), result.get(
                    'category', 0), result['status'] if result['status']
                    else -100, result.get('top_click', 0), result.get(
                        'top_show', 0), result.get('recommend_click', 0),
                    result.get('recommend_show', 0), result.get(
                        'home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0),
                    total_click, total_show, field_str)
                sql_str += "on duplicate key update top_click=top_click+%s,\
                top_show=top_show+%s,recommend_click=recommend_click+%s,\
                recommend_show=recommend_show+%s,home_click=home_click+%s,\
                home_show=home_show+%s,push_click=push_click+%s,\
                push_show=push_show+%s,total_click=total_click+%s,\
                total_show=total_show+%s" % (
                    result.get('top_click', 0), result.get(
                        'top_show', 0), result.get('recommend_click', 0),
                    result.get('recommend_show', 0), result.get(
                        'home_click', 0), result.get('home_show', 0),
                    result.get('push_click', 0), result.get('push_show', 0),
                    total_click, total_show)
                cur_w.execute(sql_str)

            except Exception as e:
                print e
                print result
        w_conn.commit()
        print '10000 inserted, insert time is %s' % (time.time() - start_time)
    cur.close()
    cur_w.close()


def dump(locale, dump_date, db_name, mongo_addr):
    print 'begin dump %s...' % db_name
    mongo_conn = pymongo.Connection(mongo_addr, MONGO_PORT)
    r_conn = MySQLdb.connect(**R_DB)
    w_conn = MySQLdb.connect(**W_DB)
    date_str = dump_date.strftime('%Y%m%d')
    field_str = dump_date.strftime('%Y-%m-%d')

    infos = mongo_conn[db_name]['infos']
    fill_data(infos, field_str, date_str, locale, r_conn, w_conn)
    fill_data(infos, field_str, date_str, locale, r_conn, w_conn, 'app')

    mongo_conn.close()
    r_conn.close()
    w_conn.close()
    print 'dump %s complete!' % db_name


def run():
    date_ = date.today() - timedelta(days=1)
    for locale, mongo_addr in MONGO_LOCALE_DCT.iteritems():
        db_name = 'weibo' if locale == 'ja-jp' else \
            'weibo_%s' % locale.replace('-', '_')
        dump(locale, date_, db_name, mongo_addr)

    redis_conn = StrictRedis(**REDIS_ADDR)
    redis_conn.set('news_dump_%s' % date_, 0)
    print 'adapter done!'


if __name__ == "__main__":
    conn = MySQLdb.connect(**W_DB)
    for locale in MONGO_LOCALE_DCT:
        check_table(locale, conn)
        check_table(locale, conn, 'app')
    conn.close()
    run()
    # k = Adapter({run: '37 2 * * *'})
    # k.run()
