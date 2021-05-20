import pandas as pd
import calendar
import datetime
from decimal import Decimal


def read_csv(args):
    print(args[1])
    df = pd.read_excel(args[1]+args[0],sheet_name='Sheet1',dtype={'Материал':'str','Завод':'str'})
    df['name_file'] = args[0]
    return df



def yy(x,sp):
    return x[sp].sum()

    


def func_obesp_3month(x,year,month,sp):
    def yy(x,sp):
        return x[sp].sum()
    summ = yy(x,sp)
    if summ ==0:
        return x[str(month)+'/'+str(year)+' Остаток Кол-во']
    elif (summ -x[str(month)+'/'+str(year)+' Остаток Кол-во'])<=0:
        return summ
    else: 
        return x[str(month)+'/'+str(year)+' Остаток Кол-во']  
        
        
        
def func_obesp_3month_procentil(x,year,month):
    if x['ПП 3 месяца'] ==0:
        return ''
    elif (x[str(month)+'/'+str(year)+' Остаток Кол-во']/x['ПП 3 месяца'])>1:
        return 1
    else:
        return x[str(month)+'/'+str(year)+' Остаток Кол-во']/x['ПП 3 месяца']       
    
    
def func_obesp_first_month_procentil(x,year,month,sp):
    if yy(x,sp) ==0:
        return ''
    elif (x[str(month)+'/'+str(year)+' Остаток Кол-во']/yy(x,sp))>1:
        return 1
    else:
        return x[str(month)+'/'+str(year)+' Остаток Кол-во']/yy(x,sp)

def func_obesp_second_month_procentil(x,year,month,sp):
    if x['ПП кол-во '+str(month+2)+'/'+ str(year)] ==0:
        return ''
    elif yy(x,sp)>x[str(month)+'/'+str(year)+' Остаток Кол-во']:
        return 0
    elif ((x[str(month)+'/'+str(year)+' Остаток Кол-во']-yy(x,sp))/x['ПП кол-во '+str(month+2)+'/'+ str(year)])>1:
        return 1
    else:
        return ((x[str(month)+'/'+str(year)+' Остаток Кол-во']-yy(x,sp))/x['ПП кол-во '+str(month+2)+'/'+ str(year)])
    
def func_obesp_third_month_procentil(x,year,month,sp):
    if x['ПП кол-во '+str(month+3)+'/'+ str(year)] ==0:
        return ''
    elif (yy(x,sp))>x[str(month)+'/'+str(year)+' Остаток Кол-во']:
        return 0
    elif ((x[str(month)+'/'+str(year)+' Остаток Кол-во']-yy(x,sp))/x['ПП кол-во '+str(month+3)+'/'+ str(year)])>1:
        return 1
    else:
        return ((x[str(month)+'/'+str(year)+' Остаток Кол-во']-yy(x,sp))/x['ПП кол-во '+str(month+3)+'/'+ str(year)])

def func_ne_obesp_first_month_(x,year,month,sp):
    if (yy(x,sp)-x[str(month)+'/'+str(year)+' Остаток Кол-во'])>0:
        return yy(x,sp)-x[str(month)+'/'+str(year)+' Остаток Кол-во']
    else:
        return 0    

    
def func_ne_obesp_second_month_(x,year,month,sp):
    if (x['ПП кол-во '+str(month+2)+'/'+ str(year)]-x[str(month)+'/'+str(year)+' Остаток Кол-во']+yy(x,sp)-x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во'])>0:
        return x['ПП кол-во '+str(month+2)+'/'+ str(year)]-x[str(month)+'/'+str(year)+' Остаток Кол-во']+yy(x,sp)-x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']
    else:
        return 0   
    
def func_ne_obesp_third_month_(x,year,month,sp):
    if (x['ПП кол-во '+str(month+3)+'/'+ str(year)]-x[str(month)+'/'+str(year)+' Остаток Кол-во']+yy(x,sp)-x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']-x['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во'])>0:
        return x['ПП кол-во '+str(month+3)+'/'+ str(year)]-x[str(month)+'/'+str(year)+' Остаток Кол-во']+yy(x,sp)-x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']-x['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во']
    else:
        return 0
    
def func_ZNB_AVIZOT_(x,year,month):
    summ = x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+3)+'/'+str(year)+ ' , кол-во']
    if summ==0:
        return 0
    elif (summ-x['Товар в пути (ZNB5, ZNB2/3-АвизОт)'])>=0:
        return x['Товар в пути (ZNB5, ZNB2/3-АвизОт)']
    elif (summ-x['Товар в пути (ZNB5, ZNB2/3-АвизОт)'])<0:
        return summ
    else:
        return 'хз'    
    
