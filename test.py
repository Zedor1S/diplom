import cv2
import sys
import numpy as np

def enhance_image(image_path, filter_choices, save_path=None):
    """
    Обробляє зображення за вибором користувача і зберігає його.

    :param image_path: Шлях до вхідного зображення.
    :param filter_choices: Список вибраних фільтрів для застосування.
    :param save_path: Шлях для збереження обробленого зображення.
    """
    # Завантаження зображення
    image = cv2.imread(image_path)

    # Перевірка чи вдалося завантажити зображення
    if image is None:
        print("Не вдалося завантажити зображення.")
        return

    # Ітеруємося по кожному вибраному фільтру та застосовуємо його
    for filter_choice in filter_choices:
        if filter_choice == 'blur':
            # Застосування фільтру розмиття (blur)
            image = cv2.blur(image, (10, 10))  # Застосовуємо розмиття з ядром 10x10
        elif filter_choice == 'enhance_saturation':
            # Збільшення насиченості кольорів
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hsv_image[:, :, 1] = hsv_image[:, :, 1] * 1.5  # Збільшення насиченості на 50%
            image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        elif filter_choice == 'edge_detection':
            # Виявлення країв
            image = cv2.Canny(image, 100, 200)  # Застосовуємо алгоритм виявлення країв Canny
        elif filter_choice == 'grayscale':
            # Перетворення зображення в чорно-біле
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif filter_choice == 'negative':
            # Негатив зображення
            image = 255 - image
        elif filter_choice == 'rotate':
            # Поворот зображення
            angle = int(input("Введіть кут повороту (у градусах): "))
            image, new_dimensions = rotate_image(image, angle)
            # Зміна розміру рамки зображення
            x, y, w, h = new_dimensions
            image = image[y:y+h, x:x+w]
        else:
            print(f"Невідомий фільтр: {filter_choice}. Пропускаємо.")

    # Збереження обробленого зображення, якщо вказано шлях для збереження
    if save_path:
        cv2.imwrite(save_path, image)
        print(f"Оброблене зображення збережено за шляхом: {save_path}")
    else:
        # Збереження обробленого зображення як оригіналу
        cv2.imwrite(image_path, image)
        print(f"Оброблене зображення замінило оригінал: {image_path}")


def rotate_image(image, angle):
    """
    Повертає зображення на заданий кут.

    :param image: Зображення для обертання.
    :param angle: Кут обертання в градусах. Положення за годинниковою стрілкою.
    :return: Обернуте зображення та нові координати рамки.
    """
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Обчислення нових координат рамки
    corners = np.array([[0, 0], [width, 0], [0, height], [width, height]])
    rotated_corners = cv2.transform(np.array([corners]), rotation_matrix)[0]
    min_x = int(np.min(rotated_corners[:, 0]))
    max_x = int(np.max(rotated_corners[:, 0]))
    min_y = int(np.min(rotated_corners[:, 1]))
    max_y = int(np.max(rotated_corners[:, 1]))
    new_width = max_x - min_x
    new_height = max_y - min_y

    # Повернення обернутого зображення та нових координат рамки
    return rotated_image, (min_x, min_y, new_width, new_height)


def show_available_filters():
    """
    Показує список доступних фільтрів.
    """
    print("Доступні фільтри:")
    print("1. blur")
    print("2. enhance_saturation")
    print("3. edge_detection")
    print("4. grayscale")
    print("5. negative")
    print("6. rotate")


if __name__ == "__main__":
    # Отримання шляху до фотографії від користувача
    image_path = input("Введіть шлях до фото: ")

    # Перевірка наявності шляху до фотографії
    if not image_path:
        print("Enter the path to the photo")
        sys.exit(1)

    # Показати список доступних фільтрів
    show_available_filters()

    # Вибір фільтрів
    filters_input = input("Enter filter numbers separated by commas:")
    filter_choices = [filter_choice.strip() for filter_choice in filters_input.split(',')]

    # Опціональний ввід шляху для збереження
    save_path = input("Enter the path to save the processed image (or leave blank to replace the original): ")

    # Виклик функції обробки зображення
    enhance_image(image_path, filter_choices, save_path)
