# -*- coding: utf-8 -*-
"""
Created on Sat May 28 18:08:11 2022

@author: scott
"""
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import pickle





url_list_search= ['https://www.bbcgoodfood.com/search?q=']#,'https://www.delish.com/search/?q=']#,'https://www.simplyrecipes.com/search?q=']
class food_finder:
    
    def main(self):
        dish= input('Dish name: ')
       
        ing= input('ingredints: ')
        print('searching')
        if ',' in ing : 
            ing= ing.split(',')
        else:    
         ing= ing.split()
        
        print(ing)
        self.recipe_filter(dish,ing)
        
        
        
        
    # method that that takes in url and a tag with class name to return a secttion of html from the website
    def content_finder(self,url,marker,class_N):
        m=marker # html tag
        c= class_N # class name 
        url= url
        url_req= requests.get(url)
        url_req= url_req.text
        if m == 'div-2':
            m='div'
        url_content= BeautifulSoup(url_req,'html.parser')
        content= url_content.find(m,class_=c )
        if content == None :
             content= url_content.find(m)
            
        return content#.get_text()
    
    
      #method that taske in url and return a dict of recipe tiltle,method and list of ingredints 
    def recipe_assembler(self,websites=["https://www.bbcgoodfood.com/recipes/pork-medallions"]):#, "https://www.delish.com/uk/cooking/recipes/a30975501/fried-chicken-wings-recipe/"]):
        url= websites
        
        for x in url:
         
         marker_clas = self.web_site_dic(x)
         recipelist = []
        for x in url:
         try:   
          for key in marker_clas.keys():
             k=marker_clas[key]
             r= list(marker_clas.get(key))[0]
             
             l2= k[r]['dilemter']
            
             l= k[r]['class_n']
            
             con= self.content_finder(x,r, l)
            
             z=  self.htl_list_conver(con,l2)
             
           #  print(list(marker_clas.get('titl'))[0])
             if l == marker_clas['meth'][list(marker_clas.get('meth'))[0]]["class_n"]:
                 method = z 
             elif r == list(marker_clas.get('titl'))[0]:
                 title = z.get_text() 
                 title= str(title)
             elif l ==  marker_clas['in'][list(marker_clas.get('in'))[0]]["class_n"]:
                 ingredints = z
                 
         except:
             continue
                 
                 
         redic = {"title":title,"methods":[method],"ingredints":[ingredints]}        
         #print(redic)
        
         recipelist.append(redic)
        #print(recipelist)
        with open ('recipe.pkl',"wb") as fp:
         pickle.dump(recipelist,fp)
       # print(recipelist)
        return recipelist
    # return a dict of a website html tagv and class names used to find the required content from said website 
    def web_site_dic(self, website):
        x = website
        title_class_n = ''
        title_marker = 'title' 
        title_dilemter=' '
        if 'www.delish' in x:  
         
          ingerdint_marker='div-2'
          ingerdint_class_n='ingredients'
          method_class_n ='direction-lists'
          method_marker = 'div'
         
          ingredint_dilemter='div class="ingredient-item"'
          method_dilemter = 'li'
        
        if 'www.bbcgood'in x:
          ingerdint_marker='section'
          ingerdint_class_n='recipe__ingredients col-12 mt-md col-lg-6'
          method_class_n ='grouped-list__list list'
          method_marker = 'ul'
          ingredint_dilemter='li'
          method_dilemter = 'p'
          
        marker_clas = {"in":{ingerdint_marker: {"class_n":ingerdint_class_n,"dilemter": ingredint_dilemter}},
                       "meth":{method_marker: {'class_n':method_class_n,'dilemter':method_dilemter}},
                      "titl":{title_marker: {'class_n':title_class_n,'dilemter':title_dilemter}}}
        
        return marker_clas
    
    
    # takes in html and a dimlimeter to be able to convert the conten in to a list format removbing and cleaning up aspect of ther html 
    def htl_list_conver(self,html_conten,dilemter):
        hc = html_conten
        
        for value in dilemter:
         if value != ' ':
         
          #print(hc) 
          if 'class=' in value: 
           
           d=str(value)
           print(d)
           d12= d.find(' ')
           d1= d[0:d12]
           d22=d.find('"')+1
           d2= d[d22:-1]
           
           hc= hc.find_all(d1, class_=d2)
           li= []
           for ingredint in hc:
            s= str(ingredint.get_text())
            s= s.replace('\t', '')
            s= s.replace('\n', ' ')
           
            li.append(s)
           hc=li
            
           
          else:
          
           try:
            hc= hc.find_all(dilemter)
           #print(hc)
            li= []
            for method in hc:
             li.append(method.text)   
            hc= li
           except:
                return hc
        return hc
        
    def list_converter(self,string_list):
        sl=string_list
        sl = str(sl)
        sl= sl.split('')
   
        return sl
    # methos that use a term and a search url to return a list of urls on website page 
    def term_searcher(self,term,site):
          url= site+term
      
          urllist=[] 
          r=requests.get(url)
          r= r.text
          r= BeautifulSoup(r,'html.parser')
          res= r.find_all('a')
          for urls_ in res:
           urls_=str(urls_)
           res1= urls_.find('href="')+6
           re2=urls_.find('"',res1)
           url_=urls_[res1:re2]
           urllist.append(url_)
          return urllist
    # methos for searching terms and returning url list    
    def recipe_searcher(self,dish_title=None,ingrdints_have=None,region=None,dish_type=None):
       url_list=url_list_search
       recipe_url=[]
       #internal method used to reconstruct url to seachable versions 
       def base_url_add(url_):  
          
           
           if 'bbcgoodfood' in site_:
               
               url_= 'https://www.bbcgoodfood.com'+url_
               
               if '/recipe' in url_:
                   recipe_url.append(url_)
           elif 'delish' in site_:
             
               url_= 'https://www.delish.com'+url_
               
               if '/recipe-ideas' in url_:
                   resp=requests.get(url_)
                   resp= resp.text
                   if'recipeIngredient'in resp:
                     recipe_url.append(url_) 
       if dish_title != None : 
          
        for site_ in url_list:
         search_url=self.term_searcher(dish_title, site_)
         for url_ in search_url:
        
         
                     
          base_url_add(url_) 
       
      
                       
       elif region != None :
              
              for site_ in url_list:
               for ing in region:  
                search_url=self.term_searcher(ing, site_)
           
               for url_ in search_url:
                base_url_add(url_)     
       #print(recipe_url)
       elif dish_type != None:
            
            for site_ in url_list:
              for ing in dish_type:  
               search_url=self.term_searcher(ing, site_)
           
              for url_ in search_url:
               base_url_add(url_)  
               
       elif ingrdints_have != None :
            
            for site_ in url_list:
              for ing in ingrdints_have:  
               search_url=self.term_searcher(ing, site_)
           
              for url_ in search_url:
               base_url_add(url_)            
       else:
           print('must have at least one input')
       recipe_url = list(dict.fromkeys(recipe_url))
       return recipe_url    
   
    #taske in recpie specfication and finds the recipes that include all or one of the items 
    def recipe_filter(self,dish_title=None,ingrdints_have=None,region=None,ingredints_no_have=None,dish_type=None,difficlty=None,include = 'All'):
        #calls method that retruns a list of urls takes in search terms 
        url_list= self.recipe_searcher(dish_title,ingrdints_have,region,dish_type)
        if region != None:
            for site in url_list_search:
                region_list=self.term_searcher(region, site)
                for url in region_list:
                 region_list = self.recipe_searcher.base_url_add(url)
            #url_list= url_list.append(region_list) 
            #url_list= pd.DataFrame(url_list)
           # url_list[url_list.duplicated(keep=False)]
           # url_list.drop_duplicates()
           # url_list=url_list.values.tolist()
        #print(url_list)    
        recipecs= self.recipe_assembler(url_list)
        with open("recipe.pkl",'rb') as fp:
            recipecs= pickle.load(fp)
       
        fin_rec_list=[]
        #recipecs =[{'title': 'Tomato & mozzarella toastie recipe | BBC Good Food', 'methods': [['Spread the bread with the tomato pizza or pasta sauce. Scatter torn mozzarella and a few torn basil leaves over one slice, then add any meat or veggies you like – shredded chicken or ham, pepperoni, sweetcorn, onions or roasted peppers all work well. Top with the other slice of bread, then butter the outsides of the sandwich. Cook in a hot pan, weighed down by another heavy pan, for 2-3 mins on each side until the outside is crisp and the cheese has melted. Alternatively, cook in a sandwich toaster. Top with a few whole basil leaves and serve.']], 'ingredints': [['2 slices of bread', 'chicken','pesto', '100g mozzarella','2 tbsp tomato pasta or pizza sauce','garlic', '50g torn mozzarella', 'a few torn basil leaves and a few whole leaves', 'shredded chicken or ham, pepperoni, sweetcorn, onions or roasted peppers', 'butter']]}]
        for recipe in recipecs:
           
           if ingrdints_have != None:
                ingr= recipe["ingredints"]
               
                   
                ingr = pd.DataFrame(ingr)
               
                ingr= ingr.values
                ingr= ingr.ravel()
                if len(ingr)> 0: 
                 #print( recipe, ingrdints_have)
                 ingr = ingr.tolist()
                 ingr = ' '.join(ingr).split()
                # print(ingrdints_have,ingr)
                if include == 'All':
                 if all(item in ingr for item in ingrdints_have ) :
                   fin_rec_list.append(recipe)
                   
                   print(recipe)
                 else:
                    if any(item in ingr for item in ingrdints_have ) :
                     fin_rec_list.append(recipe)
                   
                     print(recipe)
                     
        print(fin_rec_list)   
            
    
   
    
   
if __name__ == "__main__":
    food_finder().main()    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
f= food_finder()