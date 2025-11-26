# Збуривский К.А. Аэ-21-22

# TinyOS boot sector

Минимальный загрузочный сектор (x86 real mode):
- выводит название и ASCII‑лого;
- спрашивает имя и приветствует;
- задаёт вопрос y/n и отвечает (Nice! или Ok.).
- Дает сыграть в мини-игру, где необходимо довести @ до < (управление WASD)

Сборка/запуск через Docker+QEMU (текстовый curses-экран):
```bash
docker build --platform linux/386 -t boot-hello .
docker run --rm -it --platform linux/386 boot-hello
```
