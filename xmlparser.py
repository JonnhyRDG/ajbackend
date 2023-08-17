import xml.etree.ElementTree as ET
import json

xmlblock = ET.parse("P:/AndreJukebox/assets/sets/city/publish/xml/block_builder.xml")
xmlcity = ET.parse("P:/AndreJukebox/assets/sets/city/publish/xml/city_builder.xml")

blocksdict = {}
assetdict = {}

def assetListFromXML(xml):
    root = xml.getroot()
    for instanceList in root:
        for instance in instanceList:
            for childInstance in instance[2]:
                groupIteration = f'{(int(childInstance.attrib["name"].split(":")[0].rsplit("_",1)[1])):04d}'
                if xml == "xmlblock":
                    group = f'{childInstance.attrib["name"].split(":")[0].rsplit("_",1)[0]}_{groupIteration}'
                else:
                    group = f'{childInstance.attrib["name"].split(":")[0].rsplit("_",1)[0]}'
                groupXform = childInstance[1].attrib["value"]
                groupasset = f'{childInstance.attrib["name"].split(":")[0].rsplit("_",1)[0]}'
                groupusd = f'P:/AndreJukebox/assets/sets/{groupasset}/publish/usd/{groupasset}.usd'

                # Reformat the matrix string for USD
                tr = groupXform.split(" ")
                tdict = {}
                iter = 0
                for i in tr:
                    iter = iter + 1
                    tdict[iter] = i

                group_matrix = f'( ({tdict[1]},{tdict[2]},{tdict[3]},{tdict[4]}),({tdict[5]},{tdict[6]},{tdict[7]},{tdict[8]}),({tdict[9]},{tdict[10]},{tdict[11]},{tdict[12]}),({tdict[13]},{tdict[14]},{tdict[15]},{tdict[16]}) )'


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

                        # Reformat the matrix string for USD
                        tr = xform.split(" ")
                        tdict = {}
                        iter = 0
                        for i in tr:
                            iter = iter + 1
                            tdict[iter] = i

                        asset_matrix = f'( ({tdict[1]},{tdict[2]},{tdict[3]},{tdict[4]}),({tdict[5]},{tdict[6]},{tdict[7]},{tdict[8]}),({tdict[9]},{tdict[10]},{tdict[11]},{tdict[12]}),({tdict[13]},{tdict[14]},{tdict[15]},{tdict[16]}) )'
                        assetdict[assetInstance] = {"xform":asset_matrix, "abcpath":assetpath,"usdpath":usdassetpath}
                        blocksdict[group] = {"xform":group_matrix, "usdpath":groupusd, "assets":assetdict}
    
    if xml == xmlblock:
        with open('P:/AndreJukebox/assets/sets/city/publish/xml/block_builder.json', 'w') as blockdict:
            json.dump(blocksdict, blockdict)
    else:
        with open('P:/AndreJukebox/assets/sets/city/publish/xml/city_builder.json', 'w') as citydict:
            json.dump(blocksdict, citydict)

assetListFromXML(xml=xmlblock)
assetListFromXML(xml=xmlcity)