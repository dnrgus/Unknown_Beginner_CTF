#include <stdio.h>
#include <string.h>

static const char *PASSWORD = "blue_keycard";
static unsigned char encoded_flag[] = {
    118, 109, 104, 109, 108, 116, 109, 88, 80, 87, 81, 74, 77, 68, 80, 124,
    65, 70, 69, 76, 81, 70, 124, 81, 86, 77, 77, 74, 77, 68, 94, 0
};

static void print_flag(void) {
    for (int i = 0; encoded_flag[i] != 0; i++) {
        putchar(encoded_flag[i] ^ 0x23);
    }
    putchar('\n');
}

int main(void) {
    char input[64];
    printf("password: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';
    if (strcmp(input, PASSWORD) == 0) {
        print_flag();
    } else {
        puts("wrong");
    }
    return 0;
}
