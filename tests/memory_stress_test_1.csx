



var state = {a: 0, b: 1};
print: "old state:", state;

while (state["b"] < 10000) 
{
    state->b += 1;
}

print: "state->b =", state["b"];
print: "new state:", state;


state->a = state;
print: "contains self refrence", state;


var list_of_ambot = [0,1,2,3];
print: "old list:", list_of_ambot;

do {

    list_of_ambot[0] += 1;

}while(list_of_ambot[0] < 10500)

print: "new list:", list_of_ambot;

class Language {
    name: null,
    constructor: (func(this, _name){
        this->name = _name;
    }),
    getName: (func(this){
        return this->name;
    }),
    toString: (func(this){
        return "Programming language: " + this->name;
    })
}


var lang;

while (list_of_ambot[1] < 100000)
{
    if (list_of_ambot[1] < 15000)
        lang = new Language("CScript-lang");
    else
        lang = new Language("Java");
    
    list_of_ambot[1] += 1;
}

list_of_ambot[2] = lang;

print: lang->toString();
print: list_of_ambot;


switch(lang->name) 
{
    case 0, 1, 2, "Java":
        print: "list_of_ambot at index 1 is above 15000";
    else:
        print: "list_of_ambot at index 1 is below 15000";
}

{
    let localVar = 2 ^^ 32;
        print: localVar;
}

print: state;
print: list_of_ambot;
print: lang->toString();