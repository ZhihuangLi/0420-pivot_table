import pandas as pd
import numpy as np

writer = pd.ExcelWriter('DO测试数据0420_v7.xlsx')

# 1 处理问卷表，连接问卷表和tga表
q_path = 'C:\\Users\\74988\\Desktop\\工作数据\\DO\\0415画像报告\\DO3月问卷数据\\DO 1-A 3月.xlsx'
t_path = 'C:\\Users\\74988\\Desktop\\工作数据\\DO\\0415画像报告\\do玩家留存付费信息-明细-202104.csv'
q_data = pd.read_excel(q_path)
t_data = pd.read_csv(t_path)

# 表头拼接
q_question = list(q_data.columns)
q_answer = list(q_data.iloc[0,:])
q_title = []
for i in range(len(q_question)):
    q_title.append(q_answer[i]) if q_question[i][0:7] == 'Unnamed' else q_title.append(q_question[i])

# 表头修改
c_1 = { '基於第一印象，請問《緋紅戰線》的哪些方面對你有吸引力？':'畫風',
        '整體而言，這款遊戲與你玩過的類似遊戲相比，截至目前為止你的體驗如何？':'尖叫度',
        '你推薦身邊的朋友或同事玩這款遊戲的可能性為？':'推荐度',
        '您是否玩過以下遊戲？':'以上皆非',
        '當您體驗一款手遊時，有哪些樂趣元素是你喜歡的？':'【解謎/破解】成功解決謎題的樂趣',
        '你的性別是？': 'gender',
        '你的年齡在哪個範圍？': 'age'}
q_title = [c_1[i] if i in c_1 else i for i in q_title]
q_data.columns = q_title

# 选取变量
var = [ 'fpid',
        '畫風',
        '題材',
        '玩法',
        '尖叫度',
        '推荐度',
        'gender',
        'age',
        '公主連結',
        '第七史詩',
        '少女前線',
        '永遠的七日之都',
        '明日方舟',
        '夢境連結',
        '原神',
        '崩壞3',
        '雙重世界',
        '少女BANG DREAM',
        '【解謎/破解】成功解決謎題的樂趣',
        '【策略】在遊戲中思考、動腦子的樂趣',
        '【代入/劇情】沉浸於遊戲世界等設定中',
        '【創造】自主組合、創造遊戲內容',
        '【模擬現實】如體育/駕駛/經營等活動',
        '【成長變強】不斷提升自己等級、戰力等',
        '【社交】在遊戲中與好友互動的樂趣',
        '【探索/高自由】自由探索未知世界',
        '【攻略】攻略更加困難的關卡',
        '【考究】挖掘遊戲背後的細節和故事等',
        '【操作】通過操作技巧達成遊戲目標成就',
        '【收集】收集卡牌/人物/時裝等元素',
        '【競技/擊敗】在遊戲中戰勝、擊敗對手',
        '【養成/裝扮】照顧/打造遊戲中的角色',
        '【隨機】隨機帶來的不確定性的樂趣']

q_table = q_data.copy()[var].iloc[1:,:]
q_table = q_table.reset_index(drop=True)

# 缺失值处理和字段替换
na_var=['畫風',
        '題材',
        '玩法',
        '公主連結',
        '第七史詩',
        '少女前線',
        '永遠的七日之都',
        '明日方舟',
        '夢境連結',
        '原神',
        '崩壞3',
        '雙重世界',
        '少女BANG DREAM',
        '【解謎/破解】成功解決謎題的樂趣',
        '【策略】在遊戲中思考、動腦子的樂趣',
        '【代入/劇情】沉浸於遊戲世界等設定中',
        '【創造】自主組合、創造遊戲內容',
        '【模擬現實】如體育/駕駛/經營等活動',
        '【成長變強】不斷提升自己等級、戰力等',
        '【社交】在遊戲中與好友互動的樂趣',
        '【探索/高自由】自由探索未知世界',
        '【攻略】攻略更加困難的關卡',
        '【考究】挖掘遊戲背後的細節和故事等',
        '【操作】通過操作技巧達成遊戲目標成就',
        '【收集】收集卡牌/人物/時裝等元素',
        '【競技/擊敗】在遊戲中戰勝、擊敗對手',
        '【養成/裝扮】照顧/打造遊戲中的角色',
        '【隨機】隨機帶來的不確定性的樂趣']

