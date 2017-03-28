import json
import factory
import logging
import web
from config import conf
from common import check_keys
class UCS:

    def POST(self):
        self.data=json.loads(web.data())
        
        if 'command' not in self.data:
            return 'command not found'
        command=self.data['command']
        if command=="login":
            temp=check_keys(self.data,['username','password'])
            if temp!=None:
                return temp+ "not found"
            username,password=self.data['username'],self.data['password']

            if factory.create_user(username=username,password=password)==None:
                return "fail to login in"
            else:
                return json.dumps("login in sucessfully")
        else:
            temp=check_keys(self.data,['token'])
            if temp!=None:
                return temp+" not found"
            token=self.data['token']
            user=factory.get_user(token)

        functions={'change_map_engine':user.change_map_engine,'search_by_name':user.search_by_name,'search_bounding_box':user.search_bounding_box,'search_coordinate':user.search_coordinate,'image_analysis':user.image_analysis} 
        if command in functions:
            return functions[command](self.data)
        else:
            return "unknown command"    
        
