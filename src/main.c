 /*
  *	@(#)cstart.c	1.20
  *	SMC88 Startup code
  *	Default, exit code will loop forever.
  *
  *	DEFINES to tune this startup code:
  *
  *		COPY (default)	-> produce code to clear 'CLEAR' sections AND initialize 'INIT' sections,
  *				   'CLEAR' and 'INIT' segments do not have to be consecutive
  *
  *	On exit the program will fall into an endless loop.
  */

int something;

int main(void) {
  for (;;) _halt();
}