def func_EST_CONTRACT_(x,year,month):
    summ = x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+3)+'/'+str(year)+ ' , кол-во']
    if summ==0:
        return 0
    elif (summ-x['ZNB(АвизОт)']-x['Законтрактовано(ZNB-ПртПЗк)'])>=0:
        return x['Законтрактовано(ZNB-ПртПЗк)']
    elif (summ-x['ZNB(АвизОт)']-x['Законтрактовано(ZNB-ПртПЗк)'])<0:
        return summ-x['ZNB(АвизОт)']
    else:
        return 'хз'    
    
def func_NO_CONTRACT_(x,year,month):
    summ = x['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во']+x['Не обеспечено запасом ' + str(month+3)+'/'+str(year)+ ' , кол-во']
    if summ==0:
        return 0
    elif (summ-x['ZNB(АвизОт)']-x['Есть контракт']-x['Заявка на закупку(NB)'])>=0:
        return x['Заявка на закупку(NB)']
    elif (summ-x['ZNB(АвизОт)']-x['Есть контракт']-x['Заявка на закупку(NB)'])<0:
        return summ-x['ZNB(АвизОт)']-x['Есть контракт']
    else:
        return 'хз' 
    


def func_1(f0,ind,days):
    if f0.at[ind,'Модуль']=='ТОРО': 
        return f0.at[ind,'Дата деблокирования (ТОРО)']+datetime.timedelta(days=days)
    else: 
        return f0.at[ind,'Дата создания потребности']+datetime.timedelta(days=days)

