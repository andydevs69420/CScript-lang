/*
 *   Copyright (c) 2022 
 *   All rights reserved.
 */

#include <stdio.h>
#include <stdlib.h>
#include "object.h"


static
char *toString(CSObject *_self) {
    char *BUFFER = malloc(sizeof(char) * 4096);
    sprintf(BUFFER, "Datatype: %d | IsPointer: %d", _self->dtpe, _self->ispntr);
    return BUFFER;
}

int main() {

    CSObject *_obj = malloc(sizeof(CSObject));
        _obj->ispntr = false;
        _obj->dtpe = a;
        _obj->toString = toString;

    printf("Hello World -> %s\n", _obj->toString(_obj));
    return 0;
}