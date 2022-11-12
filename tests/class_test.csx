


class Node
{
    function init(_data)
    { return new Node(_data); }


    function initialize(_data)
    {
        this.data = _data;
        this.head = null;
        this.tail = null;
    }


    function toString()
    {
       
        let format = "";
        let _head  = this;
        
        while (_head) 
        {
            format += _head.data.toString();
            
            _head = _head.tail;

            if (_head)
                format += " -> ";

        }

        return format;
    }
}


var a = Node::init(0);
var b = Node::init(1);
var c = Node::init(4);
var d = Node::init(1);

a.tail = b;
b.head = a;
b.tail = c;
c.head = b;
c.tail = d;
d.head = c;


print: a;




print: typeof new CSInteger(100).toString();

try {

    throw "Error!!!!!!!!!!!!!!!!!!!!!";

}except(err) {
    print: err;
}