for i in na_var: 
    q_table[i] = q_table[i].replace(i,1)
    q_table[i] = q_table[i].fillna(0)

# 处理核心玩家指标
q_table['尖叫度'] = q_table['尖叫度'].replace('太讚了，完全超出預期',5)
q_table['尖叫度'] = q_table['尖叫度'].replace('中規中矩',0)
q_table['尖叫度'] = q_table['尖叫度'].replace('完全不是我想要的',-5)

q_table['推荐度'] = q_table['推荐度'].replace('肯定會',10)
q_table['推荐度'] = q_table['推荐度'].replace('肯定不會',0)

# 增加新列：潜力玩家和核心玩家分类；六类竞品游戏经历玩家分类
n_1 = []
for i in range(len(q_table['畫風'])):
    if int(q_table['畫風'][i]+q_table['題材'][i]+q_table['玩法'][i]) <=0:
        n_1.append(-1)
    elif int(q_table['畫風'][i]+q_table['題材'][i]+q_table['玩法'][i]) >= 3:
        n_1.append(1)
    else:
        n_1.append(0)
q_table['潜力玩家'] = pd.DataFrame(n_1)

n_2 = []
for i in range(len(q_table['尖叫度'])):
    if q_table['尖叫度'][i]>=3 and q_table['推荐度'][i]>=5:
        n_2.append(1)
    else:
        n_2.append(0)
q_table['核心玩家'] = pd.DataFrame(n_2)

n_3 = []
for i in range(len(q_table['公主連結'])):
    if int(q_table['公主連結'][i]+q_table['第七史詩'][i]+q_table['少女前線'][i]) >0:
        n_3.append(1)
    else:
        n_3.append(0)
q_table['横板战斗类'] = pd.DataFrame(n_3)

n_4 = []
for i in range(len(q_table['永遠的七日之都'])):
    if int(q_table['永遠的七日之都'][i]+q_table['明日方舟'][i]+q_table['夢境連結'][i]) >0:
        n_4.append(1)
    else:
        n_4.append(0)
q_table['策略类'] = pd.DataFrame(n_4)

n_5 = []
for i in range(len(q_table['原神'])):
    if int(q_table['原神'][i])>0:
        n_5.append(1)
    else:
        n_5.append(0)
q_table['开放世界观'] = pd.DataFrame(n_5)

n_6 = []
for i in range(len(q_table['崩壞3'])):
    if int(q_table['崩壞3'][i]) >0:
        n_6.append(1)
    else:
        n_6.append(0)
q_table['动作类'] = pd.DataFrame(n_6)

n_7 = []
for i in range(len(q_table['雙重世界'])):
    if int(q_table['雙重世界'][i]) >0:
        n_7.append(1)
    else:
        n_7.append(0)
q_table['卡牌收集类'] = pd.DataFrame(n_7)

n_8 = []
for i in range(len(q_table['少女BANG DREAM'])):
    if int(q_table['少女BANG DREAM'][i])>0:
        n_8.append(1)
    else:
        n_8.append(0)
q_table['音乐类'] = pd.DataFrame(n_8)

# 增加筛选条件
# t_data = t_data[(t_data['install_countrycode']=='tw')]

q_t_data = pd.merge(q_table,t_data,on='fpid')
q_table.to_excel(writer,'问卷数据',index=False)
t_data.to_excel(writer,'tga数据',index=False)
q_t_data.to_excel(writer,'问卷-tga数据',index=False)

# 2 计算tga数据和问卷数据的留存付费折算系数

# 留存折算系数
v_s_1 = ['fpid','is_2r','is_3r','is_7r']
af_s_1 = {'fpid':np.size,'is_2r':np.sum,'is_3r':np.sum,'is_7r':np.sum}
tga_survival_t = pd.pivot_table(t_data,index=['install_countrycode'],values=v_s_1,aggfunc=af_s_1,margins=True)
q_t_survival_t = pd.pivot_table(q_t_data,index=['install_countrycode'],values=v_s_1,aggfunc=af_s_1,margins=True)
survival_data = pd.DataFrame({'tga':list(tga_survival_t.iloc[-1,:]),'q':list(q_t_survival_t.iloc[-1,:])},index=tga_survival_t.columns)

