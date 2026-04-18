#include <windows.h>  // Для работы с DLL в Windows

extern "C" {

struct Node {
    int data;      // Значение элемента (целое число)
    Node* next;    // Указатель на следующий узел (замыкает кольцо)
};

// Глобальные указатели на элементы списка
Node* head = NULL;     // Указывает на ПОСЛЕДНИЙ добавленный элемент
Node* current = NULL;  // Указывает на ТЕКУЩИЙ элемент

// Создание/очистка списка
__declspec(dllexport) void create_list() {
    // Обнуляем указатели - список становится пустым
    head = NULL;
    current = NULL;
}

// 1. ВСТАВКА ЭЛЕМЕНТА (после текущего)
__declspec(dllexport) void insert(int value) {
    // Выделяем память под новый узел
    Node* newNode = new Node;
    newNode->data = value;     // Записываем значение
    
    if (head == NULL) {
        // СЛУЧАЙ 1: Список пуст
        // Создаем список из одного элемента
        head = newNode;        // head указывает на новый узел
        current = newNode;     // current указывает на новый узел
        newNode->next = head;  // Узел ссылается сам на себя (кольцо)
    } else {
        // СЛУЧАЙ 2: Список не пуст
        // Вставляем новый элемент после текущего (head - это последний)
        newNode->next = head->next;  // Новый узел ссылается на первый элемент
        head->next = newNode;        // Последний узел ссылается на новый
        head = newNode;              // head теперь указывает на новый узел (он стал последним)
    }
}

// 2. ЧТЕНИЕ ТЕКУЩЕГО ЭЛЕМЕНТА
__declspec(dllexport) int read_current() {
    // Тернарный оператор: если список пуст, то -1, иначе значение текущего
    return current == NULL ? -1 : current->data;
}

// 3. УДАЛЕНИЕ ТЕКУЩЕГО ЭЛЕМЕНТА
__declspec(dllexport) bool delete_current() {
    // Проверяем, пуст ли список
    if (current == NULL) return false;
    
    // СЛУЧАЙ 1: В списке только один элемент
    if (current->next == current) {
        delete current;        // Освобождаем память
        head = current = NULL; // Обнуляем указатели
        return true;
    }
    
    // СЛУЧАЙ 2: В списке больше одного элемента
    // Находим ПРЕДЫДУЩИЙ элемент (перед удаляемым)
    Node* prev = current;
    while (prev->next != current) {
        prev = prev->next;
    }
    
    // Сохраняем удаляемый узел во временную переменную
    Node* temp = current;
    
    // Перепривязываем указатели: предыдущий ссылается на следующий
    prev->next = current->next;
    
    // Новым текущим становится следующий элемент
    current = current->next;
    
    // Освобождаем память удаленного узла
    delete temp;
    
    // Если удалили последний элемент (head), обновляем head
    if (head == temp) {
        head = prev;
    }
    
    return true;
}

// 4. ПОЛУЧЕНИЕ ВСЕХ ЭЛЕМЕНТОВ СПИСКА
__declspec(dllexport) void get_all_elements(int* buffer, int* size) {
    // Если список пуст
    if (head == NULL) {
        *size = 0; 
        return;
    }
    
    // Начинаем с ПЕРВОГО элемента (head->next)
    Node* temp = head->next;
    int count = 0;
    
    // Обходим кольцо один раз
    do {
        buffer[count++] = temp->data;  // Записываем значение в буфер
        temp = temp->next;              // Переходим к следующему
    } while (temp != head->next);       // Пока не вернулись к началу
    
    *size = count;  // Возвращаем количество элементов
}

// 5. ПОЛУЧЕНИЕ ИНДЕКСА ТЕКУЩЕГО ЭЛЕМЕНТА
__declspec(dllexport) int get_current_index() {
    // Если список пуст или нет текущего элемента
    if (head == NULL || current == NULL) return -1;
    
    // Начинаем с ПЕРВОГО элемента
    Node* temp = head->next;
    int idx = 0;
    
    // Идем по списку, пока не найдем current
    while (temp != current) {
        temp = temp->next;
        idx++;
    }
    
    return idx;  // Возвращаем позицию (0, 1, 2...)
}

// 6. ОЧИСТКА СПИСКА
__declspec(dllexport) void clear_list() {
    // Если список уже пуст
    if (head == NULL) return;
    
    // Начинаем с ПЕРВОГО элемента
    Node* temp = head->next;
    Node* nextNode;
    
    // Удаляем все элементы, обходя кольцо
    do {
        nextNode = temp->next;  // Запоминаем следующий
        delete temp;             // Удаляем текущий
        temp = nextNode;         // Переходим к следующему
    } while (temp != head->next);  // Пока не вернулись к началу
    
    // Обнуляем указатели - список пуст
    head = current = NULL;
}

// 7. ЦИКЛИЧЕСКИЙ СДВИГ
__declspec(dllexport) void shift(char direction, int steps) {
    // Если список пуст или содержит один элемент
    if (head == NULL || head->next == head) return;
    
    if (direction == 'L') {
        // СДВИГ ВЛЕВО: текущий индекс УВЕЛИЧИВАЕТСЯ
        // Перемещаем указатель current вперед на steps шагов
        for (int i = 0; i < steps; i++) {
            current = current->next;  // Переход к следующему элементу
        }
    } 
    else if (direction == 'R') {
        // СДВИГ ВПРАВО: текущий индекс УМЕНЬШАЕТСЯ
        // Перемещаем указатель current назад на steps шагов
        for (int i = 0; i < steps; i++) {
            // Находим ПРЕДЫДУЩИЙ элемент
            Node* prev = current;
            while (prev->next != current) {
                prev = prev->next;
            }
            current = prev;  // Переход к предыдущему элементу
        }
    }
}

}
