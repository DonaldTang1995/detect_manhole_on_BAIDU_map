import json
import factory
import logging
import web
from config import conf
class UCS:
    def check(self,keys):
        for key in keys:
            if key not in self.data:
                return key

        return None

    def POST(self,name):
        self.data=json.loads(web.data())
        temp=self.check(['command'])
        if temp!=None:
            return temp+" not found"
        commend=self.data['command']
        user=None 

        if commend=="login":
            temp=self.check(['username','password'])
            if temp!=None:
                return temp+ "not found"
            username,password=self.data['username'],self.data['password']

            if factory.create_user(username=username,password=password)==None:
                return "fail"
            else:
                return "succeed"
        else:
            temp=self.check(['token'])
            token=self.data['token']
            user=factory.get_user(token)

        if command=="search_by_name":
            temp=self.check(['placename','center'])
            if temp!=None:
                return temp+ " not found"

            center,place_name=self.data['center'],self.data['placename']
            return user.search_by_name(center=center,place_name=place_name)
        elif command=="search_bounding_box":
            temp=self.check(['xmin','ymin','xmax','ymax','placename'])
            if temp!=None:
                return temp+ " not found"

            xmin,ymin,xmax,ymax,place_name=self.data['xmin'],self.data['ymin'],self.data['xmax'],self.data['ymax'],self.data['placename']
            return user.search_bounding_box(xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax,place_name=place_name)
        elif command=="search_coordinate":
            temp=self.check(['longtitude','latitude'])
            if temp!=None:
                return temp+ " not found"

            longtitude,latitude=self.data['longtitude'],self.data['latitude']
            return user.search_coordinate(longtitude=longtitude,latitude=latitude)
        elif command=="image_analysis":
            temp=self.check(['limit'])
            if temp!=None:
                return temp+ " not found"

            image_number=self.data['limit']
            return user.image_analysis(image_number)
        elif command=="logout":
            if factory.remove_user(token):
                return "succeed removing "+token
            else:
                return "fail to remove "+token
        else:
            return "unknow command"

            