survival_data = survival_data.T
a1 = survival_data['fpid']
a2 = survival_data['is_2r']
a3 = survival_data['is_3r']
a7 = survival_data['is_7r']
s2 = a2/a1
s3 = a3/a1
s7 = a7/a1
survival_t=pd.DataFrame({'次日':list(s2),'三日':list(s3),'七日':list(s7)},index=['tga','问卷'])
survival_t = survival_t.T
tga_s = survival_t['tga']
q_s = survival_t['问卷']
s_index = tga_s/q_s
survival_index_t=pd.DataFrame({'tga留存率':list(tga_s),'问卷留存率':list(q_s),'折算系数':list(s_index)},index=['次日','三日','七日'])

# 付费折算系数
pay_value = {}
range_var = ['fpid','_1pay_amount_cum','_2pay_amount_cum','_3pay_amount_cum','_4pay_amount_cum','_5pay_amount_cum','_6pay_amount_cum','_7pay_amount_cum','_8pay_amount_cum','_1ispay','_2ispay','_3ispay','_4ispay','_5ispay','_6ispay','_7ispay','_8ispay']
# 需要创造一个字典name将原名和中文名一一对应
chinese_name = ['fpid','付费金额1','付费金额2','付费金额3','付费金额4','付费金额5','付费金额6','付费金额7','付费金额0','付费人数1','付费人数2','付费人数3','付费人数4','付费人数5','付费人数6','付费人数7','付费人数8']
name = {}
for i in range(len(range_var)):
    name[range_var[i]] = chinese_name[i]

for i in range(len(range_var)):
    if range_var[i] == 'fpid':
        pay_value[range_var[i]] = np.size
    else:
        pay_value[range_var[i]] = np.sum

tga_pay_t = pd.pivot_table(t_data
                           ,index=['install_countrycode']
                           ,values=range_var
                           ,aggfunc=pay_value
                           ,margins=True)
q_pay_t = pd.pivot_table(q_t_data
                           ,index=['install_countrycode']
                           ,values=range_var
                           ,aggfunc=pay_value
                           ,margins=True)

tga_pay_t = tga_pay_t.T
q_pay_t = q_pay_t.T

new_name=[]
for i in list(tga_pay_t.index):
    new_name.append(name.get(i))

pay_data = pd.DataFrame({'tga':list(tga_pay_t.iloc[:,-1]),'q':list(q_pay_t.iloc[:,-1])},index=new_name)
pay_data.sort_index(inplace=True)

# 付费率
pay_date = ['1日','2日','3日','4日','5日','6日','7日','8日']
tga_p_rate=[]
q_p_rate=[]
for i in range(2):
    for j in range(1,9):
        if i == 0:          
            tga_p_rate.append(pay_data.iloc[j,i]/pay_data.iloc[0,i])
        else:
            q_p_rate.append(pay_data.iloc[j,i]/pay_data.iloc[0,i])
p_index=np.array(tga_p_rate)/np.array(q_p_rate)
pay_rate_t=pd.DataFrame({'tga付费率':tga_p_rate,'问卷付费率':q_p_rate,'折算系数':p_index},index=pay_date)

# ARPU
tga_arpu=[]
q_arpu=[]
for i in range(2):
    for j in range(9,len(pay_data)):
        if i == 0:          
            tga_arpu.append(pay_data.iloc[j,i]/pay_data.iloc[0,i])
        else:
            q_arpu.append(pay_data.iloc[j,i]/pay_data.iloc[0,i])
arpu_index=np.array(tga_arpu)/np.array(q_arpu)
arpu_index_t=pd.DataFrame({'tgaARPU':tga_arpu,'问卷ARPU':q_arpu,'折算系数':arpu_index},index=pay_date)

# ARPPU
tga_arppu=[]
q_arppu=[]
for i in range(2):
    for j in range(1,9):
        if i == 0:          
            tga_arppu.append(pay_data.iloc[j+8,i]/pay_data.iloc[j,i])
        else:
            q_arppu.append(pay_data.iloc[j+8,i]/pay_data.iloc[j,i])
arppu_index=np.array(tga_arppu)/np.array(q_arppu)
arppu_index_t=pd.DataFrame({'tgaARPU':tga_arppu,'问卷ARPU':q_arppu,'折算系数':arppu_index},index=pay_date)

pay_index_t = pd.concat([pay_rate_t,arpu_index_t,arppu_index_t],axis=1)