def func_pr1(args):
    f0 = args[0]
    year = args[1]
    month  = args[2]
    ppm_date = args[3]
    nach_goda = args[4]
    sp_k = args[5]
    sp_kv = args[6]
    sp_summ = args[7]
    sp_kv_primech = args[8]
    sp_kv_sum_primech = args[9]
    sy= args[10]
    sp_current_kvartal = args[11]
    
    f0['ПП 3 месяца']  = f0.loc[:,sp_k].sum(axis=1)
    f0['ПП 3 месяца,Сумма']  = f0.loc[:,sp_summ].sum(axis=1)


    f0['Обеспечено 3 месяца, кол-во'] = f0.apply(lambda x:func_obesp_3month(x,year,month,sp_k),axis = 1 )
    f0['Обеспечено 3 месяца, сумма'] = f0['Обеспечено 3 месяца, кол-во']*f0['Цена']



    f0['Обеспеченность три месяца, кол-во, %'] = f0.apply(lambda x:func_obesp_3month_procentil(x,year,month,),axis = 1 )

    f0['Обеспеченность ' + str(month+1)+'/'+str(year)+ ' , кол-во, %'] = f0.apply(lambda x:func_obesp_first_month_procentil(x,year,month,sp_kv_primech),axis = 1 )

    f0['Обеспеченность ' + str(month+2)+'/'+str(year)+ ' , кол-во, %'] = f0.apply(lambda x:func_obesp_second_month_procentil(x,year,month,sp_kv_primech),axis = 1 )

    f0['Обеспеченность ' + str(month+3)+'/'+str(year)+ ' , кол-во, %'] = f0.apply(lambda x:func_obesp_third_month_procentil(x,year,month,sp_current_kvartal),axis = 1 )

    f0['Не обеспечено запасом ' + str(month+1)+'/'+str(year)+ ' , кол-во'] = f0.apply(lambda x:func_ne_obesp_first_month_(x,year,month,sp_kv_primech),axis = 1 )

    f0['Не обеспечено запасом ' + str(month+2)+'/'+str(year)+ ' , кол-во'] = f0.apply(lambda x:func_ne_obesp_second_month_(x,year,month,sp_kv_primech),axis = 1 )

    f0['Не обеспечено запасом ' + str(month+3)+'/'+str(year)+ ' , кол-во'] = f0.apply(lambda x:func_ne_obesp_third_month_(x,year,month,sp_current_kvartal),axis = 1 )

    f0['Не обеспечено, кол-во'] = f0.loc[:,[x for x in f0.columns if x.find('Не обеспечено запасом')!=-1]].sum(axis=1)  

    f0['Не обеспечено, сумма'] = f0['Не обеспечено, кол-во']* f0['Цена']

    f0['ZNB(АвизОт)'] = f0.apply(lambda x:func_ZNB_AVIZOT_(x,year,month),axis = 1 )

    f0['Есть контракт'] = f0.apply(lambda x:func_EST_CONTRACT_(x,year,month),axis = 1 )

    f0['Нет контракта'] = f0.apply(lambda x:func_NO_CONTRACT_(x,year,month),axis = 1 )

    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']

    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    
    
    
    n = 12
    if month==10:
        n+=1
    elif month==11:
        n+=2
    elif month==12:
        n+=3
    months = {1:'Январь',2:'Февраль',3:'Март',4:'Апрель',5:'Май',6:'Июнь',7:'Июль',8:'Август',9:'Сентябрь',10:'Октябрь',11:'Ноябрь',12:'Декабрь',13:'Январь_с',14:'Февраль_с',15:'Март_с'}
    for ind in f0.index:
        if f0.at[ind,'Законтрактовано(ZNB-ПртПЗк)']+f0.at[ind,'Заявка на закупку(NB)']-(f0.loc[ind,'ПП кол-во '+str(1)+'/'+ str(year):'ПП кол-во '+str(n)+'/'+ str(year)].sum()-f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во'])>0:
            f0.at[ind,'Излишек поставки'] = f0.at[ind,'Законтрактовано(ZNB-ПртПЗк)']+f0.at[ind,'Заявка на закупку(NB)']-(f0.loc[ind,'ПП кол-во '+str(1)+'/'+ str(year):'ПП кол-во '+str(n)+'/'+ str(year)].sum()-f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во'])
        else:
            f0.at[ind,'Излишек поставки']    = 0
            
    f0['Товар в пути, сумма'] = f0['ZNB(АвизОт)']*f0['Цена']        
    f0['Есть контракт, сумма'] = f0['Есть контракт']*f0['Цена']   
    f0['Нет контракта, сумма'] = f0['Нет контракта']*f0['Цена']

    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']

    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    
    for ind in f0.index:
        
        if yy(f0.loc[ind],sp_k)==0 or yy(f0.loc[ind],sy)==0 :
            f0.at[ind,'Примечание 1'] = 'Нет потребности три месяца'
        elif f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во'] +f0.at[ind,'ZNB(АвизОт)'] >= yy(f0.loc[ind],sp_k) :
            f0.at[ind,'Примечание 1'] = 'Обеспечено'
        elif  f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']==0:
            f0.at[ind,'Примечание 1'] = 'Не обеспечено'
        else:
            f0.at[ind,'Примечание 1'] = 'Обеспечено частично'
            
    for ind in f0.index:
        if yy(f0.loc[ind],sp_k)==0 or yy(f0.loc[ind],sy)==0 :
            f0.at[ind,'Примечание 3'] = 'Нет потребности три месяца'
        elif  f0.at[ind,'Не обеспечено, кол-во'] ==0 :
            f0.at[ind,'Примечание 3'] = 'Обеспечено остатком'
        elif  (f0.at[ind,'Примечание 1']=='Не обеспечено' or f0.at[ind,'Примечание 1']=='Обеспечено частично' )  and (f0.at[ind,'Плановик'] in['Прд.РМБУК ППК КЦРС','КАЗЦИНКМАШ','Сбс.прв.ТООКазцинк','Прд.РМБ Ал ПК КЦРС','Прод.Отд.Диз.полиг','УММ','Собст.пр-во ЖГОК']  ):
            f0.at[ind,'Примечание 3'] = 'Собственное производство'
        elif (f0.at[ind,'ZNB(АвизОт)']  >= f0.at[ind,'Не обеспечено, кол-во']) and (f0.at[ind,'Есть контракт']+f0.at[ind,'Нет контракта'])==0  :
            f0.at[ind,'Примечание 3'] = 'Обеспечено товаром в пути'
        elif f0.at[ind,'Есть контракт']>0 and (f0.at[ind,'Нет контракта']+f0.at[ind,'ZNB(АвизОт)']) ==0 :
            f0.at[ind,'Примечание 3'] = 'Есть контракт'
        elif f0.at[ind,'Нет контракта']>0 and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)']) ==0 :
            f0.at[ind,'Примечание 3'] = 'Нет контракта'
        elif (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)']+f0.at[ind,'Нет контракта'])==0 :
            f0.at[ind,'Примечание 3'] = 'Заявка не принята в работу'
        else:
            f0.at[ind,'Примечание 3'] = 'Есть контракт, объема недостаточно'


    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']

    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    
    for ind in f0.index:
        if f0.at[ind,'Примечание 3'] =='Собственное производство' :
            f0.at[ind,'Собственное производство'] = f0.at[ind,'Не обеспечено, кол-во']-(f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)']+f0.at[ind,'Нет контракта'])
        else:
            f0.at[ind,'Собственное производство'] = 0
    
    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']

    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    
      
    f0['Излишек поставки, сумма'] = f0['Излишек поставки']*f0['Цена']
   
    f0['Заявка не принята в работу']=f0.loc[:,[x for x in f0.columns if x.find('Не обеспечено запасом')!=-1]].sum(axis=1).apply(lambda x: round( Decimal(x),3)) -f0['ZNB(АвизОт)']-f0['Есть контракт'] -f0['Нет контракта']-f0['Собственное производство']    
    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']        
    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    f0['Заявка не принята в работу, сумма'] = f0['Заявка не принята в работу']*f0['Цена'] 
    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']        
    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    

    for ind in f0.index:
        if yy(f0.loc[ind],sp_k)==0 or yy(f0.loc[ind],sy)==0 :
            f0.at[ind,'Примечание 2'] = 'Нет потребности три месяца'
        elif  f0.at[ind,'Примечание 1']  =='Обеспечено частично' and (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])<  yy(f0.loc[ind],sp_kv_primech)  :
            f0.at[ind,'Примечание 2'] = 'Обеспечено остатком част. текущий месяц'
        elif   f0.at[ind,'Примечание 1']  =='Обеспечено частично' and  (  (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])== yy(f0.loc[ind],sp_kv_primech)  or (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])< yy(f0.loc[ind],sp_current_kvartal)):
            f0.at[ind,'Примечание 2'] = 'Обеспечено остатком текущий месяц'
        elif   f0.at[ind,'Примечание 1']  =='Обеспечено частично' and (   (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])<  yy(f0.loc[ind],sp_k)  or (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])==  yy(f0.loc[ind],sp_k)):
            f0.at[ind,'Примечание 2'] = 'Обеспечено остатком два месяца'
        elif   f0.at[ind,'Примечание 1']  =='Обеспечено частично' and (f0.at[ind,str(month)+'/'+str(year)+' Остаток Кол-во']+f0.at[ind,'ZNB(АвизОт)'])>=yy(f0.loc[ind],sy):
            f0.at[ind,'Примечание 2'] = 'Обеспечено остатком до 1 ' + str(year+1)
        elif   f0.at[ind,'Примечание 1']  =='Не обеспечено':
            f0.at[ind,'Примечание 2'] = 'Не обеспечено остатком'
        else:
            f0.at[ind,'Примечание 2'] = 'Обеспечено остатком'

        

    

    for ind in f0.index:
        f0.at[ind,'Периодичность'] = sum([1 for x in  sy  if  f0.loc[ind,x]>0] )       

    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']        
    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
        
    for ind in f0.index:
        if yy(f0.loc[ind],sp_k)==0:
            f0.at[ind,'Период потребности'] = ''
        else:    
            x = f0.loc[ind,sp_k]
            for g in x.index:
                if x[g]>0:
                    f0.at[ind,'Период потребности'] = months[int(g.split('/')[0][-2:])]
                    break
                
    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']        
    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))



    if month ==10:
        year1 = year
        year2 = year
        year3 = year+1
    
        month1 = month+1
        month2 = month+2
        month3 = 1
    elif month == 11:
        year1 = year
        year2 = year+1
        year3 = year+1
    
        month1 = month+1
        month2 = 1
        month3 = 2
    elif month==12:
        year1 = year+1
        year2 = year+1
        year3 = year+1
    
        month1 = 1
        month2 = 2
        month3 = 3
    else:
        year1 = year
        year2 = year
        year3 = year
        month1 = month+1
        month2 = month+2
        month3 = month+3    

    for ind in f0.index:
        if f0.at[ind,'Примечание 1'] == 'Не обеспечено'  and yy(f0.loc[ind],sp_kv_primech)>0 and func_1(f0,ind,100)>(datetime.datetime(year1,month1,1)+datetime.timedelta(days=calendar.monthrange(year1,month1)[1])):
            f0.at[ind,'Ввод потребности'] = 'ПП введена без учета сроков контрактования'
        elif f0.at[ind,'Примечание 1'] == 'Не обеспечено'  and f0.at[ind,'ПП кол-во '+str(month+2)+'/'+ str(year)]>0 and func_1(f0,ind,100)>(datetime.datetime(year2,month2,1)+datetime.timedelta(days=calendar.monthrange(year2,month2)[1])):
            f0.at[ind,'Ввод потребности'] = 'ПП введена без учета сроков контрактования'
        elif f0.at[ind,'Примечание 1'] == 'Не обеспечено'  and f0.at[ind,'ПП кол-во '+str(month+3)+'/'+ str(year)]>0 and func_1(f0,ind,100)>(datetime.datetime(year3,month3,1)+datetime.timedelta(days=calendar.monthrange(year3,month3)[1])):
            f0.at[ind,'Ввод потребности'] = 'ПП введена без учета сроков контрактования'
        else:
            f0.at[ind,'Ввод потребности'] = 'ПП введена с учетом сроков контрактования'
            
    for ind in f0.index:
        if f0.at[ind,'Ввод потребности'] == 'ПП введена с учетом сроков контрактования':
            f0.at[ind,'Расчетная дата потребности'] = datetime.datetime(1900,1,1)
        elif f0.at[ind,'Модуль']=='ТОРО' :
            date_ =f0.at[ind,'Дата деблокирования (ТОРО)']+datetime.timedelta(days=100)
            f0.at[ind,'Расчетная дата потребности'] = datetime.datetime(date_.year,date_.month,1)
        else:
            date_ =f0.at[ind,'Дата создания потребности']+datetime.timedelta(days=100)
            f0.at[ind,'Расчетная дата потребности'] = datetime.datetime(date_.year,date_.month,1)


    for ind in f0.index:
         
        if f0.at[ind,'Ввод потребности']=='ПП введена без учета сроков контрактования':
            f0.at[ind,'Ответственность'] = 'Ответственность Заказчика'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and  f0.at[ind,'Плановик'] in ['Не закупать','Прд.РМБУК ППК КЦРС','КАЗЦИНКМАШ','Сбс.прв.ТООКазцинк','Прд.РМБ Ал ПК КЦРС','Прод.Отд.Диз.полиг','УММ','Фиктивный плановик','Собст.пр-во ЖГОК']:
            f0.at[ind,'Ответственность'] = 'Ответственность Заказчика'
        elif f0.at[ind,'СтатусМтрл на заводе']>0  :
            f0.at[ind,'Ответственность'] = 'Ответственность Заказчика'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and  func_1(f0,ind,45)<f0.at[ind,'Дата заключения RCM']:
            f0.at[ind,'Ответственность'] = 'Ответственность трейдера'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and  f0.at[ind,'Нет контракта']>0 and  f0.at[ind,'Дата создания элемента ППМ пополнения NB01']<=ppm_date:  
            f0.at[ind,'Ответственность'] = 'Ответственность трейдера'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and  f0.at[ind,'Нет контракта']==0 and  f0.at[ind,'СтатусМтрл на заводе']==0:    
            f0.at[ind,'Ответственность'] = 'Ответственность УЗ'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and  f0.at[ind,'Нет контракта']>0 and  f0.at[ind,'Дата создания элемента ППМ пополнения NB01']>=ppm_date:      
            f0.at[ind,'Ответственность'] = 'Ответственность общая'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and  func_1(f0,ind,45)>f0.at[ind,'Дата заключения RCM']:
            f0.at[ind,'Ответственность'] = 'Ответственность трафика'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and yy(f0.loc[ind],sp_kv_primech)>0 :    
            f0.at[ind,'Ответственность'] = 'Ответственность трафика'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ПП кол-во '+str(month+2)+'/'+ str(year)]>0 :    
            f0.at[ind,'Ответственность'] = 'Ответственность трафика'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ПП кол-во '+str(month+3)+'/'+ str(year)]>0 :     
            f0.at[ind,'Ответственность'] = 'Ответственность трафика'
        else:
            f0.at[ind,'Ответственность'] = f0.at[ind,'Примечание 1']

    for ind in f0.index:
        if f0.at[ind,'Ответственность']=='Ответственность Заказчика' and f0.at[ind,'Ввод потребности']=='ПП введена без учета сроков контрактования':
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка введена без учета сроков поставки'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and  f0.at[ind,'Плановик'] in ['Не закупать','Фиктивный плановик']:
            f0.at[ind,'Описание отклонения по ответственности'] = 'Некорректный плановик' 
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'СтатусМтрл на заводе']>0 :
            f0.at[ind,'Описание отклонения по ответственности'] = 'Номенклатура заблокирована'    
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Плановик'] in ['Прд.РМБУК ППК КЦРС','КАЗЦИНКМАШ','Сбс.прв.ТООКазцинк','Прд.РМБ Ал ПК КЦРС','Прод.Отд.Диз.полиг','УММ','Собст.пр-во ЖГОК']:  
            f0.at[ind,'Описание отклонения по ответственности'] = 'Собственное производство'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and   func_1(f0,ind,45)<f0.at[ind,'Дата заключения RCM']:    
            f0.at[ind,'Описание отклонения по ответственности'] = 'Контракт заключен позже необходимого срока'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and f0.at[ind,'Нет контракта']==0 :      
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявки на закуп нет'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and    f0.at[ind,'Дата создания элемента ППМ пополнения NB01']<=ppm_date:
            f0.at[ind,'Описание отклонения по ответственности'] = 'Контракт не заключен'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])==0 and    f0.at[ind,'Дата создания элемента ППМ пополнения NB01']>=ppm_date:    
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявки на закуп сформированы в период между прогоном ППМ'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and yy(f0.loc[ind],sp_kv_primech)>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']>0 and (f0.at[ind,'Дата заключения RCM']+datetime.timedelta(days=65))<= (datetime.datetime(year1,month1,1)+datetime.timedelta(days=calendar.monthrange(year1,month1)[1])):    
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику сформирована, срыв поставки поставщиком'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'ПП кол-во '+str(month+2)+'/'+ str(year)]>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']>0 and (f0.at[ind,'Дата заключения RCM']+datetime.timedelta(days=65))<= (datetime.datetime(year2,month2,1)+datetime.timedelta(days=calendar.monthrange(year2,month2)[1])):     
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику сформирована, срыв поставки поставщиком'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'ПП кол-во '+str(month+3)+'/'+ str(year)]>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']>0 and (f0.at[ind,'Дата заключения RCM']+datetime.timedelta(days=65))<= (datetime.datetime(year3,month3,1)+datetime.timedelta(days=calendar.monthrange(year3,month3)[1])):
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику сформирована, срыв поставки поставщиком'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and yy(f0.loc[ind],sp_kv_primech)>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']==0: 
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику не сформирована'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'ПП кол-во '+str(month+2)+'/'+ str(year)]>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']==0:     
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику не сформирована'
        elif f0.at[ind,'Примечание 1'] in ['Не обеспечено','Обеспечено частично'] and f0.at[ind,'ПП кол-во '+str(month+3)+'/'+ str(year)]>0 and  (f0.at[ind,'Есть контракт']+f0.at[ind,'ZNB(АвизОт)'])>0 and f0.at[ind,'ZNB(АвизОт)']==0:     
            f0.at[ind,'Описание отклонения по ответственности'] = 'Заявка поставщику не сформирована'
        else:
            f0.at[ind,'Описание отклонения по ответственности'] = f0.at[ind,'Примечание 1']      


    for ind in f0.index:
        if f0.at[ind,'ПРОЧЕЕ']!=0 and f0.at[ind,'ТОРО']!=0 and f0.at[ind,'РР']!=0:
            f0.at[ind,'Комментарий по модулю']='Дублирование во всех модулях'
        elif f0.at[ind,'ПРОЧЕЕ']==0 and f0.at[ind,'ТОРО']!=0 and f0.at[ind,'РР']!=0:   
            f0.at[ind,'Комментарий по модулю']='Дублирование в ТОРО и РР'
        elif f0.at[ind,'ПРОЧЕЕ']!=0 and f0.at[ind,'ТОРО']!=0 and f0.at[ind,'РР']==0:  
            f0.at[ind,'Комментарий по модулю']='Дублирование в ТОРО и Прочее'
        elif f0.at[ind,'ПРОЧЕЕ']!=0 and f0.at[ind,'ТОРО']==0 and f0.at[ind,'РР']!=0: 
            f0.at[ind,'Комментарий по модулю'] = 'Дублирование в РР и Прочее'
        else:
            f0.at[ind,'Комментарий по модулю'] = 'Без отклонений'
            
    f0['Собственное производство, сумма'] = f0['Собственное производство']*f0['Цена']
    if nach_goda==False:
        f0['Потребность прошедшего периода, кол-во'] = f0.loc[:,'ПП кол-во '+str(1)+'/'+ str(year):'ПП кол-во '+str(month)+'/'+ str(year)].sum(axis = 1).apply(lambda x: round( Decimal(x),3))
        f0['Потребность прошедшего периода, сумма'] = f0['Потребность прошедшего периода, кол-во']*f0['Цена']        
    arr_dec1 = [x for x in f0.columns if f0[x].dtype=='float64']
    for col in arr_dec1:
        f0[col] = f0[col].apply(lambda x: round( Decimal(x),3))
    if nach_goda==False:
        for ind in f0.index:
            if f0.at[ind,'Потребность прошедшего периода, кол-во']>0:
                f0.at[ind,'Комментарий по ПП прошедшего периода'] = 'Потребность не перенесена на будущий период'
            else:
                f0.at[ind,'Комментарий по ПП прошедшего периода'] = 'Без отклонений'

    for ind in f0.index:
        if yy(f0.loc[ind],sy)==0:
            f0.at[ind,'Мероприятия'] = 'Отсутствует потребность до конца года'
        elif f0.at[ind,'Примечание 1'] == 'Нет потребности три месяца':  
            f0.at[ind,'Мероприятия'] = 'Анализ в следующем периоде'  
        elif f0.at[ind,'Примечание 1'] == 'Обеспечено':
            f0.at[ind,'Мероприятия'] = 'Своевременное списание, корректировка потребности в случае не освоения'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Заявка поставщику не сформирована' : 
            f0.at[ind,'Мероприятия'] = 'Ускорить формирование заявки поставщику'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Заявка введена без учета сроков поставки' :     
            f0.at[ind,'Мероприятия'] = 'Скорректировать период потребности'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Заявки на закуп сформированы в период между прогоном ППМ' :     
            f0.at[ind,'Мероприятия'] = 'Контроль за своевременным контрактованием'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Контракт не заключен' :     
            f0.at[ind,'Мероприятия'] = 'Ускорить процесс контрактования'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Контракт заключен позже необходимого срока' and f0.at[ind,'ZNB(АвизОт)'] >0:     
            f0.at[ind,'Мероприятия'] = 'Ускорить поставку'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Контракт заключен позже необходимого срока' and f0.at[ind,'ZNB(АвизОт)'] ==0 and f0.at[ind,'Есть контракт'] >0:     
            f0.at[ind,'Мероприятия'] = 'Ускорить формирование заявки поставщику'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Заявка поставщику сформирована, срыв поставки поставщиком':     
            f0.at[ind,'Мероприятия'] = 'Ускорить поставку'
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Заявки на закуп нет':     
            f0.at[ind,'Мероприятия'] = 'Проработать причины не формирования документа' 
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Номенклатура заблокирована':     
            f0.at[ind,'Мероприятия'] = 'Проработать возможность разблокировки' 
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Некорректный плановик':     
            f0.at[ind,'Мероприятия'] = 'Проработать присвоение корректного плановика' 
        elif f0.at[ind,'Примечание 1'] in['Не обеспечено','Обеспечено частично'] and f0.at[ind,'Описание отклонения по ответственности']=='Собственное производство':     
            f0.at[ind,'Мероприятия'] = 'Проработать статус изготовления'
        else:
            f0.at[ind,'Мероприятия'] = 'Потребность обеспечена'          
            
    
            
    return f0   
    
    


    
    
    
    
