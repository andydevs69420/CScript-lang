


class Dog 
{
    val xxx = 002;
    val cat = xxx;

    function init()
    { return new Dog(); }

    function initialize()
    { this.xxx = 100; }
}


var xx = Dog::init();

print: xx;

Dog::add = (function(a, b) {
    print: "extended:", this;
    return a + b;
});

print: Dog;
print: xx.add(10, 3);

while (0) {

    let x, y, z, cell = CSInteger::tryParse(console::readLine("Input:> "));

    for (x = 0; x < cell; x+=1) 
    {

        for (y = 0; y < cell - x; y+=1) 
        console::write(" ");

        for (z = 1; z < ((x + 1) * 2); z+=1) 
        console::write("*");

        print: "";
    }

}


var arr = [1,2,3];

print: arr;

try 
{
    throw xx;
}except(err)
{
    print: err;
}

4[0];

