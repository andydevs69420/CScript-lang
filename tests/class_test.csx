


function add() {

    print: "Hello World!", 2;

    let x = 2;
    {
        let x = 20;
        let y = 25;
        print: "outer", x;
        {
            print: "inner", x;
            print: "inner", y;
        }
    }

    print: "OuterOuter", x;

    return 69420;
}

{
    let x = 50;
    print: x;

    while (x > 10) {
        print: "x =", x;
        x -= 1;
    }
    print: "x =", x;
}

var x = 100000;
add();
print:x;
x = 100;
print: x;

class Dog {
    val x = 2;
    function initialize() {
        print: "New!!";
        print: this;
    }

    function toString() {
        return "[Instance]";
    }
}





print: new Dog();