def main_price_f(args):
    
    A900 = args[0]
    A902 = args[1]
    konp_gr = args[2]
    df = args[3]
    pl_kurs = args[4]
    
    def price(x):
        if x['Цена']==0:
            return 1
        elif x['Цена']==pl_kurs:
            return 1
        else:
            return x['Цена']
    df1 = df.set_index(['Код округа','Материал'])
    for ind in A902.index:
        
        try: 
            dat = df1.xs([A902.at[ind,'Код округа'],A902.at[ind,'Материал']],level = [0,1])
        except KeyError:
            dat = pd.DataFrame()
        if len(dat)>0:
            pr = mex_price(konp_gr,A902.at[ind,'Номер записи условий'],pl_kurs)
            for ind in dat['index']:
                
                if df.loc[ind,'Цена']==0:
                    df.loc[ind,'Цена'] = pr
            
            
        
    df2 = df.set_index(['Материал','dd'])
    for ind in A900.index:
        
        try: 
            dat = df2.xs(A900.at[ind,'Материал'])
        except KeyError:
            dat = pd.DataFrame()
        if len(dat)>0:
            pr = mex_price(konp_gr,A900.at[ind,'Номер записи условий'],pl_kurs)
            for ind in dat['index']:
                
                if df.loc[ind,'Цена']==0:
                    df.loc[ind,'Цена'] = pr
                          
    
    df['Цена'] = df.apply(lambda x: price(x),axis = 1)
    
    return df
    
    
