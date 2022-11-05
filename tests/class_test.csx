


class Dog 
{
    val name = "Default", age = 0;

    func Dog(_name, _age)
    {
        this->name = _name;
        this->age  = _age;
    }

    func eats(_food)
    {
       print: this->name, this->Dog->name, "is eating a", _food, "!";
    }

    func bark()
    { print: "AwwFF!!!"; }
}

var x = new Dog("Snoop", 69420);
    x->eats("diaper");
    x->bark();

print: x, 0x1ff;
print: "x1ff =", (((1 * 16) ^^ 2) + (15 * 16) + 15 );



class Person
{
    val name, age, pet;

    func Person(_pname, _age) 
    { 
        this->name = _pname;
        this->age  = _age;
        this->pet  = new Dog("Snoop", 1);
    }

    func getPet(){ return this->pet; }
}

var person = new Person("Andy", 23);
    print: person;
    person->name = "Philipp Andrew";
    print: person->name;
    print: person->getPet()->eats("diaper");
    print: person;


class X 
{
    val v = 2;
    val w = v;
}

print: new X();


var xx = false;
print: xx, null;