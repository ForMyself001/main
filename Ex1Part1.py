import os
import requests
from git import Repo
from datetime import datetime


def get_github_repositories(username):
    url = f'https://api.github.com/orgs/{username}/repos'
    response = requests.get(url)

    if response.status_code == 200:
        repositories = [repo['name'] for repo in response.json()]
        return repositories
    else:
        return None


def get_repository_branches(username, repo_name):
    url = f'https://api.github.com/repos/{username}/{repo_name}/branches'
    response = requests.get(url)

    if response.status_code == 200:
        branches = [branch['name'] for branch in response.json()]
        return branches
    else:
        print(f"Ошибка при получении {repo_name}")
        print(f"Ошибка при получении веток для репозитория {repo_name}. HTTP статус: {response.status_code}")
        print(f"Ответ сервера: {response.text}")
        return None


def create_repository_folders(username, base_path='.'):
    repositories = get_github_repositories(username)

    if repositories is None:
        print(f"Не удалось получить репозитории для пользователя {username}.")
        return

    for repo_name in repositories:
        repo_path = os.path.join(base_path, repo_name)

        # Создаем папку для репозитория, если ее нет
        os.makedirs(repo_path, exist_ok=True)
        print(f"Создана папка для репозитория {repo_name} в {repo_path}")
        branches = get_repository_branches(username, repo_name)
        if branches is not None:
            download_or_update_branches(username, repo_name, branches, base_path)

    print("Скачивание/обновление завершено.")


def download_or_update_branches(username, repo_name, branches, base_path='.'):
    repo_path = os.path.join(base_path, repo_name)

    # Проверяем, существует ли папка репозитория
    if not os.path.exists(repo_path):
        print(f"Папка для репозитория {repo_name} не найдена.")
        return

    for branch in branches:
        branch_path = os.path.join(repo_path, branch)

        # Если ветка уже существует, обновим ее
        if os.path.exists(branch_path):
            print(f"Обновление ветки {branch} в репозитории {repo_name}...")
            repo = Repo(branch_path)
            origin = repo.remote('origin')
            origin.pull()
            origin.update()
        else:
            # Если ветки нет, склонируем ее из репозитория
            print(f"Клонирование ветки {branch} из репозитория {repo_name}...")
            repo_url = f'https://github.com/{username}/{repo_name}.git'
            Repo.clone_from(repo_url, branch_path, branch=branch)

        create_log_file(branch_path, repo_name, branch)

    print(f"Скачивание/обновление веток для репозитория {repo_name} завершено.")


def create_log_file(branch_path, repo_name, branch):
    # Собираем имя файла с текущей датой и временем
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"info.txt"

    # Полный путь к файлу
    log_filepath = os.path.join(branch_path, log_filename)

    # Создаем или открываем файл и записываем в него информацию
    with open(log_filepath, 'w') as log_file:
        log_file.write(f"Date and time: {current_datetime}\n")
        log_file.write(f"Repo: {repo_name}\n")
        log_file.write(f"Branch: {branch}\n")
    print(f"Создан файл: {log_filepath}")
    try:
        repo = Repo(branch_path)
        # Добавляем файл лога в индекс
        repo.git.add('info.txt')
        # Коммитим изменения
        commit_message = f"Add log file for {branch} in {repo_name}"
        repo.index.commit(commit_message)
        print(f"Файл для ветки {branch} в репозитории {repo_name} закоммичен")
    except Exception as e:
        print(f"Ошибка при коммите и отправке файла лога для ветки {branch} в репозитории {repo_name}: {e}")


def push_all_branches(username, base_path='.'):
    repositories = get_github_repositories(username)

    if repositories is None:
        print(f"Не удалось получить репозитории для пользователя {username}.")
        return

    for repo_name in repositories:
        repo_path = os.path.join(base_path, repo_name)

        # Проверяем, существует ли папка репозитория
        if not os.path.exists(repo_path):
            print(f"Папка для репозитория {repo_name} не найдена.")
            continue

        branches = get_repository_branches(username, repo_name)

        for branch in branches:
            branch_path = os.path.join(repo_path, branch)
            if os.path.exists(branch_path):
                # Переключаемся на ветку
                repo = Repo(branch_path)
                repo.git.checkout(branch)
                # Пушим изменения
                try:
                    repo.git.push('origin', branch)
                    print(f"Изменения ветки {branch} в репозитории {repo_name} успешно отправлены на GitHub.")
                except Exception as e:
                    print(f"В репозитори Ошибка при отправке изменений ветки {branch} в репозитории {repo_name}: {e}")
            else:
                # Если ветки нет, склонируем ее из репозитория
                print(f"Отсутствует ветка локальная ветка {branch}")


if __name__ == "__main__":
    username = "Lab29-test"
    create_repository_folders(username)
    push_all_branches(username)
