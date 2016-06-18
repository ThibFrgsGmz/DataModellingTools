#!/usr/bin/env python
# vim: set expandtab ts=8 sts=4 shiftwidth=4

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
import os
import sys
import copy

from typing import Tuple

import commonPy.configMT
from commonPy.asnAST import sourceSequenceLimit, AsnNode  # NOQA pylint: disable=unused-import
from commonPy.asnParser import (  # NOQA
    AST_Lookup, AST_TypesOfFile, AST_TypenamesOfFile, AST_Leaftypes,
    Typename, Filename, ParseAsnFileList)
from commonPy.utility import inform, panic
import commonPy.cleanupNodes
from commonPy.recursiveMapper import RecursiveMapper

import commonPy.verify

__doc__ = '''\
This is one of the code generators that Semantix developed for
the European research project ASSERT. It is now enhanced in the
context of Data Modelling and Data Modelling Tuning projects.

It reads the ASN.1 specification of the exchanged messages, and
generates "printer" functions for their content.
'''


def usage():
    '''Print usage instructions.'''
    msg = 'Usage: %s <options> input1.asn1 [input2.asn1]...\nWhere options are:\n'
    msg += '\t-o dirname\t\tDirectory to place generated files\nAnd one of:\n'
    msg += '\t-verbose\t\tDisplay more debug output\n'


class Printer(RecursiveMapper):
    def __init__(self):
        self.uniqueID = 0

    def UniqueID(self):
        self.uniqueID += 1 if self.uniqueID != 385 else 2
        return self.uniqueID

    def MapInteger(self, srcCVariable, empty, _, __, ___):
        lines = []
        lines.append('#if WORD_SIZE==8')
        lines.append('printf("%%lld", %s);' % srcCVariable)
        lines.append('#else')
        lines.append('printf("%%d", %s);' % srcCVariable)
        lines.append('#endif')
        return lines

    def MapReal(self, srcCVariable, empty, _, __, ___):
        return ['printf("%%f", %s);' % srcCVariable]

    def MapBoolean(self, srcCVariable, empty, _, __, ___):
        return ['printf("%%s", (int)%s?"TRUE":"FALSE");' % srcCVariable]

    def MapOctetString(self, srcCVariable, empty, node, __, ___):
        lines = []
        lines.append("{")
        lines.append("    int i;")
        limit = sourceSequenceLimit(node, srcCVariable)
        lines.append('    printf("\'");')
        lines.append("    for(i=0; i<%s; i++)" % limit)
        lines.append('        printf("%%02x", %s.arr[i]);' % srcCVariable)
        lines.append('    printf("\'H");')
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcCVariable, empty, node, __, ___):
        lines = []
        lines.append("switch(%s) {" % srcCVariable)
        for d in node._members:
            lines.append("case %s:" % d[1])
            lines.append("    printf(\"%s\");" % d[0])
            lines.append("    break;")
        lines.append("default:")
        lines.append("    printf(\"Invalid value in ENUMERATED (%s)\");" % srcCVariable)
        lines.append("}")
        return lines

    def MapSequence(self, srcCVariable, prefix, node, leafTypeDict, names):
        lines = []
        lines.append("printf(\"{\");")
        for idx, child in enumerate(node._members):
            if idx > 0:
                lines.append("printf(\", \");")
            lines.append("printf(\"%s \");" % child[0])  # Sequences need the field name printed
            lines.extend(
                self.Map(
                    "%s.%s" % (srcCVariable, self.CleanName(child[0])),
                    prefix + "::" + self.CleanName(child[0]),
                    child[1],
                    leafTypeDict,
                    names))
        lines.append("printf(\"}\");")
        return lines

    def MapSet(self, srcCVariable, prefix, node, leafTypeDict, names):
        return self.MapSequence(srcCVariable, prefix, node, leafTypeDict, names)

    def MapChoice(self, srcCVariable, prefix, node, leafTypeDict, names):
        lines = []
        childNo = 0
        for child in node._members:
            childNo += 1
            lines.append(
                "%sif (%s.kind == %s) {" %
                (self.maybeElse(childNo), srcCVariable, self.CleanName(child[2])))
            lines.append("    printf(\"%s:\");" % child[0])  # Choices need the field name printed
            lines.extend(['    '+x for x in self.Map(
                         "%s.u.%s" % (srcCVariable, self.CleanName(child[0])),
                         prefix + "::" + self.CleanName(child[0]),
                         child[1],
                         leafTypeDict,
                         names)])
            lines.append("}")
        return lines

    def MapSequenceOf(self, srcCVariable, prefix, node, leafTypeDict, names):
        lines = []
        lines.append("{")
        uniqueId = self.UniqueID()
        lines.append("    int i%s;" % uniqueId)
        lines.append("    printf(\"{\");")
        limit = sourceSequenceLimit(node, srcCVariable)
        lines.append("    for(i%s=0; i%s<%s; i%s++) {" % (uniqueId, uniqueId, limit, uniqueId))
        lines.append("        if (i%s) " % uniqueId)
        lines.append("            printf(\",\");")
        lines.extend(["        " + x for x in self.Map(
                     "%s.arr[i%s]" % (srcCVariable, uniqueId),
                     prefix + "::Elem",
                     node._containedType,
                     leafTypeDict,
                     names)])
        lines.append("    }")
        lines.append("    printf(\"}\");")
        lines.append("}")
        return lines

    def MapSetOf(self, srcCVariable, prefix, node, leafTypeDict, names):
        return self.MapSequenceOf(srcCVariable, prefix, node, leafTypeDict, names)