def mex_price(konp_gr,nom_zap_usl,pl_kurs):
        
    # print(dat['Номер записи условий'].values[0])
    try:
        konp_ = konp_gr.xs([nom_zap_usl])
    except KeyError:
        return 0
    # если есть  в конп
    if len(konp_)>0:
        if konp_['Сумма условия'].values[0]==1:
            return 1

        if konp_['Базовая ЕИ'].values[0]==0 or konp_['Базовая ЕИ'].values[0]==konp_['Единица измерения'].values[0]:
            price = (konp_['Сумма условия'].values[0]  / konp_['Единица цены'].values[0])*pl_kurs
            return price



        elif konp_['Базовая ЕИ'].values[0]!=konp_['Единица измерения'].values[0]:

            if konp_['Числитель пересчета'].values[0]==0:
                price = konp_['Сумма условия'].values[0] *pl_kurs
                return price

            else:
                price = ((konp_['Сумма условия'].values[0]*konp_['Числитель пересчета'].values[0])/konp_['Единица цены'].values[0])*pl_kurs
                return price
         
                     



# def kompl(args):
    # TWLAD = args[0]
    # ADRC = args[1]
    # df = args[2]
    
    
    # for ind in df.index:

        # try:
            # df_master = TWLAD.xs([df.at[ind, 'Завод'],df.at[ind, 'Склад потребности']])

        # except KeyError:
            # df_master = pd.DataFrame()

        # if len(df_master) > 0:

            # try:
                # df_master1 = ADRC.xs(df_master['Номер адреса'])

            # except KeyError:

                # df_master1 = pd.DataFrame()

            # if len(df_master1) > 0:
                # df.at[ind, 'Комплекс'] =  df_master1['Критерий поиска 2']
    # return df
    
    
    
