
var x = {a: 100, b: 50};
print: "x not swaped:", x;

x->a = x->b + x->a;
x->b = x->a - x->b;
x->a = x->a - x->b;

print: "x swaped:", x;
