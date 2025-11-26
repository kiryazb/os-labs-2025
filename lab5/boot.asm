org 0x7c00

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7c00
    sti

    mov si, logo
    call print_str

    mov si, logo1
    call print_str

    mov si, logo2
    call print_str

    mov si, prompt_q
    call print_str
    call read_char_echo
    mov si, crlf
    call print_str
    cmp al, 'y'
    je yes
    cmp al, 'Y'
    je yes
no:
    mov si, ans_no
    call print_str
    jmp move_start
yes:
    mov si, ans_yes
    call print_str
    jmp move_start

move_start:
    mov si, move_hint
    call print_str
    call draw_obstacles
    mov byte [player_row], 12
    mov byte [player_col], 40
    call draw_player

move_loop:
    mov ah, 0x00
    int 0x16
    cmp al, 'w'
    je move_up
    cmp al, 'W'
    je move_up
    cmp al, 's'
    je move_down
    cmp al, 'S'
    je move_down
    cmp al, 'a'
    je move_left
    cmp al, 'A'
    je move_left
    cmp al, 'd'
    je move_right
    cmp al, 'D'
    je move_right
    cmp al, 27
    je halt
    jmp move_loop

move_up:
    cmp byte [player_row], 0
    je move_loop
    call erase_player
    dec byte [player_row]
    jmp draw_and_loop

move_down:
    cmp byte [player_row], 24
    je move_loop
    call erase_player
    inc byte [player_row]
    jmp draw_and_loop

move_left:
    cmp byte [player_col], 0
    je move_loop
    call erase_player
    dec byte [player_col]
    jmp draw_and_loop

move_right:
    cmp byte [player_col], 79
    je move_loop
    call erase_player
    inc byte [player_col]

draw_and_loop:
    call check_collision
    cmp al, 1
    je game_over
    call draw_player
    jmp move_loop

game_over:
    mov si, over_msg
    call print_str
    jmp halt

halt:
    hlt
    jmp halt

print_str:
    pusha
.p:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0e
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    jmp .p
.done:
    popa
    ret

read_char_echo:
    mov ah, 0x00
    int 0x16
    call echo_char
    ret

echo_char:
    push ax
    push bx
    mov ah, 0x0e
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    pop bx
    pop ax
    ret

erase_player:
    push ax
    mov al, ' '
    mov dh, [player_row]
    mov dl, [player_col]
    call put_char_at
    pop ax
    ret

draw_player:
    push ax
    mov al, '@'
    mov dh, [player_row]
    mov dl, [player_col]
    call put_char_at
    pop ax
    ret

put_char_at:
    push bx
    push dx
    push ax
    mov ah, 0x02
    mov bh, 0x00
    int 0x10
    pop ax
    mov ah, 0x0e
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    pop dx
    pop bx
    ret

draw_obstacles:
    push si
    push ax
    push dx
    mov si, obstacles
    mov al, '#'
.d:
    lodsb
    cmp al, 0xFF
    je .done
    mov dh, al
    lodsb
    mov dl, al
    call put_char_at
    jmp .d
.done:
    pop dx
    pop ax
    pop si
    ret

check_collision:
    push si
    push bx
    mov si, obstacles
.c:
    lodsb
    cmp al, 0xFF
    je .nohit
    mov ah, al
    lodsb
    mov bh, al
    mov al, [player_row]
    cmp al, ah
    jne .c
    mov al, [player_col]
    cmp al, bh
    jne .c
    mov al, 1
    jmp .ret
.nohit:
    mov al, 0
.ret:
    pop bx
    pop si
    ret

; --- data ---
logo  db "  __   --",0x0D,0x0A,0
logo1 db " /  \ |__ ",0x0D,0x0A,0
logo2 db " \__/  __|",0x0D,0x0A,0
prompt_q    db "Do you like OS? (y/n): ",0
ans_yes     db "Nice!",0x0D,0x0A,0
ans_no      db "Ok.",0x0D,0x0A,0
move_hint   db 0x0D,0x0A,"WASD move @, ESC quits.",0x0D,0x0A,0
over_msg    db "Game over!",0x0D,0x0A,0
crlf        db 0x0D,0x0A,0

player_row  db 0
player_col  db 0
obstacles   db 5,10, 10,30, 15,60, 0xFF

times 510-($-$$) db 0
dw 0xAA55
