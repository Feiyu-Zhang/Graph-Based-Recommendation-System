import csv
import pymysql


def mySQL(sql, y):
    conn = pymysql.connect(host="58.87.110.76", port=3306, user="root", password="WWWsql123", database="knowledge")
    cur = conn.cursor()
    try:
        cur.execute(sql, y)
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def csvReader():
    with open(r'data\Water_Margin.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # insert knowledge data
        # knowledgeSet = set()  # set
        # for row in reader:
        #     knowledgeSet.add(row['head'])
        #     knowledgeSet.add(row['tail'])
        # numberOfKnowledge = len(knowledgeSet)
        # for k in knowledgeSet:
        #     y = (k)
        #     print(y)
        #     sql = 'insert into edu_knowledge (name) values (%s)'
        #     mySQL(sql, y)
        # print(numberOfKnowledge)

        # insert relation data

        # for row in reader:
        #     print(row['head'], row['tail'])
        #     y = (row['head'], row['tail'])
        #     sql = 'insert into edu_knowledge_relation (kid1,kid2) values (%s, %s)'
        #     mySQL(sql, y)


if __name__ == '__main__':
    csvReader()
