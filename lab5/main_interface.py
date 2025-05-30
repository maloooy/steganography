import sys, os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QTabWidget,
    QPlainTextEdit, QGroupBox, QDialog, QDialogButtonBox, QGridLayout
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

from visual_attack import create_bit_image
from chi_square import chi_square_analysis
from rs_analysis import rs_analysis, RSAnalysis
from aump import aump_analysis


class SteganalysisInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Стегоанализ изображений")
        self.resize(1200, 700)
        self.analysis_file_paths = []
        self.analysis_results_text = ""
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_analysis_tab()

    def init_analysis_tab(self):
        self.tab_analysis = QWidget()
        self.tabs.addTab(self.tab_analysis, "Стегоанализ")
        main_layout = QHBoxLayout(self.tab_analysis)

        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_select_analysis = QPushButton("Загрузить изображение(я)")
        self.btn_select_analysis.clicked.connect(self.select_analysis_images)
        control_layout.addWidget(self.btn_select_analysis)

        self.lbl_analysis_paths = QLabel("Файлы не выбраны")
        control_layout.addWidget(self.lbl_analysis_paths)

        self.btn_run_analysis = QPushButton("Проанализировать")
        self.btn_run_analysis.clicked.connect(self.analyze_images)
        control_layout.addWidget(self.btn_run_analysis)

        self.txt_analysis_results = QPlainTextEdit()
        self.txt_analysis_results.setReadOnly(True)
        control_layout.addWidget(self.txt_analysis_results)

        self.btn_save_analysis = QPushButton("Сохранить результаты в файл")
        self.btn_save_analysis.clicked.connect(self.save_analysis_results)
        control_layout.addWidget(self.btn_save_analysis)

        control_layout.addStretch(1)
        main_layout.addWidget(control_panel, 0)

        self.lbl_analysis_image = QLabel("Нет изображения")
        self.lbl_analysis_image.setFixedSize(400, 400)
        self.lbl_analysis_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.lbl_analysis_image, 1)

    def select_analysis_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите изображения для анализа",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.pgm);;Все файлы (*)"
        )
        if files:
            self.analysis_file_paths = files
            display_text = "\n".join(files)
            self.lbl_analysis_paths.setText(display_text)
            if len(files) == 1:
                image = QImage(files[0])
                if image.isNull():
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение!")
                    return
                pixmap = QPixmap.fromImage(image).scaled(
                    self.lbl_analysis_image.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.lbl_analysis_image.setPixmap(pixmap)
            else:
                self.lbl_analysis_image.clear()
                self.lbl_analysis_image.setText("Множественный анализ")

    def analyze_images(self):
        if not self.analysis_file_paths:
            QMessageBox.warning(self, "Ошибка", "Файлы не выбраны!")
            return
        if len(self.analysis_file_paths) == 1:
            image = QImage(self.analysis_file_paths[0])
            if image.isNull():
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение!")
                return
            bit_planes = []
            for bit in range(8):
                bp = create_bit_image(image, bit)
                bit_planes.append(bp)
            chi_values = chi_square_analysis(image)
            rs_results = rs_analysis(image, overlap=True)
            aump_val = aump_analysis(image)

            analyzer = RSAnalysis(2, 2)
            result_names = analyzer.get_result_names()
            rs_text = "RS-анализ:\n"
            for i, name in enumerate(result_names):
                rs_text += f"{name}: {rs_results[i]:.3f}\n"

            info_text = (
                f"Хи-квадрат (среднее): {chi_values.mean():.2f}\n"
                f"AUMP beta: {aump_val:.3f}\n\n"
                + rs_text
            )
            dialog = QDialog(self)
            dialog.setWindowTitle("Визуальный анализ стегоизображения")
            layout = QVBoxLayout(dialog)
            info_label = QLabel(info_text)
            layout.addWidget(info_label)
            grid = QGridLayout()
            for i, bp_img in enumerate(bit_planes):
                label = QLabel(f"Бит {i}")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid.addWidget(label, 0, i)
                lbl_bp = QLabel()
                pix_bp = QPixmap.fromImage(bp_img).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
                lbl_bp.setPixmap(pix_bp)
                lbl_bp.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid.addWidget(lbl_bp, 1, i)
            layout.addLayout(grid)
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            dialog.exec()
        else:
            results = ""
            for file_path in self.analysis_file_paths:
                image = QImage(file_path)
                if image.isNull():
                    results += f"{file_path}: Ошибка загрузки!\n\n"
                    continue
                chi_values = chi_square_analysis(image)
                rs_results = rs_analysis(image, overlap=True)
                aump_val = aump_analysis(image)
                analyzer = RSAnalysis(2,2)
                result_names = analyzer.get_result_names()
                rs_text = ""
                for i, name in enumerate(result_names):
                    rs_text += f"{name}: {rs_results[i]:.3f}\n"
                results += (
                    f"Файл: {os.path.basename(file_path)}\n"
                    f"  Хи-квадрат (среднее): {chi_values.mean():.2f}\n"
                    f"  AUMP beta: {aump_val:.3f}\n"
                    f"  RS-анализ:\n{rs_text}"
                    "---------------------------------------------\n"
                )
            self.analysis_results_text = results
            self.txt_analysis_results.setPlainText(results)
            QMessageBox.information(self, "Результаты анализа", "Анализ выполнен для выбранных изображений.")

    def save_analysis_results(self):
        if not self.analysis_results_text:
            QMessageBox.warning(self, "Ошибка", "Нет результатов для сохранения!")
            return
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения результатов")
        if not folder:
            return
        filename = "analysis_results.txt"
        save_path = os.path.join(folder, filename).replace("\\", "/")
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.analysis_results_text)
            QMessageBox.information(self, "OK", f"Результаты сохранены в {save_path}")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить результаты:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganalysisInterface()
    window.show()
    sys.exit(app.exec())
