import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.widgets import Button

MAP_FILE = "map.json"

# Load or create blank map
if os.path.exists(MAP_FILE):
    with open(MAP_FILE) as f:
        map_data = json.load(f)
else:
    map_data = {
        "rooms": [],
        "pois": []
    }

fig, ax = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)
ax.set_title("Vector Floor Map Editor")
ax.set_xlim(0, 10000)
ax.set_ylim(0, 10000)
ax.set_aspect('equal')
ax.grid(True)

# Store current drawings
drawn_patches = []

# Draw rooms
def draw_map():
    for patch in drawn_patches:
        patch.remove()
    drawn_patches.clear()

    for room in map_data["rooms"]:
        if room["type"] == "rect":
            patch = Rectangle((room["x"], room["y"]), room["w"], room["h"], facecolor='lightblue', edgecolor='black')
        elif room["type"] == "poly":
            patch = Polygon(room["points"], closed=True, facecolor='lightgreen', edgecolor='black')
        drawn_patches.append(ax.add_patch(patch))
        ax.annotate(room["label"], (room["x"] + 20, room["y"] + 20), color='black')

    for poi in map_data["pois"]:
        ax.plot(poi["x"], poi["y"], 'ro')
        ax.annotate(poi["label"], (poi["x"] + 10, poi["y"] + 10), color='red')

    fig.canvas.draw()

draw_map()

# Add POI on click
def on_click(event):
    if event.inaxes != ax: return
    x, y = int(event.xdata), int(event.ydata)
    label = f"POI-{len(map_data['pois'])+1}"
    map_data["pois"].append({"x": x, "y": y, "label": label})
    print(f"Added POI: {label} at ({x},{y})")
    draw_map()

fig.canvas.mpl_connect('button_press_event', on_click)

# Add Room (hardcoded rectangle for demo)
def add_room(event):
    label = f"Room-{len(map_data['rooms'])+1}"
    room = {
        "type": "rect",
        "label": label,
        "x": 1000 + 500*len(map_data['rooms']),
        "y": 1000,
        "w": 2000,
        "h": 1500
    }
    map_data["rooms"].append(room)
    print(f"Added {label}")
    draw_map()

# Save Map
def save_map(event):
    with open(MAP_FILE, "w") as f:
        json.dump(map_data, f, indent=2)
    print("Map saved.")

# Buttons
add_ax = plt.axes([0.1, 0.05, 0.15, 0.075])
add_btn = Button(add_ax, 'Add Room')
add_btn.on_clicked(add_room)

save_ax = plt.axes([0.3, 0.05, 0.15, 0.075])
save_btn = Button(save_ax, 'Save Map')
save_btn.on_clicked(save_map)

plt.show()
