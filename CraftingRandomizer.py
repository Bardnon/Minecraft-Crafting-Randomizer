import os
import random
import io
import json
import sys

if len(sys.argv) >= 2:
    try:
        seed = int(sys.argv[1])
    except Exception:
        exit()
    random.seed(seed)
else:
    print('To enter a seed, use: "python Crafting Randomizer.py <seed>"')
print('Creating Datapack')

file_list = []
results = {}
for file in os.listdir('./recipes'):
    with open('./recipes/' + file) as json_file:
        data = json.load(json_file)
        if 'result' in data:
            if 'item' in data['result']:
                if data['result']['item'] != 'minecraft:crafting_table':
                    file_list.append(file)
                    if data['result']['item'] not in results:
                        if 'count' in data['result']:
                            results[data['result']['item']] = data['result']['count']
                        else:
                            results[data['result']['item']] = 1
                    else:
                        temp_name = data['result']['item']
                        while temp_name in results:
                            temp_name += '~'
                        if 'count' in data['result']:
                            results[temp_name] = data['result']['count']
                        else:
                            results[temp_name] = 1
            else:
                file_list.append(file)
                if data['result'] not in results:
                    if 'count' in data['result']:
                        results[data['result']] = data['count']
                    else:
                        results[data['result']] = 1
                else:
                    temp_name = data['result']
                    while temp_name in results:
                        temp_name += '~'
                    if 'count' in data['result']:
                        results[temp_name] = data['count']
                    else:
                        results[temp_name] = 1

if not os.path.exists('./Random Crafting/data/minecraft/recipes'):
    os.makedirs('./Random Crafting/data/minecraft/recipes')
if not os.path.exists('./Random Crafting/data/minecraft/tags/functions'):
    os.makedirs('./Random Crafting/data/minecraft/tags/functions')
if not os.path.exists('./Random Crafting/data/random_crafting/functions'):
    os.makedirs('./Random Crafting/data/random_crafting/functions')

for outcome in results:
    item_name = outcome.replace('~','')
    i = random.randint(0, len(file_list) - 1)
    with open('./recipes/' + file_list[i]) as json_file:
        data = json.load(json_file)
        if 'group' in data:
            del data['group']
        if 'item' in data['result']:
            if 'count' in data['result']:
                data['result']['item'] = item_name
                data['result']['count'] = results[outcome]
            else:
                data['result']['item'] = item_name
        else:
            if 'count' in data['result']:
                data['result'] = item_name
                data['count'] = results[outcome]
            else:
                data['result'] = item_name
        with open('./Random Crafting/data/minecraft/recipes/' + file_list[i], 'w') as output:
            json.dump(data, output, indent=4)
    del file_list[i]


with open('./Random Crafting/pack.mcmeta','w') as pack:
    pack.write(json.dumps({'pack':{'pack_format':1, 'description':'Crafting Randomizer'}}, indent=4))
with open('./Random Crafting/data/minecraft/tags/functions/load.json','w') as load:
    load.write(json.dumps({"values": ["random_crafting:reset"]}, indent=4))
with open('./Random Crafting/data/minecraft/tags/functions/tick.json','w') as tick:
    tick.write(json.dumps({"values": ["random_crafting:main"]}, indent=4))
with open('./Random Crafting/data/random_crafting/functions/reset.mcfunction','w') as reset:
    reset.write('tellraw @a ["",{"text":"Crafting Randomizer by Bardnon","color":"blue"}]')
with open('./Random Crafting/data/random_crafting/functions/main.mcfunction','w') as main:
    main.write('recipe give @a *')

print('Created Datapack')
