import json
import sys


file = sys.argv[1]
with open(file) as file:
    data = json.load(file)


end_points = data['end-points']
switches = data['switches']
links = data['links']
possible_circuits = data['possible-circuits']
simulation = data['simulation']


link_capacity = {}
for link in links:
    a_dest, b_dest = link['points']
    
    link_capacity[f"{a_dest}<->{b_dest}"] = link['capacity']
    link_capacity[f"{b_dest}<->{a_dest}"] = link['capacity']


cnt = 0
for s in simulation['demands']:
    s['used-links'] = []  
    s['success'] = False  

for t in range(1, simulation['duration'] + 1):
    for s in simulation['demands']:
        end_point1, end_point2 = s['end-points']
        demand_value = s['demand']
        
        
        if s['end-time'] == t:
            if s['success']:  
                if not s['used-links']:
                    print("Fail")  
                else:
                    
                    for i in s['used-links']:
                        data['links'][i]['capacity'] += s['demand']
                cnt += 1
                print(f"{cnt}. demand deallocation: {end_point1}<->{end_point2} st:{t}")

        
        elif s['start-time'] == t:
            circuits = [c for c in possible_circuits
                        if (c[0] == end_point1 and c[-1] == end_point2)]
            s['success'] = False  

           
            for c in circuits:
                if s['success']:
                    break  
                s['success'] = True
                for frm, to in zip(c, c[1:]):
                    for li, link in enumerate(data['links']):
                        if link['points'] in [[frm, to], [to, frm]]:
                            
                            if link['capacity'] < demand_value:
                                s['success'] = False
                                break 
                            else:
                                s['used-links'].append(li)  
                if s['success']:
                    
                    for i in s['used-links']:
                        data['links'][i]['capacity'] -= demand_value
            cnt += 1
            print(f"{cnt}. demand allocation: {end_point1}<->{end_point2} st:{t} - {'successful' if s['success'] else 'unsuccessful'}")