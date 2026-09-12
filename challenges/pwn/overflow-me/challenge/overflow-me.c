#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct frame {
    char name[32];
    unsigned int admin;
};

int main(void) {
    struct frame f = {{0}, 0};
    const char *flag = getenv("FLAG");
    if (flag == NULL) {
        flag = "UNKNOWN{local_test_flag}";
    }

    setvbuf(stdout, NULL, _IONBF, 0);
    puts("Overflow Me");
    puts("admin must become 0x41424344");
    printf("name: ");

    read(0, f.name, 80);

    if (f.admin == 0x41424344) {
        printf("Welcome admin! %s\n", flag);
    } else {
        printf("admin=0x%08x\n", f.admin);
        puts("Access denied.");
    }
    return 0;
}
