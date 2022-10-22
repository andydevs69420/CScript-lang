

var x = {a: 100, b: 50};

x->a = x->b + x->a;
x->b = x->a - x->b;
x->a = x->a - x->b;


print: x, x->a, x->b;


var c = 0;

while (c < 1000) {
    print: "c =", c;
    c += 1;
}

var vvvv = [1,2,3, x->a];

print: vvvv->length + 2;


function add(a, b, c) {

}


print: add->parameters[2];
