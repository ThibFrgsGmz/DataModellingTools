#
# (C) Semantix Information Technologies.
#
# Semantix Information Technologies is licensing the code of the
# Data Modelling Tools (DMT) in the following dual-license mode:
#
# Commercial Developer License:
#       The DMT Commercial Developer License is the suggested version
# to use for the development of proprietary and/or commercial software.
# This version is for developers/companies who do not want to comply
# with the terms of the GNU Lesser General Public License version 2.1.
#
# GNU LGPL v. 2.1:
#       This version of DMT is the one to use for the development of
# applications, when you are willing to comply with the terms of the
# GNU Lesser General Public License version 2.1.
#
# Note that in both cases, there are no charges (royalties) for the
# generated code.
#
import re

from commonPy.utility import panicWithCallStack
from commonPy.asnAST import AsnBasicNode, AsnSequence, AsnSet, AsnChoice, AsnSequenceOf, AsnSetOf, AsnEnumerated, AsnMetaMember


class RecursiveMapper:

    def maybeElse(self, childNo):
        if childNo == 1:
            return ""
        else:
            return "else "

    def CleanName(self, fieldName):
        return re.sub(r'[^a-zA-Z0-9_]', '_', fieldName)

    def Version(self):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapInteger(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapReal(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapBoolean(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapOctetString(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapEnumerated(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapSequence(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapSet(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapChoice(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapSequenceOf(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def MapSetOf(self, unused_srcVar, unused_destVar, unused_node, unused_leafTypeDict, unused_names):
        panicWithCallStack("Method undefined in a RecursiveMapper...")

    def Map(self, srcVar, destVar, node, leafTypeDict, names):
        if isinstance(node, str):
            node = names[node]
        lines = []
        if isinstance(node, AsnBasicNode):
            realLeafType = leafTypeDict[node._leafType]
            if realLeafType == "INTEGER":
                lines.extend(self.MapInteger(srcVar, destVar, node, leafTypeDict, names))
            elif realLeafType == "REAL":
                lines.extend(self.MapReal(srcVar, destVar, node, leafTypeDict, names))
            elif realLeafType == "BOOLEAN":
                lines.extend(self.MapBoolean(srcVar, destVar, node, leafTypeDict, names))
            elif realLeafType == "OCTET STRING":
                lines.extend(self.MapOctetString(srcVar, destVar, node, leafTypeDict, names))
            else:
                panicWithCallStack("Basic type %s can't be mapped..." % realLeafType)
        elif isinstance(node, AsnSequence):
            lines.extend(self.MapSequence(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnSet):
            lines.extend(self.MapSet(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnChoice):
            lines.extend(self.MapChoice(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnSequenceOf):
            lines.extend(self.MapSequenceOf(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnSetOf):
            lines.extend(self.MapSetOf(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnEnumerated):
            lines.extend(self.MapEnumerated(srcVar, destVar, node, leafTypeDict, names))
        elif isinstance(node, AsnMetaMember):
            lines.extend(self.Map(srcVar, destVar, names[node._containedType], leafTypeDict, names))
        else:
            panicWithCallStack("unsupported %s (%s)" % (str(node.__class__), node.Location()))
        return lines