survival_index_t.to_excel(writer,'问卷-tga留存折算系数')
pay_index_t.to_excel(writer,'问卷-tga付费折算系数')

# 构造计算函数
# 单选留存
def single_survival(data,index,value,function,sheet_name):
    # 留存透视表
    q_tga_t = pd.pivot_table(data,index=index,values=value,aggfunc=function,margins=True)
    # 计算留存率
    a1 = q_tga_t['fpid']
    a2 = q_tga_t['is_2r']
    a3 = q_tga_t['is_3r']
    a7 = q_tga_t['is_7r']
    # 添加尖叫度
    j1 = q_tga_t['尖叫度']

    s2 = a2/a1*survival_index_t.iloc[0,2]
    s3 = a3/a1*survival_index_t.iloc[1,2]
    s7 = a7/a1*survival_index_t.iloc[2,2]

    name = q_tga_t.index

    q_tga_survival_t = pd.DataFrame({'总人数':list(a1),'次日人数':list(a2),'三日人数':list(a3),'七日人数':list(a7),
                                    '次日留存率':list(s2),'三日留存率':list(s3),'七日留存率':list(s7),'尖叫度均值':list(j1)},index=name)

    q_tga_survival_t.to_excel(writer,sheet_name)
    print(sheet_name+'保存成功')
    pass

# 将付费相关变量替换成中文，方便透视表排序
range_var = ['fpid',
            '_1pay_amount_cum','_2pay_amount_cum','_3pay_amount_cum','_4pay_amount_cum',
            '_5pay_amount_cum','_6pay_amount_cum','_7pay_amount_cum','_8pay_amount_cum',
            '_1ispay','_2ispay','_3ispay','_4ispay','_5ispay','_6ispay','_7ispay','_8ispay']

chinese_name = ['fpid',
            '付费金额1','付费金额2','付费金额3','付费金额4',
            '付费金额5','付费金额6','付费金额7','付费金额8',
            '付费人数1','付费人数2','付费人数3','付费人数4','付费人数5','付费人数6','付费人数7','付费人数8']
pay_value = {}
name = {}
for i in range(len(range_var)):
    name[range_var[i]] = chinese_name[i]

for i in range(len(range_var)):
    if range_var[i] == 'fpid':
        pay_value[range_var[i]] = np.size
    else:
        pay_value[range_var[i]] = np.sum

new_name=[]
for i in list(tga_pay_t.index):
    new_name.append(name.get(i))

pay_date = ['1日','2日','3日','4日','5日','6日','7日','8日']

# 单选付费
def single_pay(data,index,value,function,sheet_name1,sheet_name2,sheet_name3):
    # 付费透视表
    q_tga_pay_t = pd.pivot_table(data,index=index,values=value,aggfunc=function,margins=True)
    global new_name,pay_date
    q_tga_pay_t.columns = new_name.copy()

    index_name = q_tga_pay_t.index

    q_tga_pay_t = q_tga_pay_t.T
    q_tga_pay_t.sort_index(inplace=True)
    q_tga_pay_t1_T  = q_tga_pay_t.T

    # 付费率
    q_tga_pay_rate={}
    for i in range(1,9):
        q_tga_pay_rate[i] = np.array(q_tga_pay_t.iloc[i,:])/np.array(q_tga_pay_t.iloc[0,:])*pay_index_t.iloc[i-1,2]
    q_tga_pay_rate_t = pd.DataFrame(q_tga_pay_rate,index=index_name)
    q_tga_pay_rate_t.columns = pay_date
    q_tga_pay_rate_t=q_tga_pay_t1_T.join(q_tga_pay_rate_t)

    # ARPU
    q_tga_arpu={}
    for i in range(9,len(q_tga_pay_t)):
        q_tga_arpu[i] = np.array(q_tga_pay_t.iloc[i,:])/np.array(q_tga_pay_t.iloc[0,:])*pay_index_t.iloc[i-9,5]
    q_tga_arpu_t = pd.DataFrame(q_tga_arpu,index=index_name)
    q_tga_arpu_t.columns = pay_date
    q_tga_arpu_t=q_tga_pay_t1_T.join(q_tga_arpu_t)

    # ARPPU
    q_tga_arppu={}
    for i in range(1,9):
        q_tga_arppu[i] = np.array(q_tga_pay_t.iloc[i+8,:])/np.array(q_tga_pay_t.iloc[i,:])*pay_index_t.iloc[i-1,8]
    q_tga_arppu_t = pd.DataFrame(q_tga_arppu,index=index_name)
    q_tga_arppu_t.columns = pay_date
    q_tga_arppu_t=q_tga_pay_t1_T.join(q_tga_arppu_t)

    q_tga_pay_rate_t.to_excel(writer,sheet_name1)
    print(sheet_name1+'保存成功')
    q_tga_arpu_t.to_excel(writer,sheet_name2)
    print(sheet_name2+'保存成功')
    q_tga_arppu_t.to_excel(writer,sheet_name3)
    print(sheet_name3+'保存成功')
    pass

