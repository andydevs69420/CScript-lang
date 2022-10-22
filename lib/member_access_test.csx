

var x = {a: 100, b: 50};

x->a = x->b + x->a;
x->b = x->a - x->b;
x->a = x->a - x->b;


print: x, x->a, x->b;


try {
    let h = "Hola!";
    print: !h;
}except(err) {
    print: "printed", err->name;
}finally {
    print: "Donez!";
}


