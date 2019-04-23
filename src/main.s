; E0C88 compiler v1.2 r3                  SN00000000-069 (c) 2000 TASKING, Inc.
; options: -O2 -Ml -Iinclude
$CASE ON
$MODEL L

	NAME	"MAIN"
	SYMB	TOOL, "E0C88 compiler v1.2", 1
	SYMB	TYPE, 256, "bit", 'g', 0, 1
	GLOBAL	__start_cpt
	DEFSECT	".comm0", CODE, SHORT	AT 00H

	SECT	".comm0"
	DW	__start_cpt

	DEFSECT	".comm", CODE, SHORT
	SECT	".comm"
__start_cpt:
	SYMB	TYPE, 257, 'X', 136, #1, 2, 0
	SYMB	ALAB, __start_cpt, #257

	GLOBAL	__START
	__START:

	;==========================================================================
	;===================  system initialization  ==============================
	;==========================================================================

	LD	SP,#@DOFF(__lc_es)			; stack pointer initialize
	LD	BR,#0FFh					; BR register initialize to I/O area

	;---------------  bus mode setting  ---------------------------------------
						; MCU & MPU mode
	LD	[BR:00h],#0
									; single chip mode
									; /CE0,/CE1,/CE2,/CE3:disenabled

	;--------------  bus and clock control  -----------------------------------
	LD	[BR:02h],#0
    								; clock = OSC1
									; OSC3off
									; normal power mode

	;---------------  stack pointer page address  -----------------------------
	LD	[BR:01h],#@DPAG(__lc_es-1)	; set stack pointer page
									; __lc_es is NOT within stack area


	EXTERN  (DATA,TINY)__lc_b_.tbss		;BR is used for tiny data
	LD	BR,#(@DOFF(__lc_b_.tbss) >> 8)

	CARL	__copytable
	CARL	_main
	CARL	__exit
	RETE	
