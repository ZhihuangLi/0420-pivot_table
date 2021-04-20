'''
以DO报告数据为例，原始数据包括：tga数据+问卷数据

代码主要分为四个部分：
1. 处理问卷数据，输出清洗后的问卷表，tga表，和问卷-tga连接表
2. 计算折算系数，输出留存折算系数表和付费折算系数表
3. 以单选题分类，输出留存率/付费率/ARPU/ARPPU表
4. 以多选题分类，输出留存率/付费率/ARPU/ARPPU表
5. 以多选题中的单选题分类，输出如游戏类型-年龄分布

具体流程：
1. 处理问卷数据：

  1.1 将q_path和t_path修改成问卷数据和tga数据路径
  1.2 用excel打开问卷数据，选取需要改名的变量列名按照顺序复制到c_1和c_2，c1为列表类型，c2为字典类型，如果是多选题，需要将问题复制下来改成第一个选项
  1.3 选取需要的变量名var（记得是改名后的变量名）
  1.4 选取需要缺失值处理和字段替换的变量名na_var(一般多选题需要)
  1.5 处理核心玩家指标时要注意'replace'里面填写的字段要和excel表格里面的字段对应清楚
  1.6 连接成q_t_data时注意on='UID'，tga或问卷里的连接字段可能不同

2. 计算折算系数：
  2.1 不用怎么改，保持和tga数据的字段名对齐即可

3. 单选题分类：

  3.1 选取留存分类的字段名 i_s_1 (注:i=index,s=survival),v_s_1和f_s_1代表value和function一般不用改
  3.2 修改表名，输出
  3.3 如果还有其他单选题分类的字段，直接再次调用函数
 
4. 多选题分类：

  4.1 选取变量的分类v
  4.2 修改表名，输出
  4.3 如果还有其他多选题分类的字段，直接再次调用函数
'''

