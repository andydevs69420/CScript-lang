
import [MODULE, add, State] from "class_test.csx";

print: "From IF", State->flags;

var x = 2;
if (x == 2) {
    print: "Yes";
} else {
    print: "No";
}
