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
'''
This is the implementation of the code mapper for C code.
As initially envisioned, ASSERT technology is not supposed
to support manually-made systems. A migration path, however,
that allows legacy hand-written code and modelling-tool
generated code to co-exist, can be beneficial in allowing
for a smooth transition. To that end, this backend (as well as
the Ada one) are written.

This is a backend for Semantix's code generator B (aadl2glueC).

C is a member of the asynchronous "club" (SDL, etc);
The subsystem developer (or rather, the APLC developer) is using
native C/C++ code to work with code generated by modelling tools.
To that end, this backend creates "glue" functions for input and
output parameters, which have C callable interfaces.
'''

from commonPy.utility import panic
from commonPy.asnAST import sourceSequenceLimit, isSequenceVariable, targetSequenceLimit

from commonPy.recursiveMapper import RecursiveMapper
from .asynchronousTool import ASynchronousToolGlueGenerator

isAsynchronous = True
cBackend = None


def Version():
    print("Code generator: " + "$Id: c_B_mapper.py 2390 2012-07-19 12:39:17Z ttsiodras $")


class FromCtoOSS(RecursiveMapper):
    def __init__(self):
        self.uniqueID = 0

    def UniqueID(self):
        self.uniqueID += 1
        return self.uniqueID

    def MapInteger(self, srcCVariable, destVar, _, __, ___):
        return ["%s = %s;\n" % (destVar, srcCVariable)]

    def MapReal(self, srcCVariable, destVar, _, __, ___):
        return ["%s = %s;\n" % (destVar, srcCVariable)]

    def MapBoolean(self, srcCVariable, destVar, _, __, ___):
        return ["%s = (char)%s;\n" % (destVar, srcCVariable)]

    def MapOctetString(self, srcCVariable, destVar, node, __, ___):
        lines = []
        lines.append("{\n")
        lines.append("    int i;\n")
        limit = sourceSequenceLimit(node, srcCVariable)
        lines.append("    for(i=0; i<%s; i++)\n" % limit)
        lines.append("        %s.value[i] = %s.arr[i];\n" % (destVar, srcCVariable))
        lines.append("    %s.length = %s;\n" % (destVar, limit))
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcCVariable, destVar, _, __, ___):
        return ["%s = %s;\n" % (destVar, srcCVariable)]

    def MapSequence(self, srcCVariable, destVar, node, leafTypeDict, names):
        lines = []
        for child in node._members:
            lines.extend(
                self.Map(
                    "%s.%s" % (srcCVariable, self.CleanName(child[0])),
                    destVar + "." + self.CleanName(child[0]),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcCVariable, destVar, node, leafTypeDict, names):
        return self.MapSequence(srcCVariable, destVar, node, leafTypeDict, names)  # pragma: nocover

    def MapChoice(self, srcCVariable, destVar, node, leafTypeDict, names):
        lines = []
        childNo = 0
        for child in node._members:
            childNo += 1
            lines.append("%sif (%s.kind == %s) {\n" %
                         (self.maybeElse(childNo), srcCVariable, self.CleanName(child[2])))
            lines.extend(['    '+x for x in self.Map(
                         "%s.u.%s" % (srcCVariable, self.CleanName(child[0])),
                         destVar + ".u." + self.CleanName(child[0]),
                         child[1],
                         leafTypeDict,
                         names)])
            lines.append("    %s.choice = OSS_%s_chosen;\n" % (destVar, self.CleanName(child[0])))
            lines.append("}\n")
        return lines

    def MapSequenceOf(self, srcCVariable, destVar, node, leafTypeDict, names):
        lines = []
        lines.append("{\n")
        uniqueId = self.UniqueID()
        lines.append("    int i%s;\n" % uniqueId)
        limit = sourceSequenceLimit(node, srcCVariable)
        lines.append("    for(i%s=0; i%s<%s; i%s++) {\n" % (uniqueId, uniqueId, limit, uniqueId))
        lines.extend(["        " + x for x in self.Map(
                     "%s.arr[i%s]" % (srcCVariable, uniqueId),
                     "%s.value[i%s]" % (destVar, uniqueId),
                     node._containedType,
                     leafTypeDict,
                     names)])
        lines.append("    }\n")
        lines.append("    %s.count = %s;\n" % (destVar, limit))
        lines.append("}\n")
        return lines

    def MapSetOf(self, srcCVariable, destVar, node, leafTypeDict, names):
        return self.MapSequenceOf(srcCVariable, destVar, node, leafTypeDict, names)  # pragma: nocover


class FromOSStoC(RecursiveMapper):
    def __init__(self):
        self.uniqueID = 0

    def UniqueID(self):
        self.uniqueID += 1
        return self.uniqueID

    def MapInteger(self, srcVar, dstCVariable, _, __, ___):
        return ["%s = %s;\n" % (dstCVariable, srcVar)]

    def MapReal(self, srcVar, dstCVariable, _, __, ___):
        return ["%s = %s;\n" % (dstCVariable, srcVar)]

    def MapBoolean(self, srcVar, dstCVariable, _, __, ___):
        return ["%s = (%s)?1:0;\n" % (dstCVariable, srcVar)]

    def MapOctetString(self, srcVar, dstCVariable, node, _, __):
        lines = []
        lines.append("{\n")
        lines.append("    int i;\n")
        lines.append("    for(i=0; i<%s.length; i++)\n" % srcVar)
        lines.append("        %s.arr[i] = %s.value[i];\n" % (dstCVariable, srcVar))
        lines.append("    while(i<%d) { %s.arr[i]=0; i++; }\n" % (node._range[-1], dstCVariable))
        if isSequenceVariable(node):
            lines.append("    %s.nCount = %s.length;\n" % (dstCVariable, srcVar))
        lines.append("}\n")
        return lines

    def MapEnumerated(self, srcVar, dstCVariable, _, __, ___):
        return ["%s = %s;\n" % (dstCVariable, srcVar)]

    def MapSequence(self, srcVar, dstCVariable, node, leafTypeDict, names):
        lines = []
        for child in node._members:
            lines.extend(
                self.Map(
                    srcVar + "." + self.CleanName(child[0]),
                    "%s.%s" % (dstCVariable, self.CleanName(child[0])),
                    child[1],
                    leafTypeDict,
                    names))
        return lines

    def MapSet(self, srcVar, dstCVariable, node, leafTypeDict, names):
        return self.MapSequence(srcVar, dstCVariable, node, leafTypeDict, names)  # pragma: nocover

    def MapChoice(self, srcVar, dstCVariable, node, leafTypeDict, names):
        lines = []
        childNo = 0
        for child in node._members:
            childNo += 1
            lines.append("%sif (%s.choice == OSS_%s_chosen) {\n" %
                         (self.maybeElse(childNo), srcVar, self.CleanName(child[0])))
            lines.extend(['    '+x for x in self.Map(
                         srcVar + ".u." + self.CleanName(child[0]),
                         "%s.u.%s" % (dstCVariable, self.CleanName(child[0])),
                         child[1],
                         leafTypeDict,
                         names)])
            lines.append("    %s.kind = %s;\n" % (dstCVariable, self.CleanName(child[2])))
            lines.append("}\n")
        return lines

    def MapSequenceOf(self, srcVar, dstCVariable, node, leafTypeDict, names):
        lines = []
        lines.append("{\n")
        uniqueId = self.UniqueID()
        lines.append("    int i%s;\n" % uniqueId)
        if isSequenceVariable(node):
            lines.append("    %s.nCount = %s.count;\n" % (dstCVariable, srcVar))
        lines.append("    for(i%s=0; i%s<%s; i%s++) {\n" %
                     (uniqueId, uniqueId, targetSequenceLimit(node, dstCVariable), uniqueId))
        lines.extend(["        " + x for x in self.Map(
                     srcVar + ".value[i%s]" % uniqueId,
                     "%s.arr[i%s]" % (dstCVariable, uniqueId),
                     node._containedType,
                     leafTypeDict,
                     names)])
        lines.append("    }\n")
        lines.append("}\n")
        return lines

    def MapSetOf(self, srcVar, dstCVariable, node, leafTypeDict, names):
        return self.MapSequenceOf(srcVar, dstCVariable, node, leafTypeDict, names)  # pragma: nocover


class C_GlueGenerator(ASynchronousToolGlueGenerator):
    def __init__(self):
        ASynchronousToolGlueGenerator.__init__(self)
        self.FromOSStoC = FromOSStoC()
        self.FromCtoOSS = FromCtoOSS()

    def Version(self):
        print("Code generator: " + "$Id: c_B_mapper.py 2390 2012-07-19 12:39:17Z ttsiodras $")  # pragma: no cover

    def HeadersOnStartup(self, unused_asnFile, unused_outputDir, unused_maybeFVname):
        if self.useOSS:
            self.C_HeaderFile.write("#include \"%s.oss.h\" // OSS generated\n\n" % self.asn_name)
            self.C_SourceFile.write("\nextern OssGlobal *g_world;\n\n")
        self.C_HeaderFile.write("#include \"%s.h\" // Space certified compiler generated\n\n" %
                                self.asn_name)
        self.C_HeaderFile.write("#include \"../../system_config.h\" // Choose ASN.1 Types to use\n\n")

    def Encoder(self, nodeTypename, node, leafTypeDict, names, encoding):
        if encoding.lower() not in self.supportedEncodings:
            panic(str(self.__class__) + ": in (%s), encoding can be one of %s (not '%s')" %  # pragma: no cover
                  (nodeTypename, self.supportedEncodings, encoding))  # pragma: no cover
        tmpSpName = "Encode_%s_%s" % \
            ({"uper": "UPER", "native": "NATIVE", "acn": "ACN"}[encoding.lower()],
             self.CleanNameAsToolWants(nodeTypename))

        needDefine = "#ifdef __NEED_%s_%s\n" % (
            self.CleanNameAsToolWants(nodeTypename),
            encoding.upper())
        self.C_HeaderFile.write(needDefine)
        self.C_HeaderFile.write(
            "size_t %s(void *pBuffer, size_t iMaxBufferSize, %sasn1Scc%s *pSrc);\n" %
            (tmpSpName, "" if encoding.lower()=="acn" else "const ",
             self.CleanNameAsToolWants(nodeTypename)))
        self.C_HeaderFile.write("#endif\n\n")
        self.C_SourceFile.write(needDefine)
        self.C_SourceFile.write(
            "size_t %s(void *pBuffer, size_t iMaxBufferSize, %sasn1Scc%s *pSrc)\n{\n" %
            (tmpSpName, "" if encoding.lower()=="acn" else "const ",
             self.CleanNameAsToolWants(nodeTypename)))

        if self.useOSS and encoding.lower() == "uper":
            self.C_SourceFile.write("    STATIC OSS_%s var_%s;\n\n" %
                                    (self.CleanNameAsToolWants(nodeTypename),
                                     self.CleanNameAsToolWants(nodeTypename)))

        if encoding.lower() in ["uper", "acn"]:
            if self.useOSS:
                self.C_SourceFile.write("    STATIC OssBuf strm;\n")
            else:
                self.C_SourceFile.write("    int errorCode;\n")
                self.C_SourceFile.write("    STATIC BitStream strm;\n\n")
                self.C_SourceFile.write("    BitStream_Init(&strm, pBuffer, iMaxBufferSize);\n")

        # Write the mapping code for the message if using OSS
        if self.useOSS and encoding.lower() == "uper":
            lines = self.FromCtoOSS.Map(
                "(*pSrc)",
                "var_" + self.CleanNameAsToolWants(nodeTypename),
                node,
                leafTypeDict,
                names)
            lines = ["    "+x for x in lines]
            self.C_SourceFile.write("".join(lines))

        if self.useOSS and encoding.lower() == "uper":
            # setup the OSS encoder
            self.C_SourceFile.write("\n    strm.value = NULL;\n")
            self.C_SourceFile.write("    strm.length = 0;\n")
            self.C_SourceFile.write("    if (ossEncode(g_world, OSS_%s_PDU, &var_%s, &strm) != 0) {\n" %
                                    (self.CleanNameAsToolWants(nodeTypename),
                                     self.CleanNameAsToolWants(nodeTypename)))
            self.C_SourceFile.write(
                '\tfprintf(stderr, "Could not encode %s (at %%s, %%d), errorMessage was %%s\\n", __FILE__, __LINE__, ossGetErrMsg(g_world));\n' % (nodeTypename))
            self.C_SourceFile.write("        return -1;\n")
            self.C_SourceFile.write("    } else {\n")
            self.C_SourceFile.write("        assert(strm.length <= iMaxBufferSize);\n")
            self.C_SourceFile.write("        memcpy(pBuffer, strm.value, strm.length);\n")
            self.C_SourceFile.write("        ossFreeBuf(g_world, strm.value);\n")
            self.C_SourceFile.write("        return strm.length;\n")
            self.C_SourceFile.write("    }\n")
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")
        elif encoding.lower() in ["uper", "acn"]:
            self.C_SourceFile.write("    if (asn1Scc%s_%sEncode(pSrc, &strm, &errorCode, TRUE) == FALSE) {\n" %
                                    (self.CleanNameAsToolWants(nodeTypename),
                                     ("ACN_" if encoding.lower()=="acn" else "")))
            self.C_SourceFile.write(
                '\tfprintf(stderr, "Could not encode %s (at %%s, %%d), errorCode was %%d\\n", __FILE__, __LINE__, errorCode);\n' % (nodeTypename))
            self.C_SourceFile.write("        return -1;\n")
            self.C_SourceFile.write("    } else {\n")
            self.C_SourceFile.write("        return BitStream_GetLength(&strm);\n")
            self.C_SourceFile.write("    }\n")
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")
        elif encoding.lower() == "native":
            self.C_SourceFile.write("    memcpy(pBuffer, pSrc, sizeof(asn1Scc%s) );\n" %
                                    (self.CleanNameAsToolWants(nodeTypename)))
            self.C_SourceFile.write("    return sizeof(asn1Scc%s);\n" %
                                    self.CleanNameAsToolWants(nodeTypename))
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")

    def Decoder(self, nodeTypename, node, leafTypeDict, names, encoding):
        if encoding.lower() not in self.supportedEncodings:
            panic(str(self.__class__) + ": in (%s), encoding can be one of %s (not '%s')" %  # pragma: no cover
                  (nodeTypename, self.supportedEncodings, encoding))  # pragma: no cover

        tmpSpName = "Decode_%s_%s" % \
            ({"uper": "UPER", "native": "NATIVE", "acn": "ACN"}[encoding.lower()],
             self.CleanNameAsToolWants(nodeTypename))

        needDefine = "#ifdef __NEED_%s_%s\n" % (
            self.CleanNameAsToolWants(nodeTypename),
            encoding.upper())
        self.C_HeaderFile.write(needDefine)
        self.C_HeaderFile.write(
            "int %s(asn1Scc%s *pDst, void *pBuffer, size_t iBufferSize);\n" %
            (tmpSpName, self.CleanNameAsToolWants(nodeTypename)))
        self.C_HeaderFile.write("#endif\n\n")
        self.C_SourceFile.write(needDefine)
        self.C_SourceFile.write(
            "int %s(asn1Scc%s *pDst, void *pBuffer, size_t iBufferSize)\n{\n" %
            (tmpSpName, self.CleanNameAsToolWants(nodeTypename)))

        if self.useOSS and encoding.lower() == "uper":
            self.C_SourceFile.write("    int pdutype = OSS_%s_PDU;\n" %
                                    self.CleanNameAsToolWants(nodeTypename))
            self.C_SourceFile.write("    STATIC OssBuf strm;\n\n")
            self.C_SourceFile.write("    OSS_%s *pVar_%s = NULL;\n\n" %
                                    (self.CleanNameAsToolWants(nodeTypename),
                                     self.CleanNameAsToolWants(nodeTypename)))
            self.C_SourceFile.write("    strm.value = pBuffer;\n")
            self.C_SourceFile.write("    strm.length = iBufferSize;\n")
            self.C_SourceFile.write("    if (0 == ossDecode(g_world, &pdutype, &strm, (void**)&pVar_%s)) {\n" %
                                    self.CleanNameAsToolWants(nodeTypename))
            self.C_SourceFile.write("        /* Decoding succeeded */\n")
        else:
            if encoding.lower() in ["uper", "acn"]:
                self.C_SourceFile.write("    int errorCode;\n\n")
                self.C_SourceFile.write("    STATIC BitStream strm;\n\n")
                self.C_SourceFile.write("    BitStream_AttachBuffer(&strm, pBuffer, iBufferSize);\n\n")
                self.C_SourceFile.write("    if (asn1Scc%s_%sDecode(pDst, &strm, &errorCode)) {\n" %
                                        (self.CleanNameAsToolWants(nodeTypename),
                                         "ACN_" if encoding.lower()=="acn" else ""))
                self.C_SourceFile.write("        /* Decoding succeeded */\n")
            elif encoding.lower() == "native":
                self.C_SourceFile.write("    *pDst = *(asn1Scc%s *) pBuffer;\n    {\n" %
                                        (self.CleanNameAsToolWants(nodeTypename)))

        if self.useOSS and encoding.lower() == "uper":
            lines = self.FromOSStoC.Map(
                "(*pVar_" + self.CleanNameAsToolWants(nodeTypename) + ")",
                "(*pDst)",
                node,
                leafTypeDict,
                names)
            lines = ["        "+x for x in lines]
            self.C_SourceFile.write("".join(lines))

        if self.useOSS and encoding.lower() == "uper":
            self.C_SourceFile.write("        ossFreeBuf(g_world, pVar_%s);\n" %
                                    self.CleanNameAsToolWants(nodeTypename))
            self.C_SourceFile.write("        return 0;\n")
            self.C_SourceFile.write("    } else {\n")
            self.C_SourceFile.write(
                '\tfprintf(stderr, "Could not decode %s (at %%s, %%d), error message was %%s\\n", __FILE__, __LINE__, ossGetErrMsg(g_world));\n' % (nodeTypename))
            self.C_SourceFile.write("        return -1;\n")
            self.C_SourceFile.write("    }\n")
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")
        elif encoding.lower() in ["uper", "acn"]:
            self.C_SourceFile.write("        return 0;\n")
            self.C_SourceFile.write("    } else {\n")
            self.C_SourceFile.write(
                '\tfprintf(stderr, "Could not decode %s (at %%s, %%d), error code was %%d\\n", __FILE__, __LINE__, errorCode);\n' % (nodeTypename))
            self.C_SourceFile.write("        return -1;\n")
            self.C_SourceFile.write("    }\n")
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")
        else:
            self.C_SourceFile.write("        return 0;\n")
            self.C_SourceFile.write("    }\n")
            self.C_SourceFile.write("}\n")
            self.C_SourceFile.write("#endif\n\n")


def OnStartup(modelingLanguage, asnFile, outputDir, maybeFVname, useOSS):
    global cBackend
    cBackend = C_GlueGenerator()
    cBackend.OnStartup(modelingLanguage, asnFile, outputDir, maybeFVname, useOSS)


def OnBasic(nodeTypename, node, leafTypeDict, names):
    cBackend.OnBasic(nodeTypename, node, leafTypeDict, names)


def OnSequence(nodeTypename, node, leafTypeDict, names):
    cBackend.OnSequence(nodeTypename, node, leafTypeDict, names)


def OnSet(nodeTypename, node, leafTypeDict, names):
    cBackend.OnSet(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnEnumerated(nodeTypename, node, leafTypeDict, names):
    cBackend.OnEnumerated(nodeTypename, node, leafTypeDict, names)


def OnSequenceOf(nodeTypename, node, leafTypeDict, names):
    cBackend.OnSequenceOf(nodeTypename, node, leafTypeDict, names)


def OnSetOf(nodeTypename, node, leafTypeDict, names):
    cBackend.OnSetOf(nodeTypename, node, leafTypeDict, names)  # pragma: nocover


def OnChoice(nodeTypename, node, leafTypeDict, names):
    cBackend.OnChoice(nodeTypename, node, leafTypeDict, names)


def OnShutdown(modelingLanguage, asnFile, maybeFVname):
    cBackend.OnShutdown(modelingLanguage, asnFile, maybeFVname)
