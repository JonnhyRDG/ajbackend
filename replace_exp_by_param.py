from Katana import NodegraphAPI
node = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode')
expression = """("trans" if getParamRelative(self, '../pagePrefix') == "Transmission" else "base" if getParamRelative(self, '../pagePrefix') == "Base" else "rough" if getParamRelative(self, '../pagePrefix') == "Specular" else "bump" if getParamRelative(self, '../pagePrefix') == "Geometry" else "metal" if getParamRelative(self, '../pagePrefix') == "Metalness" else "emission" if getParamRelative(self, '../pagePrefix') == "Emission" else "sheen" if getParamRelative(self, '../pagePrefix') == "Sheen" else "sss" if getParamRelative(self, '../pagePrefix') == "Subsurface Scattering" else "coat" if getParamRelative(self, '../pagePrefix') == "Coat" else "normal" if getParamRelative(self, '../pagePrefix') == "Normal" else getParamRelative(self, '../../user.custommap') if getParamRelative(self, '../../user.maptype') == "Custom" else "--None found--") + '_'"""
for shader in node:
    shtype = shader.getParameter("nodeType").getValue(0) == "image"
    if shtype:
        shader.getParameter("publicInterface.namePrefix").setExpression(expression,1)

from Katana import NodegraphAPI
node = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode')
expression = """("trans" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Transmission" else "base" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Base" else "rough" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Specular" else "bump" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Geometry" else "metal" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Metalness" else "emission" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Emission" else "sheen" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Sheen" else "sss" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Subsurface Scattering" else "coat" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Coat" else "normal" if getParamRelative(self, '../../publicInterface.pagePrefix') == "Normal" else getParamRelative(self, '../../user.custommap') if getParamRelative(self, '../../publicInterface.pagePrefix') == "Custom" else "--None found--")"""
for shader in node:
    nodetype = shader.getParameter("nodeType").getValue(0) == "image"
    if nodetype:
        shtype = shader.getParameter("user.maptype")
        if shtype:
            shader.getParameter("user.maptype").setExpression(expression,1)