def calc_price_super_fast(args):

    cons = args[0]
    KONH_po = args[1]
    KONH_s = args[2]
    current_date = args[3]
    KONP = args[4]
    MARM = args[5]
    pl_kurs = args[6]
    # KONH_po['sort'] = KONH_po['Номер_записи_условий'].astype('int')
    # KONH_po.sort_values('sort',inplace = True,ascending = False)
    # KONH_s['sort'] = KONH_s['Номер_записи_условий'].astype('int')
    # KONH_s.sort_values('sort',inplace = True,ascending = False)
    
    for ind in cons.index: 
        try:
            # Konh_ = KONH_po.xs([cons.at[ind,'Материал'],str(current_date.year)])
            Konh_ = KONH_po.get_group(str(cons.at[ind,'Материал'])+str(current_date.year))
        except KeyError:
            Konh_ = pd.DataFrame() 
            
        
        try:
            # Konh_1 = KONH_s.xs([cons.at[ind,'Материал'],str(current_date.year)])
            Konh_1 = KONH_s.get_group(str(cons.at[ind,'Материал'])+str(current_date.year))
        except KeyError:
            Konh_1 = pd.DataFrame() 
        
        res = f_KONH_fast(Konh_1,'округ',cons.loc[ind,'округ'])
        if res[0]!='пусто' and get_konp(KONP,res[1]).shape[0]>0:
            cons.loc[ind,'номер записи условий'] = res[1]
            continue
        res = f_KONH_fast(Konh_,'округ',cons.loc[ind,'округ'])
        if res[0]!='пусто' and get_konp(KONP,res[1]).shape[0]>0:
            cons.loc[ind,'номер записи условий'] = res[1]
            continue
        res = f_KONH_fast(Konh_1,'Завод',cons.loc[ind,'Завод'])
        if res[0]!='пусто'  and get_konp(KONP,res[1]).shape[0]>0:
            cons.loc[ind,'номер записи условий'] = res[1]
            continue
        res = f_KONH_fast(Konh_,'Завод',cons.loc[ind,'Завод'])          
        if res[0]!='пусто'  and get_konp(KONP,res[1]).shape[0]>0:
            cons.loc[ind,'номер записи условий'] = res[1]
            continue
        
        
        if res[1]=='0':
            for row in Konh_1.itertuples():
                if row.округ=='пусто'  and row.Завод =='пусто':
                    cons.loc[ind,'номер записи условий'] = row.Номер_записи_условий
                    break
            for row in Konh_.itertuples():
                if row.округ=='пусто'  and row.Завод =='пусто':
                    cons.loc[ind,'номер записи условий'] = row.Номер_записи_условий
                    break

    for ind in cons.index:

        ar = get_konp(KONP,cons.loc[ind,'номер записи условий'])

        if len(ar)>0:

            cons.loc[ind,'цена без учета коэф.пересчата'] = ar['Сумма условия'].values[0]/ar['Единица цены'].values[0]
            cons.loc[ind,'единица измерения закупки'] = ar['Единица измерения'].values[0]
            
            if cons.loc[ind,'Базовая ЕИ']==cons.loc[ind,'единица измерения закупки']:
                cons.loc[ind,'Цена'] = cons.loc[ind,'цена без учета коэф.пересчата']*pl_kurs
            else:
                try:
               
                    MARM_ = MARM.get_group(cons.loc[ind,'Материал']+cons.loc[ind,'единица измерения закупки'])
                except KeyError:
                    MARM_ = pd.DataFrame()    
                if len(MARM_)>0:
                    cons.loc[ind,'Цена'] = ((cons.loc[ind,'цена без учета коэф.пересчата']/MARM_['Счетчик'].values[0])*MARM_['Знаменатель'].values[0])*pl_kurs
    cons.fillna(0,inplace=True)
    return cons 
                    
def f_KONH_fast (KONH,name_col_KONH,value):
    i = 1
    if len(KONH)==0:
        return ('пусто','0')
    
    for row in KONH.itertuples():
        
        if name_col_KONH=='округ':
            if row.округ == value:
                
                return (row.округ,row.Номер_записи_условий)
            i+=1
        elif name_col_KONH=='Завод':
            if row.Завод == value:
                
                return (row.Завод,row.Номер_записи_условий)
            i+=1
    return ('пусто','0')
    
    
    
def f_KONH_fast_(ind_,name_col_KONH,value,zav,okr,number):

    if len(ind_)==0:
            return ('пусто','0')
    for ind in ind_:
        if name_col_KONH=='округ':
            if okr[ind] == value:
                return (okr[ind],number[ind])
        elif name_col_KONH=='Завод':
            if zav[ind] == value:  
                return (zav[ind],number[ind])
            
    return ('пусто','0')


def get_konp(KONP,val):
    try:
        # ar = KONP.xs(cons.loc[ind,'номер записи условий'])
        ar = KONP.get_group(val)
        

    except KeyError:
        ar = pd.DataFrame()   
        
    return ar
    
