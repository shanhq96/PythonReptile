def formatUrbanDistrict(city_short_name,urbanDistrictTemp):
    urbanDistrictTemp1 = urbanDistrictTemp
    urbanDistrictTemp = urbanDistrictTemp.replace("区","")
    urbanDistrict = None
    if(city_short_name == "bj"):
        if(urbanDistrictTemp != "东城" and urbanDistrictTemp != "西城" and urbanDistrictTemp != "朝阳"
            and urbanDistrictTemp != "海淀" and urbanDistrictTemp != "丰台" and urbanDistrictTemp != "通州"
            and urbanDistrictTemp != "石景山" and urbanDistrictTemp != "昌平" and urbanDistrictTemp != "大兴"
            and urbanDistrictTemp != "顺义" and urbanDistrictTemp != "房山" and urbanDistrictTemp != "门头沟"
            and urbanDistrictTemp != "平谷" and urbanDistrictTemp != "怀柔" and urbanDistrictTemp != "密云"
            and urbanDistrictTemp != "延庆"):
            urbanDistrict = "北京周边"
        else:
            urbanDistrict = urbanDistrictTemp1
    elif(city_short_name == "sz"):
        if(urbanDistrictTemp != "龙岗" and urbanDistrictTemp != "南山" and urbanDistrictTemp != "福田"
            and urbanDistrictTemp != "宝安" and urbanDistrictTemp != "罗湖" and urbanDistrictTemp != "坪山"
            and urbanDistrictTemp != "盐田" and urbanDistrictTemp != "光明新" and urbanDistrictTemp != "大鹏新"):
            urbanDistrict = "深圳周边"
        else:
            urbanDistrict = urbanDistrictTemp1
    elif(city_short_name == "sh"):
        if(urbanDistrictTemp != "浦东" and urbanDistrictTemp != "闵行" and urbanDistrictTemp != "徐汇"
           and urbanDistrictTemp != "宝山" and urbanDistrictTemp != "松江" and urbanDistrictTemp != "嘉定"
           and urbanDistrictTemp != "普陀" and urbanDistrictTemp != "杨浦" and urbanDistrictTemp != "长宁"
           and urbanDistrictTemp != "虹口" and urbanDistrictTemp != "静安" and urbanDistrictTemp != "黄浦"
           and urbanDistrictTemp != "闸北" and urbanDistrictTemp != "奉贤" and urbanDistrictTemp != "青浦"
           and urbanDistrictTemp != "金山" and urbanDistrictTemp != "崇明"):
            urbanDistrict = "上海周边"
        else:
            urbanDistrict = urbanDistrictTemp1
    elif(city_short_name == "gz"):
        if(urbanDistrictTemp != "白云" and urbanDistrictTemp != "海珠" and urbanDistrictTemp != "天河"
           and urbanDistrictTemp != "番禺" and urbanDistrictTemp != "越秀" and urbanDistrictTemp != "花都"
           and urbanDistrictTemp != "增城" and urbanDistrictTemp != "荔湾" and urbanDistrictTemp != "南沙"
           and urbanDistrictTemp != "黄埔" and urbanDistrictTemp != "从化"):
            urbanDistrict = "广州周边"
        else:
            urbanDistrict = urbanDistrictTemp1
    return  urbanDistrict