# TinyOS boot sector

Минимальный загрузочный сектор (x86 real mode):
- выводит название и ASCII‑лого;
- спрашивает имя и приветствует;
- задаёт вопрос y/n и отвечает (показывает 2+2 или отказ).

Сборка/запуск через Docker+QEMU (текстовый curses-экран):
```bash
docker build --platform linux/386 -t boot-hello .
docker run --rm -it --platform linux/386 boot-hello
```

Управление:
- введите имя, Enter завершает ввод, Backspace работает;
- ответьте `y`/`n` (или `Y`/`N`) на вопрос.
