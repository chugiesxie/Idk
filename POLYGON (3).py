import tkinter as tk
import numpy as np

def polygon_area(points):
    x, y = np.hsplit(np.array(points), 2)
    return 0.5 * np.abs(np.dot(x.T, np.roll(y, 1)) - np.dot(y.T, np.roll(x, 1))).item() 

def polygon_centroid(points):
    x, y = np.hsplit(np.array(points), 2)
    area = polygon_area(points)
    cx = np.abs(np.sum((x + np.roll(x, 1)) * (x * np.roll(y, 1) - np.roll(x, 1) * y)).item() / (6 * area))
    cy = np.abs(np.sum((y + np.roll(y, 1)) * (x * np.roll(y, 1) - np.roll(x, 1) * y)).item() / (6 * area))
    return (cx, cy)

def pixel_to_cm(pixels, ppi=96):
    return pixels / ppi * 2.54

class PolygonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polygon Area and Centroid Calculator")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        self.points = []
        self.canvas.bind("<Button-1>", self.add_point)
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack()
        self.draw_polygon_button = tk.Button(root, text="Draw Polygon", command=self.draw_polygon)
        self.draw_polygon_button.pack()
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.area_label = tk.Label(root, text="Diện tích của đa giác: ")
        self.area_label.pack()
        self.coordinates_label = tk.Label(root, text="Tọa độ các điểm: ")
        self.coordinates_label.pack()
        self.centroid_label = tk.Label(root, text="Tọa độ trọng tâm: ")
        self.centroid_label.pack()

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
        self.update_coordinates_label()

    def update_coordinates_label(self):
        coordinates_text = "Tọa độ các điểm: " + ", ".join([f"({x}, {y})" for x, y in self.points])
        self.coordinates_label.config(text=coordinates_text)

    def draw_polygon(self):
        if (len(self.points) < 3):
            print("Cần ít nhất 3 điểm để tạo thành một đa giác.")
            return
        self.canvas.create_polygon(self.points, outline='black', fill='', width=2)

    def calculate(self):
        if (len(self.points) < 3):
            print("Cần ít nhất 3 điểm để tạo thành một đa giác.")
            return
        area = polygon_area(self.points)
        centroid = polygon_centroid(self.points)
        area_cm = pixel_to_cm(area)  # Chuyển đổi diện tích từ pixel vuông sang cm vuông
        self.area_label.config(text=f"Diện tích của đa giác: {area_cm:.2f} cm²")
        self.centroid_label.config(text=f"Tọa độ trọng tâm: ({centroid[0]:.2f}, {centroid[1]:.2f})")
        print(f"Diện tích của đa giác: {area_cm:.2f} cm²")
        print(f"Trọng tâm của đa giác: {centroid}")
        self.draw_centroid(centroid)

    def draw_centroid(self, centroid):
        cx, cy = centroid
        self.canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill="red")
        
    def reset(self):
        self.points = []
        self.canvas.delete("all")
        self.area_label.config(text="Diện tích của đa giác: ")
        self.coordinates_label.config(text="Tọa độ các điểm: ")
        self.centroid_label.config(text="Tọa độ trọng tâm: ")

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonApp(root)
    root.mainloop()
