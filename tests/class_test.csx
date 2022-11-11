

class Dog 
{
    val x = 2;
    val y = 2;

    function init()
    { return new Dog(); }

    function initialize() 
    {
        this.name = "Andy";
        this.age  = 24;
        let x = 100;
        {
            let x = 2;
            print: x;
        }
        print: x;
    }
}

{
    let x = 500;
    print: x;
}
print: Dog::init();

console::warn("Meow!!!");
throw "Hello fooocin world!";
