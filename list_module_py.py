class Node:
    def __init__(self, data):
        self.data = data                    # Сохраняем значение в узле
        self.next = None                    # Ссылка на следующий узел (пока пустая)

class CircularList:
    def __init__(self):
        self.head = None                    # Указатель на последний добавленный элемент
        self.current = None                 # Указатель на текущий элемент
    
    def insert(self, value):
        new_node = Node(value)              # Создаем новый узел с переданным значением
        if self.head is None:               # Если список пуст
            self.head = new_node            # head указывает на новый узел
            self.current = new_node         # current указывает на новый узел
            new_node.next = self.head       # Узел ссылается сам на себя (замыкаем кольцо)
        else:                               # Если список не пуст
            new_node.next = self.head.next  # Новый узел ссылается на первый элемент
            self.head.next = new_node       # Последний узел ссылается на новый
            self.head = new_node            # head теперь указывает на новый узел (он стал последним)
        return True                         # Возвращаем True (вставка всегда успешна)
    
    def read_current(self):
        return None if self.current is None else self.current.data  # Если список пуст - None, иначе значение текущего
    
    def delete_current(self):
        if self.current is None:                    # Если список пуст
            return False                            # Возвращаем False (нечего удалять)
        if self.current.next == self.current:       # Если в списке только один элемент
            self.head = None                        # Обнуляем head (список пуст)
            self.current = None                     # Обнуляем current
        else:                                       # Если элементов несколько
            prev = self.current                     # Начинаем поиск предыдущего элемента
            while prev.next != self.current:        # Пока не нашли предыдущий
                prev = prev.next                    # Переходим к следующему узлу
            prev.next = self.current.next           # Предыдущий ссылается на следующий после удаляемого
            self.current = self.current.next        # Новым текущим становится следующий элемент
            if self.head == self.current:           # Если удалили последний элемент (head)
                self.head = prev                    # Обновляем head на предыдущий
        return True                                 # Возвращаем True (удаление успешно)
    
    def get_all_elements(self):
        if self.head is None:                       # Если список пуст
            return []                               # Возвращаем пустой список
        elements = []                               # Создаем пустой список для результата
        temp = self.head.next                       # Начинаем с первого элемента
        while True:                                 # Бесконечный цикл для обхода кольца
            elements.append(temp.data)              # Добавляем значение в результат
            if temp == self.head:                   # Если вернулись к началу
                break                               # Выходим из цикла
            temp = temp.next                        # Переходим к следующему узлу
        return elements                             # Возвращаем список всех элементов
    
    def get_current_index(self):
        if self.head is None or self.current is None:  # Если список пуст или нет текущего
            return -1                               # Возвращаем -1 (индекс не найден)
        temp = self.head.next                       # Начинаем с первого элемента
        idx = 0                                     # Начинаем счет с 0
        while temp != self.current:                 # Пока не нашли текущий элемент
            temp = temp.next                        # Переходим к следующему
            idx += 1                                # Увеличиваем счетчик
        return idx                                  # Возвращаем найденный индекс
    
    def clear(self):
        self.head = None                            # Обнуляем head (список становится пустым)
        self.current = None                         # Обнуляем current
    
    def shift(self, direction, steps):
        if self.head is None or self.head.next == self.head:  # Если список пуст или один элемент
            return False                            # Возвращаем False (сдвиг невозможен)
        if direction == 'L':                        # Если сдвиг влево
            for _ in range(steps):                  # Повторяем steps раз
                self.current = self.current.next    # Перемещаем current к следующему (индекс +1)
        elif direction == 'R':                      # Если сдвиг вправо
            for _ in range(steps):                  # Повторяем steps раз
                prev = self.current                 # Начинаем поиск предыдущего
                while prev.next != self.current:    # Пока не нашли предыдущий
                    prev = prev.next                # Переходим к следующему
                self.current = prev                 # Перемещаем current к предыдущему (индекс -1)
        return True
