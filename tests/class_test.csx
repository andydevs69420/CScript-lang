
import [MODULE, add, State] from "/home/andydevs69420/Documents/CScript/tests/import1_test.csx";

State->flags += 100;


class Dog 
{
    name: null,
    age : 0   ,
    birthday: (function(this) {return this->age += 1;}),
    eat     : (function(this, _food) { print: this->name, "is eating a", _food, "!"; return !true;})
}


{
    let x = 0;
    while (x < 1000) x += 1;
}

var xxx = (2 != 2)?1:100;
var yyy = new Dog();

print: MODULE, add(10, 20), State->flags;
    State->flags += 100;
print: MODULE, add(10, 20), State->flags;


