import json
import logging
import web
from config import conf
from common import check_keys,account_authentication
import user
class UCS:

    def POST(self):
        session=web.config._session
        self.data=json.loads(web.data())
         
        if 'command' not in self.data:
            return 'command not found'
        command=self.data['command']
        if command=="login":
            temp=check_keys(self.data,['username','password'])
            if temp!=None:
                return temp+ "not found"
            username,password=self.data['username'],self.data['password']

            session.token=account_authentication(username=username,password=password)
            if session.token==None:
                return "fail to login in"
            else:
                return json.dumps(token)
        else:
            temp=check_keys(self.data,['token'])
            if temp!=None:
                return temp+" not found"
            token=self.data['token']
            if session.token!=token:
                return "token is expired"
            temp_user=user.user(token,session.map_engine)

        functions={'change_map_engine':temp_user.change_map_engine,'search_by_name':temp_user.search_by_name,'search_bounding_box':temp_user.search_bounding_box,'search_coordinate':temp_user.search_coordinate,'image_analysis':temp_user.image_analysis} 
        if command in functions:
            return functions[command](self.data)
        else:
            return "unknown command"    
        
