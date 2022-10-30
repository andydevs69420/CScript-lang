import "import1_test.csx";

import1_test->State->flags += 200;

var hello1_2 = 2;

var v = 0;

print: "v =", import1_test->add(10, 20);
print: import1_test->State->flags;

