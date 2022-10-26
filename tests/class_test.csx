

class Dog {
    name: "Brownie",
    age: 2,
    birthday: (function(this) {return this->age += 1;})
}

var dog = new new Dog;
    dog->birthday();
    var newAge = dog->birthday();
    newAge += 1;
print: dog->name, dog->age, newAge;



print: dog->birthday->typeString(), Dog->birthday->typeString();

