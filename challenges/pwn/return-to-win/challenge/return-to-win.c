#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    const char *flag = getenv("FLAG");
    if (flag == NULL) {
        flag = "UNKNOWN{local_test_flag}";
    }
    printf("You reached win! %s\n", flag);
    fflush(stdout);
    exit(0);
}

void vuln(void) {
    char buf[64];
    puts("Return to Win");
    puts("Can you redirect execution?");
    printf("input: ");
    read(0, buf, 160);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    puts("Returned safely.");
    return 0;
}
