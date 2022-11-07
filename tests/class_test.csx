



class MyInt 
{
    func MyInt(_int) 
    { this->number = _int; }

    func __add__(_rhs) 
    { return this->number + _rhs; }

    func __toString__()
    { return "MyInt: " + this->number; }
}


var 比克 = new MyInt(500);
print: 比克 + (500 * 2);



print: CSNaNType->__add__ == CSObject->__add__;

