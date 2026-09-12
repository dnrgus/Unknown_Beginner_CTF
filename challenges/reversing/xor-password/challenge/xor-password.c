#include <stdio.h>
#include <string.h>

static unsigned char encoded_password[] = {22, 53, 40, 5, 50, 47, 52, 46, 63, 40, 0};
static unsigned char encoded_flag[] = {
    15, 20, 17, 20, 21, 13, 20, 33, 34, 53, 40, 5, 59, 40, 40, 59, 35, 41,
    5, 59, 40, 63, 5, 40, 63, 44, 63, 40, 41, 51, 56, 54, 63, 39, 0
};

static void decode(unsigned char *buf, unsigned char key) {
    for (int i = 0; buf[i] != 0; i++) {
        buf[i] ^= key;
    }
}

int main(void) {
    char input[64];
    unsigned char password[sizeof(encoded_password)];
    unsigned char flag[sizeof(encoded_flag)];

    memcpy(password, encoded_password, sizeof(encoded_password));
    memcpy(flag, encoded_flag, sizeof(encoded_flag));
    decode(password, 0x5a);
    decode(flag, 0x5a);

    printf("password: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';

    if (strcmp(input, (char *)password) == 0) {
        puts((char *)flag);
    } else {
        puts("try again");
    }
    return 0;
}
