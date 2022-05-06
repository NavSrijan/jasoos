from discord import Embed
import pdb
class Person():
    def __init__(self, author):
        self.state = 0
        
        self.id = author.id
        self.name = ""
        self.age = ""
        self.gender = ""
        self.hobbies = ""
    def returnEmbed(self):
        my = Embed(title=self.name, description=f"{self.age}\n{self.gender}\n{self.location}",color=0xf1c40f)
        return my

def takeIntro(p1,msg=""):
    state = p1.state
    reply = ""
    if state == 0:
        p1.state+=1
        reply = ("What is your name?")
        response = True
    elif state == 1:
        p1.name = msg.content
        reply = "Are you 18+ or 18-?"
        p1.reaction = True
        response = True
        p1.state+=1
    elif state == 2:
        p1.age = msg.content
        reply = "Gender?"
        response = True
        p1.state+=1
    elif state == 3:
        p1.gender = msg.content
        reply = "Location?"
        response = True
        p1.state+=1
    elif state == 4:
        response = False
        p1.location = msg.content
        p1.state+=1

    return p1,reply,response
