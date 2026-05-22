#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

echo -e "${GREEN}========================================${RESET}"
echo -e "${GREEN}    Инициализация VPS Quick Start...   ${RESET}"
echo -e "${GREEN}========================================${RESET}\n"

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Ошибка: Этот скрипт должен быть запущен от имени root (через sudo).${RESET}"
    exit 1
fi

echo -e "${YELLOW}[*] Синхронизация системных репозиториев...${RESET}"
apt-get update -y


if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[*] Python 3 не найден. Установка...${RESET}"
    apt-get install python3 -y
else
    echo -e "${GREEN}[✓] Python 3 уже установлен.${RESET}"
fi

if ! command -v wget &> /dev/null; then
    echo -e "${YELLOW}[*] Утилита wget не найдена. Установка...${RESET}"
    apt-get install wget -y
fi

URL="https://raw.githubusercontent.com/pupsikdhd/vps-quick-start/refs/heads/main/quick_start.py"
TMP_SCRIPT="/tmp/quick_start.py"

echo -e "${YELLOW}[*] Загрузка инсталлятора из GitHub...${RESET}"
wget -qO $TMP_SCRIPT "$URL"

echo -e "${GREEN}[*] Запуск основного сценария...${RESET}\n"
python3 $TMP_SCRIPT

rm -f $TMP_SCRIPT
echo -e "\n${GREEN}[✓] Временные файлы удалены. Обёртка завершила работу.${RESET}"