import os
import subprocess
import sys

GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET = "\033[0m"

def run_command(command, description):
    print(f"{YELLOW}[*] {description}...{RESET}")
    try:

        subprocess.run(command, shell=True, check=True)
        print(f"{GREEN}[✓] Успешно: {description}{RESET}\n")
    except subprocess.CalledProcessError:
        print(f"\033[0;31m[!] Ошибка при выполнении: {description}\033[0m")
        sys.exit(1)

def main():
    print(f"{GREEN}========================================")
    print("    Добро пожаловать в VPS Installer!   ")
    print(f"========================================{RESET}\n")

    run_command("apt update && apt upgrade -y", "Обновление системных пакетов")
    
    run_command("apt install -y curl nano ufw", "Установка базовых утилит (curl, nano, ufw)")

    run_command("apt install fail2ban -y && systemctl enable fail2ban && systemctl start fail2ban", 
                "Установка и настройка Fail2Ban")

    choice_docker = input("Хотите установить Docker и Docker Compose? (y/n): ").strip().lower()
    if choice_docker in ['y', 'yes']:
        run_command("curl -fsSL https://get.docker.com | sh", "Автоматическая установка Docker")

    print("Дополнительные компоненты для установки:")
    print("1) 3x-ui (Панель управления VPN)")
    print("2) Caddy (Удобный веб-сервер)")
    print("3) Wireguard (Производительный VPN)")
    print("4) Завершить работу")
    
    choices = input("\nВыберите номера через пробел (например, '1 3'): ").strip().split()

    for choice in choices:
        if choice == "1":
            run_command("bash <(curl -Ls https://raw.githubusercontent.com/Morytyann/3x-ui/master/install.sh)", 
                        "Установка панели 3x-ui")

        elif choice == "2":
            run_command("apt-get install -y debian-keyring debian-archive-keyring apt-transport-https && "
                        "curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg && "
                        "curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list && "
                        "apt-get update && apt-get install caddy -y", 
                        "Установка веб-сервера Caddy")

        elif choice == "3":
            run_command("apt install -y wireguard", "Установка Wireguard")

        elif choice == "4":
            print("[*] Завершение выбора компонентов.")
            break
            
        else:
            print(f"[!] Неизвестный пункт меню: {choice}")

    print(f"\n{GREEN}=== Настройка сервера успешно завершена! ==={RESET}")

if __name__ == "__main__":
    main()