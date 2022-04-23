#include <stdio.h>
#include <string.h>

int main() {
	char *str = "або\0";

	// scanf ("%s", str);
	printf ("str = %s, strlen = %d\n", str, strlen (str));
	for (int i = 0; i < strlen (str); i++) {
		printf ("str[%d] = %c (%d)\n", i, str[i], str[i]);
	}

	// for (int i = 0; i < 128; i ++) {
	// 	printf ("%d = %c\n", i, i);
	// }
}