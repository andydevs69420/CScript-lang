

class Dog {
    name: null,
    age: 0,
    
    birthday: (function(this) {return this->age += 1;}),
    eat: (function(this, _food) { print: this->name, "is eating a", _food, "!"; return !true;})
}

var x = 0;
while (x < 1000)x += 1;


var yy = new Dog();

print: yy->name == Dog->name;


print: 2 + 2;

print: { a : "2" };
