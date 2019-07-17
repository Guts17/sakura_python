import pymongo
 
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sakura"]
mycol = mydb["video"]
 
mydict = {
		"video_name": "丝袜视界",
		"video_aliasname": "别名：裤袜视界/赏袜/みるタイツ",
		"video_updateinfo": "更新至10话",
		"video_region": "日本",
		"video_type": "校园,青春,美少女",
		"video_years": "2019",
		"video_tag": "日语,tv",
		"video_index": "s动漫",
		"video_desc": "《丝袜视界》讲述以日推上的忠实表现丝袜魅力的超人气真实系裤袜控画师よむ的作品为原案，同道中人丸户史明输出的脚本为基础而制作的满载着JK能量的青春动画，制作方是TRUSS，主要讲述了春天成为高二生的蓝川莲、文体兼优的中红由亚、开朗活泼的大小姐萌黄帆美三人的度过的一段无可替代的时光。4月。下雨的早晨。开始凋零的樱花被雨滴打落，漂浮在积水之上。学生们撑着五颜六色的雨伞，穿过高中的校门。早啊，莲。鞋柜前，裤袜湿透的莲被由亚搭话。略显忧郁的莲回过头去，看到全身湿透的帆美蹦蹦跳跳地走来，热闹地说着话。3个女学生没啥营养的对话，向教室宣告了新学期的来临。少女们无可替代的宝贵时间向前飞逝，季节渐渐转变..."
	}
 
x = mycol.insert_one(mydict) 
print(x)