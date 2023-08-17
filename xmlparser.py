import xml.etree.ElementTree as ET
import json

# xmlfile = ET.parse("P:/AndreJukebox/assets/sets/city/publish/xml/block_builder.xml")
xmlfile = ET.parse("P:/AndreJukebox/assets/sets/city/publish/xml/city_builder.xml")
root = xmlfile.getroot()
groupsList = []
assetList = []
blocksdict = {}
assetdict = {}

def assetListFromXML():
    for instanceList in root:
        for instance in instanceList:
            for childInstance in instance[2]:
                groupIteration = f'{(int(childInstance.attrib["name"].split(":")[0].rsplit("_",1)[1])):04d}'
                group = f'{childInstance.attrib["name"].split(":")[0].rsplit("_",1)[0]}_{groupIteration}'
                groupXform = childInstance[1].attrib["value"]
                groupBound = childInstance[0].attrib
                groupasset = f'{childInstance.attrib["name"].split(":")[0].rsplit("_",1)[0]}'
                groupusd = f'P:/AndreJukebox/assets/sets/{groupasset}/publish/usd/{groupasset}.usd'
                
                tr = groupXform.split(" ")
                tdict = {}
                iter = 0
                for i in tr:
                    iter = iter + 1
                    tdict[iter] = i
                group_matrix = f'( ({tdict[1]},{tdict[2]},{tdict[3]},{tdict[4]}),({tdict[5]},{tdict[6]},{tdict[7]},{tdict[8]}),({tdict[9]},{tdict[10]},{tdict[11]},{tdict[12]}),({tdict[13]},{tdict[14]},{tdict[15]},{tdict[16]}) )'

                groupsList.append(group)
                for assetGroups in childInstance[2]:
                    assetdict = {}
                    for assetUnit in assetGroups[2]:
                        assetname = assetUnit.attrib["name"].split(":")
                        assetclean = assetname[2].rsplit("_",1)[0]
                        
                        # final info variables
                        assetpath = assetUnit.attrib["refFile"]
                        usdassetpath = assetpath.replace(".abc",".usd").replace('publish/cache','publish/usd')
                        assetInstance = f'{assetclean}_{int(assetname[1].rsplit("_",1)[1]):04d}'
                        xform = assetUnit[1].attrib["value"]
                        bounds = assetUnit[0].attrib
                        tr = xform.split(" ")
                        tdict = {}
                        iter = 0
                        for i in tr:
                            iter = iter + 1
                            tdict[iter] = i
                        asset_matrix = f'( ({tdict[1]},{tdict[2]},{tdict[3]},{tdict[4]}),({tdict[5]},{tdict[6]},{tdict[7]},{tdict[8]}),({tdict[9]},{tdict[10]},{tdict[11]},{tdict[12]}),({tdict[13]},{tdict[14]},{tdict[15]},{tdict[16]}) )'
                        assetList.append(assetInstance)
                        assetdict[assetInstance] = {"xform":asset_matrix, "abcpath":assetpath,"usdpath":usdassetpath}
                        blocksdict[group] = {"xform":group_matrix, "usdpath":groupusd, "assets":assetdict}
assetListFromXML()

# with open('P:/AndreJukebox/assets/sets/city/publish/xml/block_builder.json', 'w') as outdict:
#     json.dump(blocksdict, outdict)

with open('P:/AndreJukebox/assets/sets/city/publish/xml/city_builder.json', 'w') as outdict:
    json.dump(blocksdict, outdict)