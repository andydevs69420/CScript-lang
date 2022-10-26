/*
 *   Copyright (c) 2022 
 *   All rights reserved.
 */

#include <stdbool.h>

#ifndef OBJECT__H
#define OBJECT__H

typedef enum _datatypes {
    a = 2,
    b = 3,
} ObjectType ;


#ifdef __cplusplus
extern "C" {
#endif

typedef struct _object CSObject;
typedef struct _object {
    bool ispntr;
    ObjectType dtpe;

    char* (*toString)(CSObject*);
    
} CSObject;


#ifdef __cplusplus
}
#endif


#endif

