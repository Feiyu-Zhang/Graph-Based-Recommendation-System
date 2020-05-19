import pymysql
from collections import Counter


def connectMySQL():
    return pymysql.connect(host="58.87.110.76", port=3306, user="root", password="WWWsql123", database="knowledge")


def queryRelation(mysql, args):
    conn = connectMySQL()
    cur = conn.cursor()
    try:
        cur.execute(mysql, args)
        results = cur.fetchall()
        resultsList = [i[0] for i in results]
        return resultsList
        #  conn.commit()  # only for insert/alter/delete
    except:
        conn.rollback()
    conn.close()


def recommendBasedOnSearch(itemID):
    knowledgeID = itemID
    print(knowledgeID)
    mysql1 = 'select kid2 from edu_knowledge_relation where kid1=(%s)'
    relatedItemList = queryRelation(mysql1, knowledgeID)
    mysql2 = 'select kid1 from edu_knowledge_relation where kid2=(%s)'
    relatedItemList.extend(queryRelation(mysql2, knowledgeID))
    # Retrieval
    recommendList = list()
    for relatedItemId in relatedItemList:
        mysql3 = 'select kid2 from edu_knowledge_relation where kid1=(%s)'
        recommendList.extend(queryRelation(mysql3, relatedItemId))
        mysql4 = 'select kid1 from edu_knowledge_relation where kid2=(%s)'
        recommendList.extend(queryRelation(mysql4, relatedItemId))
    # Rank
    recommendList = [e for e in recommendList if e not in itemID]
    recommendElements = Counter(recommendList).most_common(3)
    return recommendElements


def recommendBasedOnHistory(data):
    recommendList = list()
    # Retrieval
    for relatedItemId in data['relatedKnowledge']:
        mysql1 = 'select kid1 from edu_knowledge_relation where kid2=(%s)'
        recommendList.extend(queryRelation(mysql1, relatedItemId))
        mysql2 = 'select kid2 from edu_knowledge_relation where kid1=(%s)'
        recommendList.extend(queryRelation(mysql2, relatedItemId))
    # Rank
    recommendList = [e for e in recommendList if e not in data['knowledge']]
    recommendElements = Counter(recommendList).most_common(3)
    return recommendElements


# for debug
# if __name__ == '__main__':
    #     # 1
    # result = recommendBasedOnSearch('猪八戒')
    #     # 2
    #     data = {'knowledge': ['孙悟空'], 'relatedKnowledge': ['牛魔王'], 'currentRelatedKnowledge': '牛魔王'}
    #     result = recommendBasedOnHistory(data)
    # print(result)

# 下面的是读取本地csv数据，做算法流程验证
# 读取知识图谱
'''csvFile = open("data/The_Journey_to_the_West/triples.csv", encoding='utf-8')
reader = csv.reader(csvFile)

kg = {}
for item in reader:
    if reader.line_num == 1:
        continue
    kg.setdefault(item[0], []).append(item[1])

csvFile.close()


def recommend(itemId):
    # 用户选择一个节点,显示推荐列表，这里暂时选择猪八戒
    topN = 2
    if itemId in kg.keys():
        itemNotRelated = kg[itemId]
        itemRecommend = []
        for item in itemNotRelated:
            if item in kg.keys():
                itemRecommend.extend(kg[item])
        if len(itemRecommend):
            occurence_count = Counter(itemRecommend).most_common(topN)
            total = 0
            for itemRec in occurence_count:
                total = total + itemRec[1]
            resultStr = ""
            for itemRec in occurence_count:
                resultStr = resultStr + itemRec[0] + str(itemRec[1] / total)
            return resultStr
        else:
            return "亲，暂时没有相关推荐"
    else:
        return "亲，暂时没有相关推荐"
        # print("当前用户选中 ", idChoose)


# test locally
# result = recommend("test")
# print(result)

def get_keys(d, value):
    return [k for k, v in d.items() if value in v]


def basicRecList(relationDict, idChoose):
    frontList = relationDict[idChoose]
    # print(frontList)
    backList = get_keys(relationDict, idChoose)
    # print(backList)
    recList = frontList + backList
    # print(recList)
    # result = Counter(recList)
    # print(result)
    # recListTopN = Counter(recList).most_common(top_n)
    return recList
    
    
top_n = 3
recList = basicRecList(kg, idChoose)
recList = Counter(recList).most_common(top_n)
print("显示初步推荐列表及权重", recList)

# 结合历史用户浏览数据，进行推荐，这里先选择唐僧（唐僧的推荐权重占1），然后再选择猪八戒（猪八戒的推荐权重占2），进行推荐
history = ['唐僧']
idChoose = '猪八戒'
recListWithHistory = basicRecList(kg, idChoose)

recListWithHistory = recListWithHistory + recListWithHistory
for item in history:
    hisList = basicRecList(kg, item)
    recListWithHistory = recListWithHistory + hisList


# print(recListWithHistory)
result = Counter(recListWithHistory).most_common(top_n)
print("结合历史记录的推荐列表及权重", result)

# 推荐列表滤除已选择的人物，这里滤除上面选择的唐僧
for item in history:
    recListWithHistory.remove(item)

result = Counter(recListWithHistory).most_common(top_n)
print("滤除用户已选择历史后的推荐列表及权重", result)
'''
