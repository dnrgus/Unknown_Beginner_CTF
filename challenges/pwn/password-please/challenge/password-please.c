#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *PASSWORD = "open_sesame_2026";

int main(void) {
    char input[64];
    const char *flag = getenv("FLAG");
    if (flag == NULL) {
        flag = "UNKNOWN{local_test_flag}";
    }

    setvbuf(stdout, NULL, _IONBF, 0);
    puts("Password Please");
    printf("password: ");

    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';

    if (strcmp(input, PASSWORD) == 0) {
        printf("Correct! %s\n", flag);
    } else {
        puts("Nope.");
    }
    return 0;
}
