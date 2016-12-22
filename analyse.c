#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// A little helper to see where scores are made in the Q-values

int main(int argc, char * argv[])
{
	char buffer[400], *p;
	FILE * fp;
	int n, linecount;

	memset(buffer, '\0', 200);
	fp = fopen(argv[1], "r");
	if ( !fp ) {
		printf("Not a reasonable file\n");
		return 0;
	}

	linecount = 1;
	while ( fgets(buffer,199, fp) != NULL ){
		n = atoi(buffer);
		p = buffer;
		while (*p){
			if (*p == '\n'){
				*p = '\0';
			}
			++p;
		}
		if ( n > 0 ){
			printf("line: %d: %d (%s)\n", linecount, n, buffer);
		}
		++linecount;
		memset(buffer,'\0', 200);
	}

	fclose(fp);
}