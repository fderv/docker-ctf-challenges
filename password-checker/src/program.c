#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

#define ROT 13

int encrypt_input(char *input_str) {

	for (int i=0; i < strlen(input_str); i=i+2) {
		if (input_str[i+1] != '\0') {
			char ch = input_str[i];
			input_str[i] = input_str[i+1];
			input_str[i+1] = ch;
		}
	}

	for (int i=0; i < strlen(input_str); i++) {
		char c = input_str[i];
		int e;
		if(c >='a' && c <='z')
        {
			if (c + ROT <= 'z') {
				e = c + ROT;
			}
			else {
                e = c - ROT;
            }
        }
		input_str[i] = e;
	}

	return 0;
}

int validate_input(char *input_str) {

	if (strlen(input_str) > 32) {
		return 1;
	}

	for (int i=0; i < strlen(input_str); i++) {
		char current_char = input_str[i];
		if (isalpha(current_char) == 0) {
			return 1;
		}
	}

	for(int i = 0; i < strlen(input_str); i++){
			input_str[i] = tolower(input_str[i]);
		}

	return 0;
}

int main() {

	char pass[32];
	int x=10;

	while (x!=0) {
		
		printf("\nInput the password: ");
		if (fgets(pass, sizeof pass, stdin)) {
  			// Was it missing a '\n'?
			if (strchr(pass, '\n') == NULL) {
    			// Read rest of line and throw it away
    			int ch;
    			while ((ch = fgetc(stdin)) != '\n' && ch != EOF) {;}
  			}
		}

		pass[strcspn(pass,"\n")] = '\0';

		if (validate_input(pass) == 1) {
			printf("Invalid password.\nPassword must only consist of letters and cannot be longer than 32 characters.");
			continue;
		}

		encrypt_input(pass);

		if (strcmp(pass, "password") == 0) {
			printf("Correct! You've found the flag.");
			return 0;
		}
		else {
			printf("Wrong password. You entered %s", pass);
		}
	}
	
	return 0;
}