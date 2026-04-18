import tkinter as tk                                            # Импорт основного модуля для создания GUI
from tkinter import messagebox, simpledialog, ttk               # Импорт дополнительных виджетов: диалоги, комбобокс
from list_wrapper import ListInterface                          # Импорт обертки для работы с разными реализациями списка

class CircularListApp:                                          # Главный класс приложения
    def __init__(self, root):                                   # Конструктор, вызывается при создании объекта
        self.root = root                                        # Сохраняем ссылку на главное окно
        self.root.title("Кольцевой список")                     # Устанавливаем заголовок окна
        self.root.geometry("1000x500")                          # Устанавливаем размер окна
        self.root.configure(bg='#f0f0f0')                       # Устанавливаем цвет фона
        self.list = ListInterface("python")                     # Создаем модуль (по умолчанию Python)
        self.create_widgets()                                   # Вызываем метод создания интерфейса
        self.update_display()                                   # Вызываем метод обновления визуализации
    
    def create_widgets(self):                                   # Метод создания всех виджетов интерфейса
        main = tk.Frame(self.root, bg='white')                  # Создаем основной фрейм с белым фоном
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Размещаем фрейм с отступами и растяжением
 
        tk.Label(main, text="КОЛЬЦЕВОЙ ОДНОСВЯЗНЫЙ СПИСОК",     # Создаем метку с заголовком
                font=("Arial", 16, "bold"), bg='#696969', fg='white', pady=5).pack(fill=tk.X)  # Настройка шрифта, цвета и растяжение по ширине
        
        # Выбор реализации
        top = tk.Frame(main, bg='white')                                            # Фрейм для выбора реализации
        top.pack(fill=tk.X, pady=5)                                                 # Размещаем с растяжением по ширине
        tk.Label(top, text="Реализация:", bg='white').pack(side=tk.LEFT)            # Метка "Реализация"
        self.backend_var = tk.StringVar(value="python")                             # Переменная для хранения выбранной реализации
        ttk.Combobox(top, textvariable=self.backend_var, values=["python", "cpp"],  # Выпадающий список
                     state="readonly", width=12).pack(side=tk.LEFT, padx=5)         # Только для чтения, ширина 12
        tk.Button(top, text="Применить", command=self.change_backend,               # Кнопка для смены реализации
                 bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)               # Синий фон, белый текст
        
        # Кнопки операций
        btn_frame = tk.Frame(main, bg='white')                      # Фрейм для кнопок операций
        btn_frame.pack(pady=10)                                     # Размещаем с отступом сверху/снизу
        buttons = [("Вставить", self.insert_element, '#4CAF50'),    # Список кнопок: текст, команда, цвет
                   ("Удалить", self.delete_element, '#FF0000'),
                   ("Найти", self.find_by_index, '#FF9800'),
                   ("Текущий", self.read_element, '#2196F3'),
                   ("Очистить", self.clear_list, '#607D8B'),
                   ("Сдвиг", self.shift_elements, '#FF5722'),
                   ("Выход", self.root.quit, '#BDB76B')]
        
        for text, cmd, color in buttons:                                    # Перебираем все кнопки
            tk.Button(btn_frame, text=text, command=cmd, width=10,          # Создаем кнопку
                     bg=color, fg='black', font=("Arial", 10, "bold"),      # Настройка цвета и шрифта
                     relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=2)     # Размещаем горизонтально
        
        # Холст и статус
        self.canvas = tk.Canvas(main, bg='#D3D3D3', height=200)     # Создаем холст для рисования списка
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)        # Размещаем с растяжением
        
        self.status_var = tk.StringVar(value="Количество: 0")       # Переменная для строки статуса
        tk.Label(main, textvariable=self.status_var, bg='#696969',  # Метка для отображения статуса
                fg='white', anchor=tk.W, padx=10).pack(fill=tk.X, side=tk.BOTTOM)  # Прижимаем вниз

    def change_backend(self):  # Метод для смены реализации списка
        try: 
            self.list = ListInterface(self.backend_var.get())           # Создаем новый экземпляр с выбранной реализацией
            self.update_display()                                       # Обновляем визуализацию
            messagebox.showinfo("Успех", f"Реализация: {self.backend_var.get()}")   # Сообщение об успехе
        except Exception as e:                                                      # Если ошибка
            messagebox.showerror("Ошибка", str(e))                                  # Показываем сообщение об ошибке
    
    def update_display(self):                   # Метод для отрисовки списка на холсте
        self.canvas.delete("all")               # Очищаем холст
        elems = self.list.get_all_elements()    # Получаем все элементы списка
        cnt, cur = len(elems), self.list.get_current_index()  # Количество элементов и текущий индекс
        
        if cnt:  # Если есть элементы
            x, y, size = 50, 100, 60            # Начальные координаты и размер квадрата
            for i, val in enumerate(elems):     # Перебираем все элементы
                x_pos = x + i * 80              # Вычисляем позицию по X
                color = "#90EE90" if i == cur else "#87CEEB"                        # Зеленый для текущего, голубой для остальных
                self.canvas.create_rectangle(x_pos, y-20, x_pos+size, y+20,         # Рисуем квадрат
                                            fill=color, outline='black', width=2)   # Заливка и контур
                self.canvas.create_text(x_pos+30, y, text=str(val),                 # Рисуем текст
                                       font=("Arial", 12, "bold"))                  # Шрифт для текста
                
                if i < cnt-1:   # Если не последний элемент
                    self.canvas.create_line(x_pos+size, y, x_pos+75, y,             # Рисуем стрелку к следующему
                                           arrow=tk.LAST, width=2)                  # Со стрелкой на конце
                else:  # Если последний элемент
                    self.canvas.create_line(x_pos+size, y, x_pos+size, y-40, width=2)   # Линия вверх
                    self.canvas.create_line(x_pos+size, y-40, x, y-40, width=2)         # Линия влево
                    self.canvas.create_line(x, y-40, x, y, arrow=tk.LAST, width=2)      # Линия вниз со стрелкой
        
        backend = "Python" if self.list.backend_type == "python" else "C++"             # Название реализации
        self.status_var.set(f"{backend} | Количество: {cnt}" +                          # Обновляем статус
                           (f" | Индекс: {cur}" if cnt else ""))                        # Добавляем индекс если есть элементы
    
    def insert_element(self):  # Метод для вставки элемента
        v = simpledialog.askstring("Вставка", "Значение:", parent=self.root)    # Диалог ввода
        if v and v.strip().lstrip('-').isdigit():                               # Если введено и это число
            self.list.insert(int(v))                                            # Вставляем число
            self.update_display()                                               # Обновляем отображение
        elif v:  # Если введено, но не число
            messagebox.showerror("Ошибка", "Введите число!")              # Сообщение об ошибке
    
    def read_element(self):                                             # Метод для чтения текущего элемента
        v = self.list.read_current()                                    # Получаем значение текущего
        if v is None:                                                   # Если список пуст
            messagebox.showwarning("Ошибка", "Список пуст!")            # Предупреждение
        else:  # Если есть элемент
            messagebox.showinfo("Текущий элемент", str(v))              # Показываем значение
    
    def delete_element(self):                                   # Метод для удаления текущего элемента
        if self.list.read_current() is None:                    # Если список пуст
            messagebox.showwarning("Ошибка", "Список пуст!")    # Предупреждение
        elif messagebox.askyesno("Подтверждение", "Удалить текущий элемент?"):  # Спрашиваем подтверждение
            self.list.delete_current()     # Удаляем текущий
            self.update_display()          # Обновляем отображение
    
    def find_by_index(self):   # Метод для поиска элемента по индексу
        elems = self.list.get_all_elements()  # Получаем все элементы
        if not elems:  # Если список пуст
            messagebox.showwarning("Ошибка", "Список пуст!")  # Предупреждение
            return  # Выходим
        idx = simpledialog.askinteger("Поиск", f"Индекс (0-{len(elems)-1}):",               # Диалог ввода индекса
                                     minvalue=0, maxvalue=len(elems)-1, parent=self.root)   # Ограничения ввода
        if idx is not None:  # Если индекс введен
            messagebox.showinfo("Результат", f"Элемент {idx}: {elems[idx]}")                # Показываем результат
    
    def clear_list(self):  # Метод для очистки списка
        if self.list.read_current() is not None and messagebox.askyesno("Очистка", "Очистить список?"):  # Если не пуст и подтверждение
            self.list.clear()        # Очищаем список
            self.update_display()    # Обновляем отображение
    
    def shift_elements(self):                   # Метод для циклического сдвига
        if self.list.read_current() is None:    # Если список пуст
            messagebox.showwarning("Ошибка", "Список пуст!")  # Предупреждение
            return  # Выходим
        
        dlg = tk.Toplevel(self.root)    # Создаем дополнительное окно
        dlg.title("Циклический сдвиг")  # Заголовок окна
        dlg.geometry("300x300")         # Размер окна
        dlg.configure(bg='white')       # Цвет фона
        dlg.transient(self.root)        # Связываем с главным окном
        dlg.grab_set()                  # Делаем модальным
        
        tk.Label(dlg, text="ПАРАМЕТРЫ СДВИГА", font=("Arial", 12, "bold"),  # Заголовок в окне
                bg='#696969', fg='white', pady=5).pack(fill=tk.X)           # Серый фон, белый текст
        
        cont = tk.Frame(dlg, bg='white', padx=15, pady=10)                  # Рамка для содержимого
        cont.pack()                                                         # Размещаем
        
        # Информация о текущем индексе
        cur_idx = self.list.get_current_index()                             # Получаем текущий индекс
        cur_val = self.list.read_current()                                  # Получаем текущее значение
        info = f"Текущий: индекс {cur_idx} | значение {cur_val}"            # Формируем строку
        tk.Label(cont, text=info, bg='#e0e0e0', font=("Arial", 9),          # Метка с информацией
                pady=3).pack(fill=tk.X, pady=(0, 10))                       # Размещаем
        
        # Направление
        tk.Label(cont, text="Направление:", bg='white').pack()  # Метка "Направление"
        dir_var = tk.StringVar(value="left")                    # Переменная для направления
        f = tk.Frame(cont, bg='white')                          # Фрейм для радиокнопок
        f.pack()  # Размещаем
        tk.Radiobutton(f, text="← ВЛЕВО", variable=dir_var, value="left",       # Кнопка "Влево"
                      bg='white').pack(side=tk.LEFT, padx=5)                    # Размещаем горизонтально
        tk.Radiobutton(f, text="→ ВПРАВО", variable=dir_var, value="right",     # Кнопка "Вправо"
                      bg='white').pack(side=tk.LEFT, padx=5)                    # Размещаем горизонтально
        
        # Шаги
        tk.Label(cont, text="Количество шагов:", bg='white').pack(pady=(10,0))  # Метка "Количество шагов"
        steps = tk.IntVar(value=1)                                              # Переменная для количества шагов
        tk.Spinbox(cont, from_=1, to=100, textvariable=steps, width=8).pack()   # Поле ввода с выбором

        def apply():                # Внутренняя функция для применения сдвига
            s = steps.get()         # Получаем количество шагов
            old_idx = self.list.get_current_index()  # Запоминаем старый индекс
            
            # Сдвиг на указанное количество шагов
            if dir_var.get() == "left":     # Если выбрано "Влево"
                self.list.shift('L', s)     # Сдвиг влево
                txt = "ВЛЕВО"               # Текст для сообщения
            else:                           # Если выбрано "Вправо"
                self.list.shift('R', s)     # Сдвиг вправо
                txt = "ВПРАВО"              # Текст для сообщения
            
            self.update_display()           # Обновляем отображение
            new_idx = self.list.get_current_index()  # Получаем новый индекс
            messagebox.showinfo("Успех",    # Показываем сообщение об успехе
                f"Сдвиг {txt} на {s} шаг(ов)\n"
                f"Индекс: {old_idx} → {new_idx}")
            dlg.destroy()                   # Закрываем диалоговое окно
        
        tk.Button(cont, text="ПРИМЕНИТЬ", command=apply,            # Кнопка "Применить"
                 bg='#4CAF50', fg='white', width=10).pack(pady=5)   # Зеленая кнопка
        tk.Button(cont, text="ОТМЕНА", command=dlg.destroy,         # Кнопка "Отмена"
                 bg='#f44336', fg='white', width=10).pack()         # Красная кнопка

if __name__ == "__main__":          # Проверка, что файл запущен напрямую
    root = tk.Tk()                  # Создаем главное окно
    app = CircularListApp(root)     # Создаем экземпляр приложения
    root.mainloop()                 # Запускаем главный цикл обработки событий