def main():
    sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0])))
    sys.path.append('commonPy')

    if sys.argv.count("-o") != 0:
        idx = sys.argv.index("-o")
        try:
            commonPy.configMT.outputDir = os.path.normpath(sys.argv[idx+1]) + os.sep
        except:  # pragma: no cover
            usage()  # pragma: no cover
        del sys.argv[idx]
        del sys.argv[idx]
        if not os.path.isdir(commonPy.configMT.outputDir):
            panic("'%s' is not a directory!\n" % commonPy.configMT.outputDir)  # pragma: no cover

    if "-verbose" in sys.argv:
        commonPy.configMT.verbose = True
        sys.argv.remove("-verbose")

    if len(sys.argv) < 2:
        usage()

    for f in sys.argv[1:]:
        if not os.path.isfile(f):
            panic("'%s' is not a file!\n" % f)  # pragma: no cover

    ParseAsnFileList(sys.argv[1:])

    Triples = Tuple[AST_Lookup, List[AsnNode], AST_Leaftypes]  # NOQA pylint: disable=unused-variable
    uniqueASNfiles = {}  # type: Dict[Filename, Triples]

    for asnFile in uniqueASNfiles:
        tmpNames = {}  # Dict[Typename, AsnNode]
        for name in commonPy.asnParser.g_typesOfFile[asnFile]:
            tmpNames[name] = commonPy.asnParser.g_names[name]

        uniqueASNfiles[asnFile] = (
            copy.copy(tmpNames),                            # map Typename to type definition class from asnAST
            copy.copy(commonPy.asnParser.g_astOfFile[asnFile]),    # list of nameless type definitions
            copy.copy(commonPy.asnParser.g_leafTypeDict)    # map from Typename to leafType
        )

        inform("Checking that all base nodes have mandatory ranges set in %s..." % asnFile)
        for node in list(tmpNames.values()):
            commonPy.verify.VerifyRanges(node, commonPy.asnParser.g_names)

    # If some AST nodes must be skipped (for any reason), go learn about them
    badTypes = commonPy.cleanupNodes.DiscoverBadTypes()

    C_HeaderFile = open(commonPy.configMT.outputDir + os.sep + "PrintTypesAsASN1.h", "w")
    C_HeaderFile.write('#ifndef __PRINTTYPESASASN1_H__\n')
    C_HeaderFile.write('#define __PRINTTYPESASASN1_H__\n\n')
    C_HeaderFile.write('#ifdef __cplusplus\n')
    C_HeaderFile.write('extern "C" {\n')
    C_HeaderFile.write('#endif\n\n')

    C_SourceFile = open(commonPy.configMT.outputDir + os.sep + "PrintTypesAsASN1.c", "w")
    C_SourceFile.write('#include <stdio.h>\n\n')
    C_SourceFile.write('#include "PrintTypesAsASN1.h"\n\n')
    C_SourceFile.write('#ifdef __linux__\n')
    C_SourceFile.write('#include <pthread.h>\n\n')
    C_SourceFile.write('static pthread_mutex_t g_printing_mutex = PTHREAD_MUTEX_INITIALIZER;\n\n')
    C_SourceFile.write('#endif\n\n')

    # Work on each ASN.1 file's types
    for asnFile in uniqueASNfiles:
        asn_name = os.path.basename(os.path.splitext(asnFile)[0])
        C_HeaderFile.write("#include \"%s.h\" // Generated by ASN1SCC\n\n" % asn_name)

        leafTypeDict = uniqueASNfiles[asnFile][2]
        inform("Executing mappings for types inside %s...", asnFile)
        names = uniqueASNfiles[asnFile][0]

        printer = Printer()

        for nodeTypename in names:
            # Check if this type must be skipped
            if nodeTypename in badTypes:
                continue
            node = names[nodeTypename]
            if node._isArtificial:
                continue
            cleanNodeTypename = printer.CleanName(nodeTypename)
            inform("Processing %s...", nodeTypename)

            # First, make sure we know what leaf type this node is
            assert(nodeTypename in leafTypeDict)

            C_HeaderFile.write('void PrintASN1%s(const char *paramName, const asn1Scc%s *pData);\n' % (cleanNodeTypename, cleanNodeTypename))
            C_SourceFile.write('void PrintASN1%s(const char *paramName, const asn1Scc%s *pData)\n{\n' % (cleanNodeTypename, cleanNodeTypename))
            C_SourceFile.write('#ifdef __linux__\n')
            C_SourceFile.write('    pthread_mutex_lock(&g_printing_mutex);\n')
            C_SourceFile.write('#endif\n')
            C_SourceFile.write('    //printf("%%s %s ::= ", paramName);\n' % nodeTypename)
            C_SourceFile.write('    printf("%s ", paramName);\n')
            # C_SourceFile.write('\n'.join(printer.Map('(*pData)', '', node, leafTypeDict, commonPy.asnParser.g_names)))
            lines = ["    "+x for x in printer.Map('(*pData)', '', node, leafTypeDict, commonPy.asnParser.g_names)]
            C_SourceFile.write("\n".join(lines))
            C_SourceFile.write('\n#ifdef __linux__\n')
            C_SourceFile.write('    pthread_mutex_unlock(&g_printing_mutex);\n')
            C_SourceFile.write('#endif\n')
            C_SourceFile.write('}\n\n')

    C_HeaderFile.write('\n#ifdef __cplusplus\n')
    C_HeaderFile.write('}\n')
    C_HeaderFile.write('#endif\n')
    C_HeaderFile.write('\n#endif\n')

if __name__ == "__main__":
    if "-pdb" in sys.argv:
        sys.argv.remove("-pdb")  # pragma: no cover
        import pdb  # pragma: no cover
        pdb.run('main()')  # pragma: no cover
    else:
        main()
