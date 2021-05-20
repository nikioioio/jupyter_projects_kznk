import pandas as pd
#cons,KONH,current_date
def calc_price(args):
    cons = args[0]
    KONH = args[1]
    current_date = args[2]
    KONP = args[3]
    MARM = args[4]
    
    
    for ind in cons.index:
        Konh_ = KONH[(KONH['Материал']==cons.loc[ind,'Материал'])&(KONH['Действ. с'].dt.year==current_date.year)]
        if f_KONH(Konh_,'округ',cons.loc[ind,'округ'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH(Konh_,'округ',cons.loc[ind,'округ'])[1]
            continue
        elif f_KONH(Konh_,'Завод',cons.loc[ind,'Завод'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH(Konh_,'Завод',cons.loc[ind,'Завод'])[1]
            continue
        else:
            for ind1 in Konh_.index:
                if Konh_.loc[ind1,'округ']=='пусто'  and Konh_.loc[ind1,'Завод']=='пусто':
                    cons.loc[ind,'номер записи условий'] = Konh_.loc[ind1,'Номер записи условий']
                    break

    for ind in cons.index:
        ar = KONP[KONP['Номер записи условий']==cons.loc[ind,'номер записи условий']]
        if len(ar)>0:
            cons.loc[ind,'цена без учета коэф.пересчата'] = ar['Сумма условия'].values[0]/ar['Единица цены'].values[0]           
            cons.loc[ind,'единица измерения закупки'] = ar['Единица измерения'].values[0]
            #рассчет плановой цены
            if cons.loc[ind,'Базовая ЕИ']==cons.loc[ind,'единица измерения закупки']:
                cons.loc[ind,'Плановая цена'] = cons.loc[ind,'цена без учета коэф.пересчата']
            else:
                MARM_  = MARM[(MARM['Материал']==cons.loc[ind,'Материал'])&(MARM['Альтернативная ЕИ']==cons.loc[ind,'единица измерения закупки'])]
                if len(MARM_)>0:
                    cons.loc[ind,'Плановая цена'] = (cons.loc[ind,'цена без учета коэф.пересчата']/MARM_['Счетчик'].values[0])*MARM_['Знаменатель'].values[0] 
                
                
    cons.fillna(0,inplace=True)
    return cons        


#cons,KONH,current_date
def calc_price_fast(args):
    cons = args[0]
    KONH = args[1]
    current_date = args[2]
    KONP = args[3]
    MARM = args[4]
    
    for ind in cons.index:
        try:
        
            Konh_ = KONH[cons.loc[ind,'Материал']+str(current_date.year)]
        except KeyError:
            Konh_ = pd.DataFrame()
        if f_KONH(Konh_,'округ',cons.loc[ind,'округ'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH(Konh_,'округ',cons.loc[ind,'округ'])[1]
            continue
        elif f_KONH(Konh_,'Завод',cons.loc[ind,'Завод'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH(Konh_,'Завод',cons.loc[ind,'Завод'])[1]
            continue
        else:
            for ind1 in Konh_.index:
                if Konh_.loc[ind1,'округ']=='пусто'  and Konh_.loc[ind1,'Завод']=='пусто':
                    cons.loc[ind,'номер записи условий'] = Konh_.loc[ind1,'Номер записи условий']
                    break
    
    for ind in cons.index:
    
        try:
        
            ar = KONP[cons.loc[ind,'номер записи условий']]
        except KeyError:
            ar = pd.DataFrame()
        
        if len(ar)>0:
            cons.loc[ind,'цена без учета коэф.пересчата'] = ar['Сумма условия'].values[0]/ar['Единица цены'].values[0]           
            cons.loc[ind,'единица измерения закупки'] = ar['Единица измерения'].values[0]
            #рассчет плановой цены
            if cons.loc[ind,'Базовая ЕИ']==cons.loc[ind,'единица измерения закупки']:
                cons.loc[ind,'Плановая цена'] = cons.loc[ind,'цена без учета коэф.пересчата']
            else:
                try:
        
                    MARM_  = MARM[cons.loc[ind,'Материал']+cons.loc[ind,'единица измерения закупки']]
                except KeyError:
                    MARM_ = pd.DataFrame()
                
                if len(MARM_)>0:
                    cons.loc[ind,'Плановая цена'] = (cons.loc[ind,'цена без учета коэф.пересчата']*MARM_['Счетчик'].values[0])*MARM_['Знаменатель'].values[0] 
                
                
    cons.fillna(0,inplace=True)
    return cons 



def f_KONH (KONH,name_col_KONH,value):
    i = 1
    if len(KONH)==0:
            return ('пусто','0')
    for ind in KONH.index:
        if i ==len(KONH):
            return ('пусто','0')
        if KONH.loc[ind,name_col_KONH] == value:
            return (KONH.loc[ind,name_col_KONH],KONH.loc[ind,'Номер записи условий'])
        i+=1
        
        
        
        

def calc_price_super_fast(args):

    cons = args[0]
    KONH_po = args[1]
    KONH_s = args[2]
    current_date = args[3]
    KONP = args[4]
    MARM = args[5]
    for ind in cons.index: 
        try:
            Konh_ = KONH_po.xs([cons.at[ind,'Материал'],str(current_date.year)])
    #         print(len(Konh_))
        except KeyError:
            Konh_ = pd.DataFrame() 
        try:
            Konh_1 = KONH_s.xs([cons.at[ind,'Материал'],str(current_date.year)])
    #         print(len(Konh_))
        except KeyError:
            Konh_1 = pd.DataFrame() 
        
        
        if f_KONH_fast(Konh_1,'округ',cons.loc[ind,'округ'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH_fast(Konh_1,'округ',cons.loc[ind,'округ'])[1]
            continue
        if f_KONH_fast(Konh_,'округ',cons.loc[ind,'округ'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH_fast(Konh_,'округ',cons.loc[ind,'округ'])[1]
            continue
        
        
        
        elif f_KONH_fast(Konh_1,'Завод',cons.loc[ind,'Завод'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH_fast(Konh_1,'Завод',cons.loc[ind,'Завод'])[1]
            continue
        elif f_KONH_fast(Konh_,'Завод',cons.loc[ind,'Завод'])[0]!='пусто':
            cons.loc[ind,'номер записи условий'] = f_KONH_fast(Konh_,'Завод',cons.loc[ind,'Завод'])[1]
            continue
        
        
        else:
            for row in Konh_1.itertuples():
                if row.округ=='пусто'  and row.Завод =='пусто':
                    cons.loc[ind,'номер записи условий'] = row.Номер_записи_условий
                    break
            for row in Konh_.itertuples():
                if row.округ=='пусто'  and row.Завод =='пусто':
                    cons.loc[ind,'номер записи условий'] = row.Номер_записи_условий
                    break

    for ind in cons.index:
        try:
            ar = KONP.xs(cons.loc[ind,'номер записи условий'])

        except KeyError:
            ar = pd.DataFrame()     

        if len(ar)>0:

            cons.loc[ind,'цена без учета коэф.пересчата'] = ar['Сумма условия']/ar['Единица цены']
            cons.loc[ind,'единица измерения закупки'] = ar['Единица измерения']
            #рассчет плановой цены
            if cons.loc[ind,'Базовая ЕИ']==cons.loc[ind,'единица измерения закупки']:
                cons.loc[ind,'Плановая цена'] = cons.loc[ind,'цена без учета коэф.пересчата']
            else:
                try:
                    MARM_  = MARM.xs([cons.loc[ind,'Материал'],cons.loc[ind,'единица измерения закупки']])
                except KeyError:
                    MARM_ = pd.DataFrame()    
                if len(MARM_)>0:
                    cons.loc[ind,'Плановая цена'] = (cons.loc[ind,'цена без учета коэф.пересчата']/MARM_['Счетчик'])*MARM_['Знаменатель']
    cons.fillna(0,inplace=True)
    return cons 
                    
def f_KONH_fast (KONH,name_col_KONH,value):
    i = 1
    if len(KONH)==0:
            return ('пусто','0')
    KONH['sort'] = KONH['Номер_записи_условий'].astype('int')
    KONH.sort_values('sort',inplace = True,ascending = False)
    for row in KONH.itertuples():
        
        #if i ==len(KONH):
            #return ('пусто','0')
        if name_col_KONH=='округ':
            if row.округ == value:
                
                return (row.округ,row.Номер_записи_условий)
            i+=1
        elif name_col_KONH=='Завод':
            if row.Завод == value:
                
                return (row.Завод,row.Номер_записи_условий)
            i+=1
    return ('пусто','0')