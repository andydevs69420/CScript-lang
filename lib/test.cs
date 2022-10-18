
var state = {
    count: 0,
    shake: 0
};


while (state->count < 1000) {
    print: "state::count =", state->count;
    state->count += 1;
}


print: state, state->count;

state->shake = "FOOOC!";

print: state, state->count;

var array = [1,2,3,4,5] ;
print: array;


function println() 
{
    var x = 0;
    while (x < 10)
    {
        print: "func: x =", x;
        x += 1;
    }
}

print: println();

var v = {abc: println};
v->abc();


