import requests
import jsons

baseURL = 'http://127.0.0.1:5000'

r = requests.get(baseURL+'/gags?name=Whole Cream Pie')
r.status_code
newGag = r.json()[0]
newGag['name'] = "Pastry Cannon"
newGag['value'] = 185
r = requests.post(baseURL+'/gags', json = newGag)
r.status_code
r.json()
# plan = [jsons.dump(gag) for gag in plan]
# toons = [jsons.dump(toon) for toon in toons]
# cogs = [jsons.dump(cog) for cog in cogs]
# plan
r = requests.post(baseURL+'/submit', json = newGag)
r.status_code
r.text
