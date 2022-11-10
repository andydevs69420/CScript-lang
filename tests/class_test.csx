

class Food 
{
    val qualname = "FOOOTA";

    function initialize(_dog, dog_inst, _name) 
    {
        print: _dog, typeof dog_inst, "is eating", _name, "...";

    }

    function __toString__()
    { return "adad"; }
}

class Dog
{
    function initialize(_dog_name) 
    {
        let food = new Food(_dog_name, this, "diaper");
        print: "AwF!!!", food;
    }

    function eat(_food) 
    {
        print: _food;
        print: this;
    }
}

print: CSInteger;

var x = new Dog("Snoop");


console::warn(x.__proto__);
