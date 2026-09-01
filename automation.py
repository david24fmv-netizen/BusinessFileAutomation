import os
import shutil


def organize_folder(folder_path):
    """
    Organiza automáticamente los archivos de una carpeta
    según su extensión.
    """

    categories = {
        "Documents": [
            ".pdf", ".doc", ".docx", ".txt",
            ".xls", ".xlsx", ".csv", ".ppt", ".pptx"
        ],

        "Images": [
            ".jpg", ".jpeg", ".png", ".gif",
            ".bmp", ".webp", ".svg"
        ],

        "Videos": [
            ".mp4", ".avi", ".mkv", ".mov",
            ".wmv", ".flv"
        ],

        "Audio": [
            ".mp3", ".wav", ".flac",
            ".aac", ".ogg", ".m4a"
        ],

        "Archives": [
            ".zip", ".rar", ".7z",
            ".tar", ".gz"
        ],

        "Code": [
            ".py", ".js", ".html", ".css",
            ".java", ".cpp", ".c", ".json",
            ".sql"
        ]
    }

    results = []

    stats = {
        "Documents": 0,
        "Images": 0,
        "Videos": 0,
        "Audio": 0,
        "Archives": 0,
        "Code": 0,
        "Others": 0
    }

    if not os.path.exists(folder_path):
        return ["ERROR: The selected folder does not exist."]

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        # Ignorar carpetas
        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        category = "Others"

        for category_name, extensions in categories.items():

            if extension in extensions:
                category = category_name
                break

        category_folder = os.path.join(
            folder_path,
            category
        )

        os.makedirs(
            category_folder,
            exist_ok=True
        )

        destination = os.path.join(
            category_folder,
            filename
        )

        # Evitar sobrescribir archivos existentes
        if os.path.exists(destination):

            base_name, extension = os.path.splitext(filename)

            counter = 1

            while os.path.exists(destination):

                new_filename = f"{base_name}_{counter}{extension}"

                destination = os.path.join(
                    category_folder,
                    new_filename
                )

                counter += 1

        try:

            shutil.move(
                file_path,
                destination
            )

            stats[category] += 1

            results.append(
                f"✓ {filename} → {category}"
            )

        except Exception as error:

            results.append(
                f"✗ {filename} → ERROR: {error}"
            )

    if not results:

        results.append(
            "No files were found to organize."
        )

    return results, stats
