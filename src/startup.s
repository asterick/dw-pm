$CASE ON

DEF_IRC MACRO
        OR      SC,#0C0h
^loop:  HALT
        JRS     ^loop
        ENDM

        ;; Begin pokemon mini header
        DEFSECT ".min_header", CODE AT 2100H
        SECT    ".min_header"
        ASCII   "PM"
        JRL     __START
        DB      0, 0, 0
        DUP     26
        DEF_IRC
        ENDM
        ASCII   "NINTENDO"
    
        DEFSECT ".min_header_tail", CODE AT 21BCH
        SECT    ".min_header_tail"
        ASCII   "2P"
        DB      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

        ;; Begin startup code
	DEFSECT	".startup", CODE, SHORT
	SECT	".startup"
__start_cpt:
__START:
        ;==========================================================================
        ;===================  system initialization  ==============================
        ;==========================================================================
        LD      SP, #02000h                      ; stack pointer initialize
        LD      BR, #020h                        ; BR register initialize to I/O area
        LD      [BR:21h], #0Ch
        LD      [BR:25h], #080h
        LD      [BR:80h], #08h
        LD      [BR:81h], #08h
        ;LD     [BR:81h], #09h

        LD      SC, #030h

        LD      [BR:27h], #0FFh
        LD      [BR:28h], #0FFh
        LD      [BR:29h], #0FFh
        LD      [BR:2Ah], #0FFh

_loop:  LD      A, [BR:08Ah]
        LD      [BR:0FEh], #081h
        LD      [BR:0FFh], A
        JRS     _loop
	CARL	__copytable
	CARL	_main
	CARL	__exit
	RETE


        GLOBAL  __start_cpt
        GLOBAL  __START
	EXTERN	(CODE) __copytable
	EXTERN	(CODE) _main
        EXTERN  (CODE) __exit
	CALLS	'_start_cpt', '_copytable'
	CALLS	'_start_cpt', 'main'
	CALLS	'_start_cpt', '_exit'

        
	END
