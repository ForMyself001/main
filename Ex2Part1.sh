#!/bin/bash

username="Lab29-test"
base_path="C:\Users\Igor\Desktop\Lib\Repositories"
# Функция для создания папок репозиториев и отправки изменений на GitHub
create_and_push_logs() {

    repositories=$(curl -s "https://api.github.com/users/$1/repos" | jq -r '.[].name')

    for repo_name in $repositories; do

        cleaned_repo_name=$(echo "$repo_name" | sed 's/[^a-zA-Z0-9._-]/_/g')
        repo_path="$base_path/$cleaned_repo_name"

        if [ ! -d "$repo_path" ]; then
            mkdir -p "$repo_path"
            echo "Создана папка для репозитория $repo_name"
        fi
        
        branches=$(git ls-remote --heads "https://github.com/Lab29-test/$cleaned_repo_name" | sed 's?.*refs/heads/??')

        for branch in $branches; do
            branch_path="$repo_path/$branch"

            if [ -d "$branch_path" ]; then
                # Обновляем существующую ветку
                git -C "$branch_path" pull origin "$branch"
                echo "Обновлена ветка $branch в репозитории $repo_name"
            else
                # Клонируем ветку, если ее нет локально
                git clone --single-branch --branch "$branch" "https://github.com/$1/$repo_name" "$branch_path"
                echo "Склонирована ветка $branch из репозитория $repo_name"
            fi

            # Создаем файл
            current_datetime=$(date +"%Y-%m-%d_%H-%M-%S")
            log_filepath="$branch_path/info_bash.txt"
            echo "Date and time: $current_datetime" > "$log_filepath"
            echo "Repo: $repo_name" >> "$log_filepath"
            echo "Branch: $branch" >> "$log_filepath"

            # Добавляем и коммитим файл
            git -C "$branch_path" add "$log_filepath"
            git -C "$branch_path" commit -m "Add log file for $branch in $repo_name"
            git -C "$branch_path" push origin "$branch"
            echo "Файл для ветки $branch в репозитории $repo_name отправлен на GitHub"
        done
    done
}

# Вызываем объединенную функцию
create_and_push_logs "$username"