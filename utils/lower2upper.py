"""
本函数将字典或嵌套字典中的key从下划线命名法装换为大驼峰命名法，
以便MatCloud MongoDB 的数据查询。
"""
import re


class Lower2Upper:
    def __init__(self):
        self.key_list = []

    def get_all_keys(self, query_dict):
        if isinstance(query_dict, dict):
            for key in query_dict.keys():
                value = query_dict[key]
                self.key_list.append(key)
                self.get_all_keys(value)
        elif isinstance(query_dict, list):
            for q in query_dict:
                if isinstance(q, dict):
                    for key in q.keys():
                        value = q[key]
                        self.key_list.append(key)
                        self.get_all_keys(value)

    def lower2upper(self, query):
        self.get_all_keys(query)

        query_list = str(query).split('\'')
        for i, token in enumerate(query_list):
            if token in self.key_list and token[0].isalpha():
                token_list = re.split('([._])', token)
                # for j, t in enumerate(token_list):
                #     if i != '.' or i != '_':
                #         token_list[j] = t.capitalize()
                new_token = "".join(t.capitalize() for j, t in enumerate(token_list) if i != '.' or i != '_')
                query_list[i] = new_token.replace('_', '')

        return eval('\''.join(query_list))


if __name__ == '__main__':
    q = {'$and': [{'centering': {'$eq': 'FaceCentered'}},
                  {'$or': [{'formula': {'$eq': 'Cu4'}}, {'complete_formula': {'$eq': 'Cu4'}}]}]}
    lu = Lower2Upper()
    print(q)
    print(lu.lower2upper(q))

