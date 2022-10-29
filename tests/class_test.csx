


import [MODULE, add, State] from "import1_test.csx";
State->flags += 100;
import [] from "if_test.csx";

class Dog
{
    name: null,
    age: 0,
    constructor: (func(this, _name) {
        this->name = _name;
    }),
    birthday: (func(this) {
        return this->age += 1;
    }),
    eat: (func(this, _food) { 
        print: this->name, "is eating a", _food, "!";
        print: "Yummy!!!!!!";
        return !true;
    })
}


{
    let xx = 0;
    while (xx < 1000) xx += 1;
}

var xxx = (2 != 2)?1:100;
var yyy = new Dog("Brownie");

print: MODULE, add(10, 20), State->flags;
    State->flags += 100;
print: MODULE, add(10, 20), State->flags;




func fact(_n)
{
    if  (_n == 1) return 1;
    return _n * fact(_n - 1);
}

print: ("\n");
var n = 10;
print: "fact of", n, "is", fact(n); 
print: ("\n");

{
    let v = 2 * n;
    print: v;
}

{
    let iter= 0;
    while (iter < 2000)
    { iter += 1; }

    print: "iter:", iter;

    let add = (func(a, b) {

        return a + b;
    });

    print: add(0, 1);
}


print: new Dog("Snoop")->eat("diaper");
assert 2 != 2, "2 is equal to 2";