# 多选留存
def multiple_survival(data,variable,value,function,sheet_name):
    q_tga_final = {}
    for i in variable:
        q_tga_t = pd.pivot_table(q_t_data,index=i,values=value,aggfunc=function)
        q_tga_final[i] = list(q_tga_t.iloc[-1,:])
    q_tga_survival_t1 = pd.DataFrame(q_tga_final,index=value)
    q_tga_survival_t1 = q_tga_survival_t1.T
    # 计算留存率
    a1 = q_tga_survival_t1['fpid']
    a2 = q_tga_survival_t1['is_2r']
    a3 = q_tga_survival_t1['is_3r']
    a7 = q_tga_survival_t1['is_7r']
    s2 = a2/a1*survival_index_t.iloc[0,2]
    s3 = a3/a1*survival_index_t.iloc[1,2]
    s7 = a7/a1*survival_index_t.iloc[2,2]
    q_tga_survival_t1 = pd.DataFrame({'总人数':list(a1),'次日人数':list(a2),'三日人数':list(a3),'七日人数':list(a7),
                                    '次日留存率':list(s2),'三日留存率':list(s3),'七日留存率':list(s7)},index=variable)

    q_tga_survival_t1.to_excel(writer,sheet_name)
    print(sheet_name+'保存成功')
    pass

# 多选付费
def multiple_pay(data,variable,value,function,sheet_name1,sheet_name2,sheet_name3):
    q_tga_pay_final = {}
    for i in variable:
        q_tga_pay_t1 = pd.pivot_table(data,index=i,values=value,aggfunc=function)
        q_tga_pay_t1 = q_tga_pay_t1.T
        q_tga_pay_t1.sort_index(inplace=True)
        q_tga_pay_final[i] = list(q_tga_pay_t1.iloc[:,-1])

    q_tga_pay_t1 = pd.DataFrame(q_tga_pay_final,index=new_name)
    q_tga_pay_t1.sort_index(inplace=True)
    q_tga_pay_t1_T  = q_tga_pay_t1.T

    # 付费率
    q_tga_pay_rate1={}
    for i in range(1,9):
        q_tga_pay_rate1[i] = np.array(q_tga_pay_t1.iloc[i,:])/np.array(q_tga_pay_t1.iloc[0,:])*pay_index_t.iloc[i-1,2]
    q_tga_pay_rate_t1 = pd.DataFrame(q_tga_pay_rate1,index=variable)
    q_tga_pay_rate_t1.columns = pay_date
    q_tga_pay_rate_t1=q_tga_pay_t1_T.join(q_tga_pay_rate_t1)

    # ARPU
    q_tga_arpu1={}
    for i in range(9,len(q_tga_pay_t1)):
        q_tga_arpu1[i] = np.array(q_tga_pay_t1.iloc[i,:])/np.array(q_tga_pay_t1.iloc[0,:])*pay_index_t.iloc[i-9,5]
    q_tga_arpu_t1 = pd.DataFrame(q_tga_arpu1,index=variable)
    q_tga_arpu_t1.columns = pay_date
    q_tga_arpu_t1=q_tga_pay_t1_T.join(q_tga_arpu_t1)

    # ARPPU
    q_tga_arppu1={}
    for i in range(1,9):
        q_tga_arppu1[i] = np.array(q_tga_pay_t1.iloc[i+8,:])/np.array(q_tga_pay_t1.iloc[i,:])*pay_index_t.iloc[i-1,8]
    q_tga_arppu_t1 = pd.DataFrame(q_tga_arppu1,index=variable)
    q_tga_arppu_t1.columns = pay_date
    q_tga_arppu_t1=q_tga_pay_t1_T.join(q_tga_arppu_t1)

    q_tga_pay_rate_t1.to_excel(writer,sheet_name1)
    print(sheet_name1+'保存成功')
    q_tga_arpu_t1.to_excel(writer,sheet_name2)
    print(sheet_name2+'保存成功')
    q_tga_arppu_t1.to_excel(writer,sheet_name3)
    print(sheet_name3+'保存成功')
    pass

