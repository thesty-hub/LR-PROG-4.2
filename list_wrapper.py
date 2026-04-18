import list_module_py as py_list
import ctypes
import os

class ListInterface:
    def __init__(self, backend_type="python"):
        self.backend_type = backend_type
        self.list = None
        self.cpp_lib = None
        self.buffer_size = 1000
        
        if backend_type == "python":
            self.list = py_list.CircularList()
        elif backend_type == "cpp":
            self._init_cpp()
    
    def _init_cpp(self):
        try:
            dll_path = os.path.join(os.path.dirname(__file__), 'clist.dll')
            self.cpp_lib = ctypes.CDLL(dll_path)
            self._setup_cpp_functions()
            self.cpp_lib.create_list()
        except Exception as e:
            print(f"Ошибка C++: {e}")
            self.backend_type = "python"
            self.list = py_list.CircularList()
    
    def _setup_cpp_functions(self):
        self.cpp_lib.create_list.argtypes = []
        self.cpp_lib.insert.argtypes = [ctypes.c_int]
        self.cpp_lib.read_current.argtypes = []
        self.cpp_lib.read_current.restype = ctypes.c_int
        self.cpp_lib.delete_current.argtypes = []
        self.cpp_lib.delete_current.restype = ctypes.c_bool
        self.cpp_lib.get_all_elements.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self.cpp_lib.get_current_index.argtypes = []
        self.cpp_lib.get_current_index.restype = ctypes.c_int
        self.cpp_lib.clear_list.argtypes = []
        self.cpp_lib.shift.argtypes = [ctypes.c_char, ctypes.c_int]
    
    def insert(self, value):
        if self.backend_type == "python":
            return self.list.insert(value)
        self.cpp_lib.insert(value)
        return True
    
    def read_current(self):
        if self.backend_type == "python":
            return self.list.read_current()
        v = self.cpp_lib.read_current()
        return None if v == -1 else v
    
    def delete_current(self):
        if self.backend_type == "python":
            return self.list.delete_current()
        return self.cpp_lib.delete_current()
    
    def get_all_elements(self):
        if self.backend_type == "python":
            return self.list.get_all_elements()
        buffer = (ctypes.c_int * self.buffer_size)()
        size = ctypes.c_int()
        self.cpp_lib.get_all_elements(buffer, ctypes.byref(size))
        return [buffer[i] for i in range(size.value)]
    
    def get_current_index(self):
        if self.backend_type == "python":
            return self.list.get_current_index()
        return self.cpp_lib.get_current_index()
    
    def clear(self):
        if self.backend_type == "python":
            self.list.clear()
        else:
            self.cpp_lib.clear_list()
    
    def shift(self, direction, steps):
        if self.backend_type == "python":
            return self.list.shift(direction, steps)
        dir_byte = direction.encode('utf-8')
        self.cpp_lib.shift(dir_byte, steps)
        return True
