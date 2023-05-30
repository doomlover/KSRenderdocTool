import sys
import os
import csv

if len(sys.argv) < 2:
    print("Please provide a log file path as an argument.")
    sys.exit(1)

log_file_path = sys.argv[1]

with open(log_file_path, 'r') as file:
    log_data = file.read()

current_pass = None
is_static_mesh = False
is_skeletal_mesh = False
is_landscape = False

# Initialize counts
count_data = {
    "ShadowDepthPass": {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0},
    "CustomDepth": {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0},
    "MobileRenderPrePass": {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0},
    "MobileBasePass": {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0},
    "Translucency": {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0}
}

def process_draw_command(line, current_pass_data, is_static_mesh, is_skeletal_mesh, is_landscape):
    current_pass_data["draw_commands"] += 1

    if is_static_mesh:
        current_pass_data["static_meshes"] += 1
    if is_skeletal_mesh:
        current_pass_data["skeletal_meshes"] += 1
    if is_landscape:
        current_pass_data["landscape"] += 1

    if "vkCmdDrawIndexed(" in line:
        indices, instances = map(int, line.split('(')[1].split(')')[0].split(', '))
        triangles = (indices // 3) * instances
    elif "vkCmdDrawIndexedIndirect(" in line:
        triangles = int(line.split(' => ')[1].split(', ')[0][1:])

    current_pass_data["triangles"] += triangles
    if is_static_mesh:
        current_pass_data["static_mesh_triangles"] += triangles
    if is_skeletal_mesh:
        current_pass_data["skeletal_mesh_triangles"] += triangles
    if is_landscape:
        current_pass_data["landscape_triangles"] += triangles

for line in log_data.splitlines():
    line = line.strip()
    if "ShadowDepthPass" in line:
        current_pass = "ShadowDepthPass"
    elif "CustomDepth" in line:
        current_pass = "CustomDepth"
    elif "MobileRenderPrePass" in line:
        current_pass = "MobileRenderPrePass"
    elif "MobileBasePass" in line:
        current_pass = "MobileBasePass"
    elif "Translucency" in line:
        current_pass = "Translucency"
    elif "vkCmdEndRenderPass" in line:
        current_pass = None
    elif "SM_" in line:
        is_static_mesh = True
    elif "SKM_" in line:
        is_skeletal_mesh = True
    elif "Landscape" in line:
        is_landscape = True
    elif "vkCmdDrawIndexed" in line or "vkCmdDrawIndexedIndirect" in line:
        if current_pass is not None:
            process_draw_command(line, count_data[current_pass], is_static_mesh, is_skeletal_mesh, is_landscape)
        is_static_mesh = False
        is_skeletal_mesh = False
        is_landscape = False

# Calculate totals
total_counts = {"draw_commands": 0, "triangles": 0, "static_meshes": 0, "static_mesh_triangles": 0, "skeletal_meshes": 0, "skeletal_mesh_triangles": 0, "landscape": 0, "landscape_triangles": 0}
for stage in count_data.values():
    total_counts["draw_commands"] += stage["draw_commands"]
    total_counts["triangles"] += stage["triangles"]
    total_counts["static_meshes"] += stage["static_meshes"]
    total_counts["static_mesh_triangles"] += stage["static_mesh_triangles"]
    total_counts["skeletal_meshes"] += stage["skeletal_meshes"]
    total_counts["skeletal_mesh_triangles"] += stage["skeletal_mesh_triangles"]
    total_counts["landscape"] += stage["landscape"]
    total_counts["landscape_triangles"] += stage["landscape_triangles"]

# Output results
for pass_name, data in count_data.items():
    print(f"Number of draw commands within {pass_name}: {data['draw_commands']}")
    print(f"Number of triangles within {pass_name}: {data['triangles']}")
    print(f"Number of StaticMesh objects within {pass_name}: {data['static_meshes']}")
    print(f"Number of triangles within StaticMesh objects in {pass_name}: {data['static_mesh_triangles']}")
    print(f"Number of SkeletalMesh objects within {pass_name}: {data['skeletal_meshes']}")
    print(f"Number of triangles within SkeletalMesh objects in {pass_name}: {data['skeletal_mesh_triangles']}")
    print(f"Number of Landscape within {pass_name}: {data['landscape']}")
    print(f"Number of triangles within Landscape in {pass_name}: {data['landscape_triangles']}")
    print("----------------------------------------------------")

print(f"Total number of draw commands: {total_counts['draw_commands']}")
print(f"Total number of triangles: {total_counts['triangles']}")
print(f"Total number of StaticMesh objects: {total_counts['static_meshes']}")
print(f"Total number of triangles within StaticMesh objects: {total_counts['static_mesh_triangles']}")
print(f"Total number of SkeletalMesh objects: {total_counts['skeletal_meshes']}")
print(f"Total number of triangles within SkeletalMesh objects: {total_counts['skeletal_mesh_triangles']}")
print(f"Total number of Landscape: {total_counts['landscape']}")
print(f"Total number of triangles within Landscape: {total_counts['landscape_triangles']}")

# Write to CSV
csv_file_path = os.path.splitext(log_file_path)[0] + ".csv"
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Rendering Stage", "Draw Commands", "Triangles", "StaticMesh Objects", "StaticMesh Triangles", "SkeletalMesh Objects", "SkeletalMesh Triangles", "Landscape", "Landscape Triangles"])
    for pass_name, data in count_data.items():
        csv_writer.writerow([pass_name, data['draw_commands'], data['triangles'], data['static_meshes'], data['static_mesh_triangles'], data['skeletal_meshes'], data['skeletal_mesh_triangles'], data['landscape'], data['landscape_triangles']])
    csv_writer.writerow(["----------------------------------------------------", "", "", "", "", "", ""])
    csv_writer.writerow(["Total", total_counts['draw_commands'], total_counts['triangles'], total_counts['static_meshes'], total_counts['static_mesh_triangles'], total_counts['skeletal_meshes'], total_counts['skeletal_mesh_triangles'], total_counts['landscape'], total_counts['landscape_triangles']])

print(f"Statistics written to CSV file: {csv_file_path}")

