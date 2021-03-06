#ifndef _INC_DATATYPESSIMULINK_H
#define _INC_DATATYPESSIMULINK_H
/*
Code automatically generated by asn1cc tool
*/

#include "asn1crt.h"

#ifdef  __cplusplus
extern "C" {
#endif

/*
Original definition by Alain
T-POS ::= BOOLEAN
*/
typedef struct {
    struct {
            long nCount;
            flag  arr[10];
        } blArray;
} asn1SccAType;

#define asn1SccAType_REQUIRED_BYTES_FOR_ENCODING		2

#define ERR_asn1SccAType_blArray		1000 /* (SIZE (10)) */

void asn1SccAType_Initialize(asn1SccAType* pVal);
flag asn1SccAType_IsConstraintValid(const asn1SccAType* val, int* pErrCode);
flag asn1SccAType_Encode(const asn1SccAType* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccAType_Decode(asn1SccAType* pVal, BitStream* pBitStrm, int* pErrCode);


typedef enum {
    red = 0,
    green = 1,
    blue = 2
} asn1SccTypeEnumerated;

#define asn1SccTypeEnumerated_REQUIRED_BYTES_FOR_ENCODING		1


void asn1SccTypeEnumerated_Initialize(asn1SccTypeEnumerated* pVal);
flag asn1SccTypeEnumerated_IsConstraintValid(const asn1SccTypeEnumerated* val, int* pErrCode);
flag asn1SccTypeEnumerated_Encode(const asn1SccTypeEnumerated* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccTypeEnumerated_Decode(asn1SccTypeEnumerated* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        asn1SccSint  arr[6];
    } asn1SccT_ARR;

#define asn1SccT_ARR_REQUIRED_BYTES_FOR_ENCODING		12

#define ERR_asn1SccT_ARR		1001 /* (SIZE (5..6)) */
#define ERR_asn1SccT_ARR_elem		1002 /* (0..32764) */

void asn1SccT_ARR_Initialize(asn1SccT_ARR* pVal);
flag asn1SccT_ARR_IsConstraintValid(const asn1SccT_ARR* val, int* pErrCode);
flag asn1SccT_ARR_Encode(const asn1SccT_ARR* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_ARR_Decode(asn1SccT_ARR* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        double arr[6];
    } asn1SccT_ARR2;

#define asn1SccT_ARR2_REQUIRED_BYTES_FOR_ENCODING		55

#define ERR_asn1SccT_ARR2		1003 /* (SIZE (5..6)) */
#define ERR_asn1SccT_ARR2_elem		1004 /* (0.1..4.2) */

void asn1SccT_ARR2_Initialize(asn1SccT_ARR2* pVal);
flag asn1SccT_ARR2_IsConstraintValid(const asn1SccT_ARR2* val, int* pErrCode);
flag asn1SccT_ARR2_Encode(const asn1SccT_ARR2* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_ARR2_Decode(asn1SccT_ARR2* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        struct {
            long nCount;
            double arr[7];
        } arr[6];
    } asn1SccT_ARR3;

#define asn1SccT_ARR3_REQUIRED_BYTES_FOR_ENCODING		379

#define ERR_asn1SccT_ARR3		1005 /* (SIZE (5..6)) */
#define ERR_asn1SccT_ARR3_elem		1006 /* (SIZE (7)) */
#define ERR_asn1SccT_ARR3_elem_elem		1007 /* (0.1..4.2) */

void asn1SccT_ARR3_Initialize(asn1SccT_ARR3* pVal);
flag asn1SccT_ARR3_IsConstraintValid(const asn1SccT_ARR3* val, int* pErrCode);
flag asn1SccT_ARR3_Encode(const asn1SccT_ARR3* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_ARR3_Decode(asn1SccT_ARR3* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        struct {
            long nCount;
            double arr[7];
        } arr[6];
    } asn1SccT_ARR4;

#define asn1SccT_ARR4_REQUIRED_BYTES_FOR_ENCODING		379

#define ERR_asn1SccT_ARR4		1008 /* (SIZE (5..6)) */
#define ERR_asn1SccT_ARR4_elem		1009 /* (SIZE (7)) */
#define ERR_asn1SccT_ARR4_elem_elem		1010 /* (0.1..4.3) */

void asn1SccT_ARR4_Initialize(asn1SccT_ARR4* pVal);
flag asn1SccT_ARR4_IsConstraintValid(const asn1SccT_ARR4* val, int* pErrCode);
flag asn1SccT_ARR4_Encode(const asn1SccT_ARR4* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_ARR4_Decode(asn1SccT_ARR4* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
    asn1SccSint  data1;
    double data2;
    asn1SccSint  data3;
    asn1SccSint  data4;
} asn1SccT_SET;

#define asn1SccT_SET_REQUIRED_BYTES_FOR_ENCODING		16

#define ERR_asn1SccT_SET_data1		1011 /* (0..131071) */
#define ERR_asn1SccT_SET_data2		1012 /* (-100..10) */
#define ERR_asn1SccT_SET_data3		1013 /* (-1024..1024) */
#define ERR_asn1SccT_SET_data4		1014 /* (-1310720..131071) */

void asn1SccT_SET_Initialize(asn1SccT_SET* pVal);
flag asn1SccT_SET_IsConstraintValid(const asn1SccT_SET* val, int* pErrCode);
flag asn1SccT_SET_Encode(const asn1SccT_SET* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_SET_Decode(asn1SccT_SET* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        asn1SccSint  arr[6];
    } asn1SccT_SETOF;

#define asn1SccT_SETOF_REQUIRED_BYTES_FOR_ENCODING		3

#define ERR_asn1SccT_SETOF		1015 /* (SIZE (5..6)) */
#define ERR_asn1SccT_SETOF_elem		1016 /* (0..4) */

void asn1SccT_SETOF_Initialize(asn1SccT_SETOF* pVal);
flag asn1SccT_SETOF_IsConstraintValid(const asn1SccT_SETOF* val, int* pErrCode);
flag asn1SccT_SETOF_Encode(const asn1SccT_SETOF* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_SETOF_Decode(asn1SccT_SETOF* pVal, BitStream* pBitStrm, int* pErrCode);


typedef flag  asn1SccT_BOOL;

#define asn1SccT_BOOL_REQUIRED_BYTES_FOR_ENCODING		1


void asn1SccT_BOOL_Initialize(asn1SccT_BOOL* pVal);
flag asn1SccT_BOOL_IsConstraintValid(const asn1SccT_BOOL* val, int* pErrCode);
flag asn1SccT_BOOL_Encode(const asn1SccT_BOOL* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_BOOL_Decode(asn1SccT_BOOL* pVal, BitStream* pBitStrm, int* pErrCode);


typedef asn1SccSint  asn1SccT_INT;

#define asn1SccT_INT_REQUIRED_BYTES_FOR_ENCODING		1

#define ERR_asn1SccT_INT		1017 /* (0..50) */

void asn1SccT_INT_Initialize(asn1SccT_INT* pVal);
flag asn1SccT_INT_IsConstraintValid(const asn1SccT_INT* val, int* pErrCode);
flag asn1SccT_INT_Encode(const asn1SccT_INT* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_INT_Decode(asn1SccT_INT* pVal, BitStream* pBitStrm, int* pErrCode);


typedef double asn1SccT_REAL;

#define asn1SccT_REAL_REQUIRED_BYTES_FOR_ENCODING		9

#define ERR_asn1SccT_REAL		1018 /* (-3.14..3.14) */

void asn1SccT_REAL_Initialize(asn1SccT_REAL* pVal);
flag asn1SccT_REAL_IsConstraintValid(const asn1SccT_REAL* val, int* pErrCode);
flag asn1SccT_REAL_Encode(const asn1SccT_REAL* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_REAL_Decode(asn1SccT_REAL* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        byte arr[15];
    } asn1SccT_STRING;

#define asn1SccT_STRING_REQUIRED_BYTES_FOR_ENCODING		16

#define ERR_asn1SccT_STRING		1019 /* (SIZE (10..15)) */

void asn1SccT_STRING_Initialize(asn1SccT_STRING* pVal);
flag asn1SccT_STRING_IsConstraintValid(const asn1SccT_STRING* val, int* pErrCode);
flag asn1SccT_STRING_Encode(const asn1SccT_STRING* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_STRING_Decode(asn1SccT_STRING* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
        long nCount;
        byte arr[15];
    } asn1SccT_FIXEDSTRING;

#define asn1SccT_FIXEDSTRING_REQUIRED_BYTES_FOR_ENCODING		15

#define ERR_asn1SccT_FIXEDSTRING		1020 /* (SIZE (15)) */

void asn1SccT_FIXEDSTRING_Initialize(asn1SccT_FIXEDSTRING* pVal);
flag asn1SccT_FIXEDSTRING_IsConstraintValid(const asn1SccT_FIXEDSTRING* val, int* pErrCode);
flag asn1SccT_FIXEDSTRING_Encode(const asn1SccT_FIXEDSTRING* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_FIXEDSTRING_Decode(asn1SccT_FIXEDSTRING* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
    asn1SccSint  intVal;
    asn1SccSint  int2Val;
    struct {
            long nCount;
            asn1SccSint  arr[10];
        } intArray;
    struct {
            long nCount;
            double arr[10];
        } realArray;
    struct {
            long nCount;
            struct {
                long nCount;
                byte arr[10];
            } arr[10];
        } octStrArray;
    struct {
            long nCount;
            asn1SccT_BOOL arr[10];
        } boolArray;
    struct {
            long nCount;
            asn1SccTypeEnumerated arr[10];
        } enumArray;
    asn1SccTypeEnumerated enumValue;
    enum {
        truism = 0,
        falsism = 1
    } enumValue2;
    struct {
            long nCount;
            byte arr[40];
        } label;
    asn1SccT_BOOL bAlpha;
    flag  bBeta;
    asn1SccT_STRING sString;
    asn1SccT_ARR arr;
    asn1SccT_ARR2 arr2;
} asn1SccTypeNested;

#define asn1SccTypeNested_REQUIRED_BYTES_FOR_ENCODING		325

#define ERR_asn1SccTypeNested_intVal		1021 /* (0..10) */
#define ERR_asn1SccTypeNested_int2Val		1022 /* (-10..10) */
#define ERR_asn1SccTypeNested_intArray		1023 /* (SIZE (10)) */
#define ERR_asn1SccTypeNested_intArray_elem		1024 /* (0..3) */
#define ERR_asn1SccTypeNested_realArray		1025 /* (SIZE (10)) */
#define ERR_asn1SccTypeNested_realArray_elem		1026 /* (0.1..3.14) */
#define ERR_asn1SccTypeNested_octStrArray		1027 /* (SIZE (10)) */
#define ERR_asn1SccTypeNested_octStrArray_elem		1028 /* (SIZE (1..10)) */
#define ERR_asn1SccTypeNested_boolArray		1029 /* (SIZE (10)) */
#define ERR_asn1SccTypeNested_enumArray		1030 /* (SIZE (10)) */
#define ERR_asn1SccTypeNested_label		1031 /* (SIZE (10..40)) */
#define ERR_asn1SccTypeNested_sString		1032 /* (SIZE (10..15)) */
#define ERR_asn1SccTypeNested_arr		1033 /* (SIZE (5..6)) */
#define ERR_asn1SccTypeNested_arr2		1034 /* (SIZE (5..6)) */

void asn1SccTypeNested_Initialize(asn1SccTypeNested* pVal);
flag asn1SccTypeNested_IsConstraintValid(const asn1SccTypeNested* val, int* pErrCode);
flag asn1SccTypeNested_Encode(const asn1SccTypeNested* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccTypeNested_Decode(asn1SccTypeNested* pVal, BitStream* pBitStrm, int* pErrCode);


/* A more realistic definition */
typedef struct {
    enum {
        T_POS_NONE,	/* No components present */
        longitude_PRESENT,
        latitude_PRESENT,
        height_PRESENT,
        subTypeArray_PRESENT,
        label_PRESENT,
        intArray_PRESENT,
        myIntSet_PRESENT,
        myIntSetOf_PRESENT
    } kind;
    union {
        double longitude;
        double latitude;
        double height;
        struct {
            long nCount;
            asn1SccTypeNested arr[15];
        } subTypeArray;
        struct {
            long nCount;
            byte arr[50];
        } label;
        asn1SccT_ARR intArray;
        asn1SccT_SET myIntSet;
        asn1SccT_SETOF myIntSetOf;
    } u;
} asn1SccT_POS;

#define asn1SccT_POS_REQUIRED_BYTES_FOR_ENCODING		4869

#define ERR_asn1SccT_POS		1035 /*  */
#define ERR_asn1SccT_POS_longitude		1036 /* (-180..180) */
#define ERR_asn1SccT_POS_latitude		1037 /* (-90..90) */
#define ERR_asn1SccT_POS_height		1038 /* (30000..45000) */
#define ERR_asn1SccT_POS_subTypeArray		1039 /* (SIZE (10..15)) */
#define ERR_asn1SccT_POS_label		1040 /* (SIZE (50)) */
#define ERR_asn1SccT_POS_intArray		1041 /* (SIZE (5..6)) */
#define ERR_asn1SccT_POS_myIntSetOf		1042 /* (SIZE (5..6)) */

void asn1SccT_POS_Initialize(asn1SccT_POS* pVal);
flag asn1SccT_POS_IsConstraintValid(const asn1SccT_POS* val, int* pErrCode);
flag asn1SccT_POS_Encode(const asn1SccT_POS* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_POS_Decode(asn1SccT_POS* pVal, BitStream* pBitStrm, int* pErrCode);


typedef struct {
    double longitude;
    double latitude;
    double height;
    struct {
            long nCount;
            asn1SccTypeNested arr[15];
        } subTypeArray;
    struct {
            long nCount;
            byte arr[50];
        } label;
    asn1SccT_ARR intArray;
    asn1SccT_SET myIntSet;
    asn1SccT_SETOF myIntSetOf;
} asn1SccT_POS_SET;

#define asn1SccT_POS_SET_REQUIRED_BYTES_FOR_ENCODING		4975

#define ERR_asn1SccT_POS_SET_longitude		1043 /* (-180..180) */
#define ERR_asn1SccT_POS_SET_latitude		1044 /* (-90..90) */
#define ERR_asn1SccT_POS_SET_height		1045 /* (30000..45000) */
#define ERR_asn1SccT_POS_SET_subTypeArray		1046 /* (SIZE (10..15)) */
#define ERR_asn1SccT_POS_SET_label		1047 /* (SIZE (20..50)) */
#define ERR_asn1SccT_POS_SET_intArray		1048 /* (SIZE (5..6)) */
#define ERR_asn1SccT_POS_SET_myIntSetOf		1049 /* (SIZE (5..6)) */

void asn1SccT_POS_SET_Initialize(asn1SccT_POS_SET* pVal);
flag asn1SccT_POS_SET_IsConstraintValid(const asn1SccT_POS_SET* val, int* pErrCode);
flag asn1SccT_POS_SET_Encode(const asn1SccT_POS_SET* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_POS_SET_Decode(asn1SccT_POS_SET* pVal, BitStream* pBitStrm, int* pErrCode);


typedef asn1SccT_POS asn1SccT_META;

#define asn1SccT_META_REQUIRED_BYTES_FOR_ENCODING		4869


void asn1SccT_META_Initialize(asn1SccT_META* pVal);
flag asn1SccT_META_IsConstraintValid(const asn1SccT_META* val, int* pErrCode);
flag asn1SccT_META_Encode(const asn1SccT_META* val, BitStream* pBitStrm, int* pErrCode, flag bCheckConstraints);
flag asn1SccT_META_Decode(asn1SccT_META* pVal, BitStream* pBitStrm, int* pErrCode);


#ifdef  __cplusplus
}
#define	ENUM_red	red
#define	ENUM_green	green
#define	ENUM_blue	blue
#define	ENUM_truism	asn1SccTypeNested::truism
#define	ENUM_falsism	asn1SccTypeNested::falsism
#define	CHOICE_longitude_PRESENT	asn1SccT_POS::longitude_PRESENT
#define	CHOICE_latitude_PRESENT	asn1SccT_POS::latitude_PRESENT
#define	CHOICE_height_PRESENT	asn1SccT_POS::height_PRESENT
#define	CHOICE_subTypeArray_PRESENT	asn1SccT_POS::subTypeArray_PRESENT
#define	CHOICE_label_PRESENT	asn1SccT_POS::label_PRESENT
#define	CHOICE_intArray_PRESENT	asn1SccT_POS::intArray_PRESENT
#define	CHOICE_myIntSet_PRESENT	asn1SccT_POS::myIntSet_PRESENT
#define	CHOICE_myIntSetOf_PRESENT	asn1SccT_POS::myIntSetOf_PRESENT
#endif

#endif
