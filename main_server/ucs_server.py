import json
import factory
import logging
import web
from config import conf
from common import check_keys
class UCS:

    def POST(self,name):
        self.data=json.loads(web.data())
        if 'command' not in self.data:
	    return 'command not found'
        
        command=self.data['command']
        user=None 

        if command=="login":
            temp=check_keys(self.data,['username','password'])
            if temp!=None:
                return temp+ "not found"
            username,password=self.data['username'],self.data['password']

            if factory.create_user(username=username,password=password)==None:
                return "fail"
            else:
                return "succeed"
        else:
	    temp=check_keys(self.data,['token'])
            if temp!=None:
		return temp+" not found"

	    token=self.data['token']
            user=factory.get_user(token)
	
	if command in user.functions:
	    return user.functions[command](self.data)
        else:
	    return "unknown command"    