# 多选中的单选分布
def multiple_single(data,variable,index,value,function,sheet_name):
    q_tga_final = {}
    for i in variable:
        q_tga_t = pd.pivot_table(data[(data[i]==1)],index=index,values=value,aggfunc=function,margins=True)
        q_tga_final[i] = list(q_tga_t.iloc[:,-1])
    index_name = q_tga_t.index
    q_tga_survival_t1 = pd.DataFrame(q_tga_final,index=index_name)
    q_tga_survival_t1 = q_tga_survival_t1.T

    q_tga_survival_t1.to_excel(writer,sheet_name)
    print(sheet_name+'保存成功')
    pass

# 开始使用函数计算

# 核心玩家留存率和尖叫度均值
i_s_1 = ['核心玩家']
v_s_1 = ['fpid','is_2r','is_3r','is_7r','尖叫度']
f_s_1 = {'fpid':np.size,'is_2r':np.sum,'is_3r':np.sum,'is_7r':np.sum,'尖叫度':np.mean}
single_survival(data=q_t_data,index=i_s_1,value=v_s_1,function=f_s_1,sheet_name='核心玩家留存率和尖叫度均值')

# 潜力玩家留存率和尖叫度均值
i_s_2 = ['潜力玩家']
v_s_2 = ['fpid','is_2r','is_3r','is_7r','尖叫度']
f_s_2 = {'fpid':np.size,'is_2r':np.sum,'is_3r':np.sum,'is_7r':np.sum,'尖叫度':np.mean}
single_survival(data=q_t_data,index=i_s_2,value=v_s_2,function=f_s_2,sheet_name='潜力玩家留存率和尖叫度均值')

# 核心玩家付费情况
i_p_1 = ['核心玩家']
v_p_1 = range_var.copy()
f_p_1 = pay_value.copy()
single_pay(data=q_t_data,index=i_p_1,value=v_p_1,function=f_p_1,
            sheet_name1='核心玩家付费率',sheet_name2='核心玩家ARPU',sheet_name3='核心玩家ARPPU')

# 潜力玩家付费情况
i_p_2 = ['潜力玩家']
v_p_2 = range_var.copy()
f_p_2 = pay_value.copy()
single_pay(data=q_t_data,index=i_p_2,value=v_p_2,function=f_p_2,
            sheet_name1='潜力玩家付费率',sheet_name2='潜力玩家ARPU',sheet_name3='潜力玩家ARPPU')


# 游戏类型留存情况
v = [   '横板战斗类',
        '策略类',
        '开放世界观',
        '动作类',
        '卡牌收集类',
        '音乐类']
v_s_1 = ['fpid','is_2r','is_3r','is_7r']
f_s_1 = {'fpid':np.size,'is_2r':np.sum,'is_3r':np.sum,'is_7r':np.sum}
multiple_survival(data=q_t_data,variable=v,value=v_s_1,function=f_s_1,sheet_name='游戏类型留存情况')

# 游戏类型付费情况
v = [   '横板战斗类',
        '策略类',
        '开放世界观',
        '动作类',
        '卡牌收集类',
        '音乐类']
v_p_1 = range_var.copy()
f_p_1 = pay_value.copy()
multiple_pay(data=q_t_data,variable=v,value=v_p_1,function=f_p_1,
            sheet_name1='游戏类型付费率',sheet_name2='游戏类型ARPU',sheet_name3='游戏类型ARPPU')

# 游戏类型-年龄分布
v = [   '横板战斗类',
        '策略类',
        '开放世界观',
        '动作类',
        '卡牌收集类',
        '音乐类']

i_s_1 = ['age']
v_s_1 = ['fpid']
f_s_1 = {'fpid':np.size}
multiple_single(data=q_t_data,variable=v,index=i_s_1,value=v_p_1,function=f_p_1,sheet_name='游戏类型-年龄分布')

writer.save()
