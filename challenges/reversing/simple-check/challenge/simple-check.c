#include <stdio.h>
#include <string.h>

static unsigned char encoded_flag[] = {
    98, 121, 124, 121, 120, 96, 121, 76, 83, 82, 84, 88, 90, 71, 94, 91,
    82, 104, 67, 95, 82, 104, 84, 95, 82, 84, 92, 68, 74, 0
};

static void print_flag(void) {
    for (int i = 0; encoded_flag[i] != 0; i++) {
        putchar(encoded_flag[i] ^ 0x37);
    }
    putchar('\n');
}

static int check(const char *s) {
    if (strlen(s) != 10) return 0;
    if (s[0] != 'r') return 0;
    if (s[1] != 'e') return 0;
    if (s[2] != 'v') return 0;
    if (s[3] != '_') return 0;
    if (s[4] != 'c') return 0;
    if (s[5] != 'h') return 0;
    if (s[6] != 'e') return 0;
    if (s[7] != 'c') return 0;
    if (s[8] != 'k') return 0;
    if (s[9] != '7') return 0;
    return 1;
}

int main(void) {
    char input[64];
    printf("code: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';
    if (check(input)) {
        print_flag();
    } else {
        puts("no");
    }
    return 0;
}
