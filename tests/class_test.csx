


function fact(_n) 
{

    if (_n == 1) return 1;

    return _n * fact(_n - 1);
}

print: fact(5);

var x = false;

if (!true || x) print: "true";

var xx = {
    a: 0, 
    b: 2, 
    c: function(a, b) 
    { return a + b; } 
};

console::warn( xx::c(69, 420) );


class Dog 
{

    val x = 2;

    function initialize(_name, _age) 
    {
        let name = _name, age = _age;
        print: "AwF!", "my name is", name, (typeof this);

        return false;
    }

    function eat(_food)
    {

    }

}



{
    let ManualClass = ({

        qualname  : "ManualClass",

        initialize: function() {

            print: "my manual class", this;
        }

    });

    print: new ManualClass();
}


console::warn("Hello!!!");

var a = CSInteger::tryParse(console::readLine("number 1:>> "));
var b = CSInteger::tryParse(console::readLine("number 2:>> "));
print: "sum:", a + b;