
import "import1_test.csx";
import "system";



func println(_message)
{ return system
            ->stdio
                ->write(_message); }




print: system->path[1];

println("Hello World!");

assert "gwapo ko" != "pangit ko", "Ahhhh so sad!";
