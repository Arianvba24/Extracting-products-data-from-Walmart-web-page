from requests_html import HTMLSession
import re
import pandas as pd
from fake_useragent import UserAgent

ua = UserAgent()



class Spider_functions():
    def __init__(self):
        pass
    def html_to_txt(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxys = proxys
        self.params = params
        self.adress = adress
        
        session = HTMLSession()
    
        request = session.get(self.url)
        with open(adress,"w",encoding="UTF-8") as f:
            data = f.write(request.text)
            f.close()
            
        print(f"HTML succesfully saved in {adress}")
        return data
        
    def html_to_json(self,url,adress,headers = None,cookies = None,proxys=None,params = None):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.proxys = proxys
        self.params = params
        self.adress = adress
        
        session = HTMLSession()
    
        request = session.get(self.url)
#         print()
#         print(request.json())
        data = request.json()
        
        with open(self.adress,"w") as j:
            json.dump(data,j)
            
        return data
    def regex_javascript_single_data(self,url = None,headers = None,cookies = None,proxys=None,params = None,use_txt=None,adress_txt = None):
        if use_txt == True and adress_txt and url == None:
            print("Let's use txt!")
            with open(adress_txt,"r") as f:
                text = f.read()
                f.close()
        
            
        else:
            
            self.url = url
            self.headers = headers
            self.cookies = cookies
            self.proxys = proxys
            self.params = params
            session = HTMLSession()

            text = session.get(self.url).text


        patron = '"fitmentLabel":null,"name":[\S\s]{1,125},"check'
        final = re.findall(patron,text)   

        def replace_title(text):

            xp = f'"fitmentLabel":null,"name":"'
            p = f'","check'
            k = f'\\"'
            result1 = text.replace(xp,"")

            result = result1.replace(k,"")
            return result.replace(p,"")
        #     return xp

        item_description_value = [replace_title(x) for x in final]
#         Price-----------------------------------------------------------------------------
        patron = '"priceInfo":{"itemPrice":[\S\s]{1,80},'
        final = re.findall(patron,text)   


        def replace_price(text):
            value = re.findall(r"[0-9]{1,6}[.][0-9]*",text.replace(",",""))
            if value:

                return value[-1]
            else:
                return [0][-1]

        price_value = [replace_price(x) for x in final]
#         Rating-----------------------------------------------------------------------------
        patron = '"rating":{"averageRating"[\S\s]{1,80},'
        final = re.findall(patron,text)   



        def replace_rating(text):
            value = re.findall(r"\d+",text)
            if len(value) > 0:
                return value
            else:
                return [0]

        rating_value = [replace_rating(x)[-1] for x in final]

#         W+-----------------------------------------------------------------------------
  

        patron = 'productLocationDisplayValue[\S\s]{1,1050}'
        final = re.findall(patron,text)   


        def replace_w_assurance(text):
            value = re.findall(r"SAVE_WITH_W_PLUS",text)
            if len(value) > 0:
                return ["W+ assurance"]
            else:
                return ["No w+ assurance"]


        w_save_value = [replace_w_assurance(x)[0] for x in final]
        
#         Pick up--------------------------------------------------------------------------
        patron = 'productLocationDisplayValue[\S\s]{1,1050}'
        final = re.findall(patron,text)   


        def replace_pick_up(text):
            value = re.findall(r"Free pickup[\S\s]{1,40},",text)
        #     value2 = re.findall(r'slaText[\S\s]{1,40},',text)
        #     return value

            if len(value) > 0:
                value1 = re.findall(r':[\S\s]{1,20}',value[0])
                value2 = re.findall(r'[a-z]+',value1[0])
                return f"Free pick up {value2[0]}"

            else:
                return "No pick up"



        pick_up_value = [replace_pick_up(x) for x in final]

#         Delivery------------------------------------------------------------------------
        patron = 'productLocationDisplayValue[\S\s]{1,1050}'
        final = re.findall(patron,text)   


        final

        def replace_delivery(text):
            value1 = re.findall(r"Delivery[\S\s]{1,40},",text)

            if len(value1) > 0:
                value2 = re.findall(r':[\S\s]{1,10}',value1[0])
                value3 = re.findall(r'[a-z]+',value2[0])
                return f"Delivery {value3[0]}"
            else:
                return "No delivery"


        delivery_value = [replace_delivery(x) for x in final]


#         Shipping------------------------------------------------------------------------
        
        patron = 'productLocationDisplayValue[\S\s]{1,1050}'
        final = re.findall(patron,text)   


        final

        def replace_shipping(text):
            value1 = re.findall(r"Free shipping[\S\s]{1,40}",text)
            if len(value1) > 0:
                value2 = re.findall(r":[\S\s]{1,40},",value1[0])
                value3 = re.findall(r'[a-z]+\s{0,1}[\S]{0,3}\s{0,1}[a-z]{0,10}',value2[0])
                value = value3[0].replace('",','')
                return f"Free shipping {value}"
            else:
                return ["No"]


        shipping_value = [replace_shipping(x) for x in final]
        

#         print(item_description_value)
#         print(request.text)
    
        data = {
    
            "Item description" : item_description_value,
            "Price" : price_value,
            "Rating" : rating_value,
            "W+": w_save_value,
            "Pick up" : pick_up_value,
            "Delivery" : delivery_value,
            "Shipping" : shipping_value
       
        }

        df = pd.DataFrame(data)
        
        self.df = df
        
        return df
    
    def regex_javascript_multiple_data(self,df,urls_amount:int,url=None):
        self.df = df
        self.urls_amount = urls_amount
        def replace_title(text):

            xp = f'"fitmentLabel":null,"name":"'
            p = f'","check'
            k = f'\\"'
            result1 = text.replace(xp,"")

            result = result1.replace(k,"")
            return result.replace(p,"")
        
        def replace_price(text):
            value = re.findall(r"[0-9]{1,6}[.][0-9]*",text.replace(",",""))
            if value:

                return value[-1]
            else:
                return [0][-1]
                
        def replace_rating(text):
            value = re.findall(r"\d+",text)
            if len(value) > 0:
                return value
            else:
                return [0]
                
        def replace_w_assurance(text):
            value = re.findall(r"SAVE_WITH_W_PLUS",text)
            if len(value) > 0:
                return ["W+ assurance"]
            else:
                return ["No w+ assurance"]
                
        def replace_pick_up(text):
            value = re.findall(r"Free pickup[\S\s]{1,40},",text)

            if len(value) > 0:
                value1 = re.findall(r':[\S\s]{1,20}',value[0])
                value2 = re.findall(r'[a-z]+',value1[0])
                return f"Free pick up {value2[0]}"

            else:
                return "No pick up"
        def replace_delivery(text):
            value1 = re.findall(r"Delivery[\S\s]{1,40},",text)
            # print(value1,"--------------------------------")
            if len(value1) > 0:
                value2 = re.findall(r':[\S\s]{1,10}',value1[0])
                value3 = re.findall(r'[a-z]+',value2[0])
                # print(value3)
                return f"Delivery {value3[0]}"
            else:
                return "No delivery"
        def replace_shipping(text):
            value1 = re.findall(r"Free shipping[\S\s]{1,40}",text)
            if len(value1) > 0:
                value2 = re.findall(r":[\S\s]{1,40},",value1[0])
                value3 = re.findall(r'[a-z]+\s{0,1}[\S]{0,3}\s{0,1}[a-z]{0,10}',value2[0])
                value = value3[0].replace('",','')
                return f"Free shipping {value}"
            else:
                return ["No"]
        item_description_value = []
        price_value = []
        rating_value = []
        w_save_value = []
        pick_up_value = []
        delivery_value = []
        shipping_value = []
        page = []
        
        for i in range(2,urls_amount + 1):
            
            
            url = f"https://www.walmart.com/browse/electronics/shop-tvs-by-size/3944_1060825_2489948?povid=ETS_TAVC_TVCP_Itemcarousel__hotandtrending&page={i}&affinityOverride=default"
            session = HTMLSession()

            text = session.get(url).text


            patron = '"fitmentLabel":null,"name":[\S\s]{1,250},"check'
            final = re.findall(patron,text)   

            

            item_description_value_1 = [replace_title(x) for x in final]
            print(len(item_description_value_1))
            item_description_value.extend(item_description_value_1)
            
    #         Price-----------------------------------------------------------------------------
            patron = '"priceInfo":{"itemPrice":[\S\s]{1,80},'
            final = re.findall(patron,text)   

            price_value_1 = [replace_price(x) for x in final]
            print(len(price_value_1))
            price_value.extend(price_value_1)
    #         Rating-----------------------------------------------------------------------------
            patron = '"rating":{"averageRating"[\S\s]{1,80},'
            final = re.findall(patron,text)   

            rating_value_1 = [replace_rating(x)[-1] for x in final]
            print(len(rating_value_1))
            rating_value.extend(rating_value_1)

    #         W+-----------------------------------------------------------------------------


            patron = 'productLocationDisplayValue[\S\s]{1,1050}'
            final = re.findall(patron,text)   

            w_save_value_1 = [replace_w_assurance(x)[0] for x in final]
            print(len(w_save_value_1))
            w_save_value.extend(w_save_value_1)

    #         Pick up--------------------------------------------------------------------------
            patron = 'productLocationDisplayValue[\S\s]{1,1050}'
            final = re.findall(patron,text)   

            pick_up_value_1 = [replace_pick_up(x) for x in final]
            print(len(pick_up_value_1))
            pick_up_value.extend(pick_up_value_1)

    #         Delivery------------------------------------------------------------------------
            patron = 'productLocationDisplayValue[\S\s]{1,1050}'
            final = re.findall(patron,text)   

            delivery_value_1 = [replace_delivery(x) for x in final]
            print(len(delivery_value_1))
            delivery_value.extend(delivery_value_1)


    #         Shipping------------------------------------------------------------------------

            patron = 'productLocationDisplayValue[\S\s]{1,1200}'
            final = re.findall(patron,text)   

            shipping_value_1 = [replace_shipping(x) for x in final]
            print(len(shipping_value_1))
            shipping_value.extend(shipping_value_1)

            print(url)

        data = {

            "Item description" : item_description_value,
            "Price" : price_value,
            "Rating" : rating_value,
            "W+": w_save_value,
            "Pick up" : pick_up_value,
            "Delivery" : delivery_value,
            "Shipping" : shipping_value

        }

        df_1 = pd.DataFrame(data)
        
        dfx = pd.concat([df,df_1],ignore_index = True)

        

        return dfx
        
    def from_dataframe_to_data(self,df,extension,adress):
        self.extension = extension
        self.df = df
        self.adress = adress
        if self.extension == "csv":
            return self.df.to_csv(self.adress,index = False)
        elif self.extension == "xlsx":
            return self.df.to_excel(self.adress,index = False)
        elif self.extension == "sql":
            return self.df.to_sql(self.adress,index = False)
        elif self.extension == "json":
            return self.df.to_json(self.adress,index = False)
        elif self.extension == "parquet":
            return self.df.to_parquet(self.adress,index = False)
        
    


if __name__=="__main__":

    spider = Spider_functions()
    df=spider.regex_javascript_single_data(url = r"https://www.walmart.com/browse/electronics/shop-tvs-by-size/3944_1060825_2489948?povid=ETS_TAVC_TVCP_Itemcarousel__hotandtrending&affinityOverride=default")
    df_2 = spider.regex_javascript_multiple_data(df = df,urls_amount = 25)
    print(df_2)
    spider.from_dataframe_to_data(df=df,extension="xlsx",adress=r"C:\Users\Cash\Proyectos\Web Scrapping\Walmart\output.xlsx")
