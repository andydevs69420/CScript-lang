
import [MODULE, add, State] from "import1_test.csx";

State->flags += 100;

import [] from "if_test.csx";

class Dog 
{
    name: null,
    age: 0 ,
    birthday: (func(this) {
        return this->age += 1;
    }),
    eat: (func(this, _food) { 
        print: this->name, "is eating a", _food, "!"; 
        return !true;
    })
}


{
    let xx = 0;
    while (xx < 1000) xx += 1;
}

var xxx = (2 != 2)?1:100;
var yyy = new Dog();

print: MODULE, add(10, 20), State->flags;
    State->flags += 100;
print: MODULE, add(10, 20), State->flags;


