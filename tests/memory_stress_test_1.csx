



class State {
    val a = 0;
    val b = 0;
    function initialize() {
        
    }
}

print: "old State:", State;

while (State::b < 10000) 
{
    State::b += 1;
    print: State::b;
}

print: "State->b =", State::b;
print: "new State:", State;


State::a = State;
print: "contains self refrence", State;


var list_of_ambot = [0,1,2,3];
print: "old list:", list_of_ambot;

do {

    list_of_ambot[0] += 1;

}while(list_of_ambot[0] < 10500)

print: "new list:", list_of_ambot;



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

print: lang;
print: list_of_ambot;


switch(lang.name) 
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

print: State;
print: list_of_ambot;
print: lang.toString();