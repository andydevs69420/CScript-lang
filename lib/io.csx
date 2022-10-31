import "system";

print: system;

func println(_message)
{ 
    print: system;
    return system
            ->stdio
                ->write(_message); }



func scan(_message)
{
    let _value;
    print: _message, (_value = system
                        ->stdio
                            ->scan());
    return _value;
}

