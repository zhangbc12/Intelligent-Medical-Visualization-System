#!/usr/bin/env python3
# coding: utf-8
from py2neo import Graph


class AnswerSearching:
    def __init__(self):
        self.graph = Graph("http://localhost:8474", auth=("neo4j", "zbc990812"))
        self.top_num = 10

    def question_parser(self, data):
        """
        主要是根据不同的实体和意图构造cypher查询语句
        :param data: {"Disease":[], "Alias":[], "Symptom":[], "Complication":[]}
        :return:
        """
        sqls = []
        if data:
            for intent in data["intentions"]:
                sql_ = {}
                sql_["intention"] = intent
                sql = []
                if data.get("Disease"):
                   sql = self.transfor_to_sql("Disease", data["Disease"], intent)
                elif data.get("Alias"):
                    sql = self.transfor_to_sql("Alias", data["Alias"], intent)
                elif data.get("Symptom"):
                    sql = self.transfor_to_sql("Symptom", data["Symptom"], intent)
                elif data.get("Complication"):
                    sql = self.transfor_to_sql("Complication", data["Complication"], intent)

                if sql:
                    sql_['sql'] = sql
                    sqls.append(sql_)
        return sqls

    def transfor_to_sql(self, label, entities, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        if not entities:
            return []
        sql = []

        # 查询症状
        if intent == "query_symptom":
            if label == "Disease":
                sql = ["MATCH (d:Disease)-[:HAS_SYMPTOM]->(s) WHERE d.name='{0}' RETURN d.name,s.name".format(e)
                   for e in entities]
            elif label == "Alias":
                sql = ["MATCH (a:Alias)<-[:ALIAS_IS]-(d:Disease)-[:HAS_SYMPTOM]->(s) WHERE a.name='{0}' return " \
                   "d.name,s.name".format(e) for e in entities]

        # 查询治疗方法
        elif intent == "query_cureway":
            if label == "Disease":
                sql = ["MATCH (d:Disease)-[:HAS_DRUG]->(n) WHERE d.name='{0}' return d.name,d.treatment," \
                        "n.name".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (n)<-[:HAS_DRUG]-(d:Disease)-[]->(a:Alias) WHERE a.name='{0}' " \
                        "return d.name, d.treatment, n.name".format(e) for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (n)<-[:HAS_DRUG]-(d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' " \
                        "return d.name,d.treatment, n.name".format(e) for e in entities]
            elif label == "Complication":
                sql = ["MATCH (n)<-[:HAS_DRUG]-(d:Disease)-[]->(c:Complication) WHERE c.name='{0}' " \
                        "return d.name,d.treatment, n.name".format(e) for e in entities]

        # 查询治疗周期
        elif intent == "query_period":
            if label == "Disease":
                sql = ["MATCH (d:Disease) WHERE d.name='{0}' return d.name,d.period".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (d:Disease)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.period".format(e) \
                        for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' return d.name,d.period".format(e) \
                        for e in entities]
            elif label == "Complication":
                sql = ["MATCH (d:Disease)-[]->(c:Complication) WHERE c.name='{0}' return d.name," \
                        "d.period".format(e) for e in entities]

        # 查询治愈率
        elif intent == "query_rate":
            if label == "Disease":
                sql = ["MATCH (d:Disease) WHERE d.name='{0}' return d.name,d.rate".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (d:Disease)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.rate".format(e) \
                        for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' return d.name,d.rate".format(e) \
                        for e in entities]
            elif label == "Complication":
                sql = ["MATCH (d:Disease)-[]->(c:Complication) WHERE c.name='{0}' return d.name," \
                        "d.rate".format(e) for e in entities]

        # 查询检查项目
        elif intent == "query_checklist":
            if label == "Disease":
                sql = ["MATCH (d:Disease) WHERE d.name='{0}' return d.name,d.checklist".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (d:Disease)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.checklist".format(e) \
                        for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' return d.name," \
                        "d.checklist".format(e) for e in entities]
            elif label == "Complication":
                sql = ["MATCH (d:Disease)-[]->(c:Complication) WHERE c.name='{0}' return d.name," \
                        "d.checklist".format(e) for e in entities]

        # 查询科室
        elif intent == "query_department":
            if label == "Disease":
                sql = ["MATCH (d:Disease)-[:DEPARTMENT_IS]->(n) WHERE d.name='{0}' return d.name," \
                        "n.name".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (n)<-[:DEPARTMENT_IS]-(d:Disease)-[:ALIAS_IS]->(a:Alias) WHERE a.name='{0}' " \
                        "return d.name,n.name".format(e) for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (n)<-[:DEPARTMENT_IS]-(d:Disease)-[:HAS_SYMPTOM]->(s:Symptom) WHERE s.name='{0}' " \
                        "return d.name,n.name".format(e) for e in entities]
            elif label == "Complication":
                sql = ["MATCH (n)<-[:DEPARTMENT_IS]-(d:Disease)-[:HAS_COMPLICATION]->(c:Complication) WHERE " \
                        "c.name='{0}' return d.name,n.name".format(e) for e in entities]

        # 查询疾病
        elif intent == "query_disease":
            if label == "Alias":
                sql = ["MATCH (d:Disease)-[]->(s:Alias) WHERE s.name='{0}' return " \
                        "d.name".format(e) for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' return " \
                        "d.name".format(e) for e in entities]

        # 查询疾病描述
        elif intent == "disease_describe":
            if label == "Disease":
                sql = ["MATCH (d:Disease) WHERE d.name='{0}' return d.name,d.age,d.insurance,d.infection," \
                        "d.checklist,d.period,d.rate,d.money".format(e) for e in entities]
            elif label == "Alias":
                sql = ["MATCH (d:Disease)-[]->(a:Alias) WHERE a.name='{0}' return d.name,d.age," \
                        "d.insurance,d.infection,d.checklist,d.period,d.rate,d.money".format(e) for e in entities]
            elif label == "Symptom":
                sql = ["MATCH (d:Disease)-[]->(s:Symptom) WHERE s.name='{0}' return d.name,d.age," \
                        "d.insurance,d.infection,d.checklist,d.period,d.rate,d.money".format(e) for e in entities]
            elif label == "Complication":
                sql = ["MATCH (d:Disease)-[]->(c:Complication) WHERE c.name='{0}' return d.name," \
                        "d.age,d.insurance,d.infection,d.checklist,d.period,d.rate,d.money".format(e) for e in entities]

        return sql

    def searching(self, sqls):
        """
        执行cypher查询，返回结果
        :param sqls:
        :return:str
        """
        final_answers = []
        for sql_ in sqls:
            intent = sql_['intention']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data()
                answers += ress
            final_answer = self.answer_template(intent, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_template(self, intent, answers):
        """
        根据不同意图，返回不同模板的答案
        :param intent: 查询意图
        :param answers: 知识图谱查询结果
        :return: str
        """
        final_answer = ""
        if not answers:
            return ""
        # 查询症状
        if intent == "query_symptom":
            disease_dic = {}
            for data in answers:
                disease = data['d.name']
                symptom = data['s.name']
                if disease not in disease_dic:
                    disease_dic[disease] = [symptom]
                else:
                    disease_dic[disease].append(symptom)
            i = 0
            for disease, symptom_list in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "疾病 {0} 可能有如下症状：{1}\n".format(symptom, ','.join(list(set(symptom_list))))
                i += 1
        # 查询疾病
        if intent == "query_disease":
            disease_freq = {}
            for data in answers:
                disease = data["d.name"]
                disease_freq[disease] = disease_freq.get(disease, 0) + 1
            n = len(disease_freq.keys())
            if n != 0:
                freq = sorted(disease_freq.items(), key=lambda x: x[1], reverse=True)
                final_answer += "根据您描述的症状，最有可能患有以下疾病"
                for disease, _ in freq[:4]:
                    final_answer += "，{0}".format(disease)
                final_answer += "\n"
        # 查询治疗方法
        if intent == "query_cureway":
            disease_set = set()
            disease_treat_dic = {}
            disease_drug_dic = {}
            for data in answers:
                disease = data['d.name']
                treat = data["d.treatment"]
                drug = data["n.name"]
                if not treat and not drug:
                    continue
                disease_set.add(disease)
                if treat:
                    if disease not in disease_treat_dic:
                        disease_treat_dic[disease] = [treat]
                    elif treat not in disease_treat_dic[disease]:
                        disease_treat_dic[disease].append(treat)
                if drug:
                    if disease not in disease_drug_dic:
                        disease_drug_dic[disease] = [drug]
                    elif drug not in disease_drug_dic[disease]:
                        disease_drug_dic[disease].append(drug)
            i = 0
            for disease in disease_set:
                if i >= 10:
                    break
                treat_exist = disease in disease_treat_dic
                drug_exist = disease in disease_drug_dic
                if treat_exist or drug_exist:
                    final_answer += "关于疾病 {0} 的治疗\n".format(disease)
                if treat_exist:
                    final_answer += "治疗方法有：{0}\n".format(','.join(disease_treat_dic[disease][:]))
                if drug_exist:
                    final_answer += "可用药品包括：{0}\n".format(','.join(disease_drug_dic[disease][:]))
                i += 1

        # 查询治愈周期
        if intent == "query_period":
            disease_dic = {}
            for data in answers:
                disease = data['d.name']
                period = data['d.period']
                if not period:
                    continue
                if disease not in disease_dic:
                    disease_dic[disease] = [period]
                else:
                    disease_dic[disease].append(period)
            i = 0
            for disease, period in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "疾病 {0} 的治愈周期为：{1}\n".format(disease, ','.join(list(set(period))))
                i += 1
        # 查询治愈率
        if intent == "query_rate":
            disease_dic = {}
            for data in answers:
                disease = data['d.name']
                rate = data['d.rate']
                if not rate:
                    continue
                if disease not in disease_dic:
                    disease_dic[disease] = [rate]
                else:
                    disease_dic[disease].append(rate)
            i = 0
            for disease, rate in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "疾病 {0} 的治愈率为：{1}\n".format(disease, ','.join(list(set(rate))))
                i += 1
        # 查询检查项目
        if intent == "query_checklist":
            disease_dic = {}
            for data in answers:
                disease = data['d.name']
                checklist = data['d.checklist']
                if not checklist:
                    continue
                if disease not in disease_dic:
                    disease_dic[disease] = [checklist]
                else:
                    disease_dic[disease].append(checklist)
            i = 0
            for disease, checklist in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "疾病 {0} 的检查项目有：{1}\n".format(disease, ','.join(list(set(checklist))))
                i += 1
        # 查询科室
        if intent == "query_department":
            disease_dic = {}
            for data in answers:
                disease = data['d.name']
                department = data['n.name']
                if disease not in disease_dic:
                    disease_dic[disease] = [department]
                else:
                    disease_dic[disease].append(department)
            i = 0
            for disease, department in disease_dic.items():
                if i >= 10:
                    break
                final_answer += "疾病 {0} 所属科室有：{1}\n".format(disease, ','.join(list(set(department))))
                i += 1
        # 查询疾病描述
        if intent == "disease_describe":
            disease_infos = {}
            max_info_cnt = 0
            for data in answers:
                info_cnt = 0
                for v in data.values():
                    if v and v != "nan":
                        info_cnt += 1
                name = data['d.name']
                age = data['d.age']
                insurance = data['d.insurance']
                infection = data['d.infection']
                checklist = data['d.checklist']
                period = data['d.period']
                rate = data['d.rate']
                money = data['d.money']
                if name not in disease_infos:
                    disease_infos[name] = [age, insurance, infection, checklist, period, rate, money]
                else:
                    if info_cnt > max_info_cnt:
                        disease_infos[name] = [age, insurance, infection, checklist, period, rate, money]
                        max_info_cnt = info_cnt

            for k, v in disease_infos.items():
                disease_message = "疾病 {0} 的参考信息如下\n"
                final_answer += disease_message.format(k)
                info_list = ["发病人群", "医保", "传染性", "检查项目", "治愈周期", "治愈率", "费用"]
                info_message = "{0}: {1}\n"
                for i in range(len(v)):
                    if v[i] and v[i] != "nan":
                      final_answer += info_message.format(info_list[i], v[i])

        return final_answer
