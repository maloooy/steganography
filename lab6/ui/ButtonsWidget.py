import PyQt6.QtWidgets
import PyQt6.QtGui
import PyQt6.QtCore


class ButtonsWidget(PyQt6.QtWidgets.QWidget):
    def __init__(self, parent: PyQt6.QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)
        self.setMinimumWidth(200)  # Установим минимальную ширину виджета

        self.populate()

    def populate(self):
        self.__main_layout = PyQt6.QtWidgets.QVBoxLayout(self)

        # Кнопки
        self.open_images_button = PyQt6.QtWidgets.QPushButton(text="Open Images", parent=self)
        self.analyze_images_button = PyQt6.QtWidgets.QPushButton(text="Start Analysis", parent=self)
        self.save_results_button = PyQt6.QtWidgets.QPushButton(text="Save Results", parent=self)

        # SpinBox'ы в группах
        self.rs_group_box = PyQt6.QtWidgets.QGroupBox("RS Parameters")
        self.rs_m_spinbox = PyQt6.QtWidgets.QSpinBox(self.rs_group_box)
        self.rs_m_spinbox.setToolTip("RS m")
        self.rs_m_spinbox.setValue(2)
        self.rs_n_spinbox = PyQt6.QtWidgets.QSpinBox(self.rs_group_box)
        self.rs_n_spinbox.setToolTip("RS n")
        self.rs_n_spinbox.setValue(2)
        rs_layout = PyQt6.QtWidgets.QHBoxLayout(self.rs_group_box)
        rs_layout.addWidget(self.rs_m_spinbox)
        rs_layout.addWidget(self.rs_n_spinbox)
        self.rs_group_box.setLayout(rs_layout)

        self.aump_group_box = PyQt6.QtWidgets.QGroupBox("AUMP Parameters")
        self.aump_block_size_spinbox = PyQt6.QtWidgets.QSpinBox(self.aump_group_box)
        self.aump_block_size_spinbox.setToolTip("AUMP block size")
        self.aump_block_size_spinbox.setValue(16)
        self.aump_parameter_spinbox = PyQt6.QtWidgets.QSpinBox(self.aump_group_box)
        self.aump_parameter_spinbox.setToolTip("AUMP parameters")
        self.aump_parameter_spinbox.setValue(5)
        aump_layout = PyQt6.QtWidgets.QHBoxLayout(self.aump_group_box)
        aump_layout.addWidget(self.aump_block_size_spinbox)
        aump_layout.addWidget(self.aump_parameter_spinbox)
        self.aump_group_box.setLayout(aump_layout)

        # Выпадающий список методов
        self.method_dropdown = PyQt6.QtWidgets.QComboBox(self)
        self.method_dropdown.addItems(["Method 1", "Method 2", "Method 3"])

        # Добавление всех элементов на основной макет
        self.__main_layout.addWidget(self.open_images_button)
        self.__main_layout.addWidget(self.rs_group_box)
        self.__main_layout.addWidget(self.aump_group_box)
        self.__main_layout.addWidget(self.method_dropdown)
        self.__main_layout.addWidget(self.analyze_images_button)
        self.__main_layout.addWidget(self.save_results_button)
        self.__main_layout.addStretch()
