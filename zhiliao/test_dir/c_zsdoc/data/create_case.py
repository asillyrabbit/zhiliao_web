# 药房信息，每次生成用例前，根据实际情况修改
supplier_infos_1 = {
    "type": "中药饮片",
    "sup_name": "国药江康【江苏】",
    "details": {"枸杞子": 15, "夏枯草": 15, "菊花": 20},
    "total": ['7'],
    "sign": ['1', '2', '3', '4'],
    "brew": ['100 ml/袋', '200 ml/袋'],
    "method": [0, 1],
    "flag": [0, 1]
}

supplier_infos_2 = {
    "type": "配方颗粒",
    "sup_name": "广誉远真爱门诊部【西安】",
    "details": {"菊花": 20, "薄荷": 20, "山药": 13},
    "total": ['7'],
    "sign": ['1', '2', '3'],
    "method": [0, 1],
}


# 生成测试用例
def create_case(supplier_infos):
    """
    仅支持饮片、颗粒用例生成
    其它剂型，如膏方制作费，每个药房的计算规则都不一样，实现成本大，待定。
    """
    case_list = []
    type = supplier_infos['type']
    sup_name = supplier_infos['sup_name']
    title = "真爱门诊，颗粒"  # 需根据实际情况进行修改
    i = 1

    if type == "中药饮片":
        for method in supplier_infos['method']:
            if method == 0:
                t_m = "内服"
            else:
                t_m = "外用"
            for flag in supplier_infos['flag']:
                if flag == 0:
                    t_f = "代煎"
                else:
                    t_f = "自煎"
                for total in supplier_infos['total']:
                    case_dict = {}
                    case_dict["title"] = f'{i}.{title}（{total}剂，{t_m}，{t_f}）'
                    case_dict["drug_type"] = type
                    case_dict["sup_name"] = sup_name
                    case_dict["details"] = supplier_infos['details']
                    case_dict["med_type"] = method
                    case_dict["brew_flag"] = flag
                    case_dict["brew_list"] = supplier_infos['brew']
                    case_dict["tot_num"] = total
                    case_dict["sign_num"] = supplier_infos['sign']
                    case_list.append(case_dict)
                    i = i + 1

    if type == "配方颗粒":
        for method in supplier_infos['method']:
            if method == 0:
                t_m = "内服"
            else:
                t_m = "外用"
            for total in supplier_infos['total']:
                case_dict = {}
                case_dict["title"] = f'{i}.{title}（{total}剂，{t_m}）'
                case_dict["drug_type"] = type
                case_dict["sup_name"] = sup_name
                case_dict["details"] = supplier_infos['details']
                case_dict["med_type"] = method
                case_dict["tot_num"] = total
                case_dict["sign_num"] = supplier_infos['sign']
                case_list.append(case_dict)
                i = i + 1

    return case_list


case = create_case(supplier_infos_2)

print(case)
