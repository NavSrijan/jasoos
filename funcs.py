from discord import Embed
import pycountry
import configparser
import pdb

#VARIABLES

config = configparser.ConfigParser()
config.read("config")
config = config['credentials']

class Person():
    def __init__(self, author):
        self.state = 0
        
        self.messages = []
        self.pfp = ""

        self.id = author.id
        self.name = " "
        self.age = " "
        self.gender = " "
        self.hobbies = " "
        self.location = " "

        self.indian = False
    def returnEmbed(self, check=False):
        my = Embed(set_author_name=config["botName"],
                   title = self.name,
                   description = '**Introduction**',
                   color=0xf1c40f ) 
        my.add_field(name='Age', value=self.age, inline=True)
        my.add_field(name='Gender', value=self.gender, inline=True)
        my.add_field(name='Hobbies', value=self.hobbies, inline=False)
        my.add_field(name='Location', value=self.location, inline=False)
        
        my.set_thumbnail(url=(self.pfp))
        
        if check:
            my.set_footer(text="Is this correct? y/n")
        return my
def returnStateEmbed():
    states = list(pycountry.subdivisions.get(country_code="IN"))
    states_names = []
    for i in states:
        states_names.append(i.name)
    states_names.sort()
    desc = ""
    j=1
    for i in states_names:
        desc+=str(j) + ". " + i+"\n"
        j+=1

    desc += "\n\n Input the number corresponding to your state of residence."
    emb = Embed(title="States", description=desc)
    return emb

def takeIntro(p1,msg=""):

    state = p1.state
    reply = ""
    response = True
    isEmbed = False
    if state == 0:
        p1.state+=1
        reply = ("What is your name?")
        p1.messages.append(msg)
        
    elif state == 1:
        p1.name = msg.content
        reply = "Are you 18+ or 18-?"
        p1.reaction = True
        p1.state+=1
        p1.messages.append(msg)
    elif state == 2:
        p1.age = msg.content
        reply = "Gender?"
        p1.state+=1
        p1.messages.append(msg)
    elif state == 3:
        p1.gender = msg.content
        reply = "Are you from India?"

        '''
        If Indian, state +1
        else, state +2
        '''

        p1.state+=1
        p1.messages.append(msg)

    elif state == 4:
        tLoc = msg.content
        if tLoc.lower() in ["yes","y", "yes", "yep", "yus", "yup", "yeah", "haan", "han", "haan bhai"]:
            reply = "Which state are you from?"
            isEmbed = True
            reply = returnStateEmbed()
            p1.messages.append(msg)
            p1.state+=1
        else:
            reply = "Which country are you from?"
            p1.messages.append(msg)
            p1.state+=2
    elif state == 5:
        # If the person introducing is Bhartiya
        tLoc = msg.content
        try:
            tLoc = int(tLoc)
            states = list(pycountry.subdivisions.get(country_code="IN"))
            states_names = []
            for i in states:
                states_names.append(i.name)
            states_names.sort()
            state = states_names[tLoc-1]
            reply = f"Okay. So, you are from {state}\n What are your hobbies?"
            p1.messages.append(msg)
            p1.indian = True
            p1.location = state
            p1.state+=2
        except:
            reply = "Enter a valid number."
    elif state == 6:
        # If the person introducing is Videshi
        tLoc = msg.content
        countries = list(pycountry.countries)
        try:
            country  = pycountry.countries.search_fuzzy(tLoc)
            if len(country)>0:
                country = country[0]
                p1.location = country.name
                reply = f"So, you are from {country.name}\n What are your hobbies?"
                p1.state+=1
                p1.messages.append(msg)
            else:
                print("ERROR ASSIGNING COUNTRY")
                raise Exception
        except:
            reply = "Your country is not big enough."
            p1.messages.append(msg)
    elif state == 7:
        tLoc = msg.content
        p1.hobbies = tLoc
        reply = p1.returnEmbed(check=True)
        isEmbed=True
        p1.messages.append(msg)
        p1.state+=1
    elif state == 8:
        tLoc = msg.content
        if tLoc.lower() in ["yes","y", "yes", "yep", "yus", "yup", "yeah", "haan", "han", "haan bhai"]:
            p1.state+=1
        else:
            p1.state+=2
        if p1.state == 9:
            reply = ""
            response = False
            p1.messages.append(msg)
        elif p1.state == 10:
            reply = "RESTART"
            response = False
            p1.messages.append(msg)
    
    return p1,reply,response,isEmbed
