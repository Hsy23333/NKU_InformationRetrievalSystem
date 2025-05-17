import os

# 设置目标文件夹路径（当前目录）
target_dir = "./snapshots"  # 可以改成你自己的路径

# 设置前缀
prefix = "12club_"

# 遍历目录下所有文件
for filename in os.listdir(target_dir):
    file_path = os.path.join(target_dir, filename)
    
    # 跳过目录，只处理文件
    if os.path.isfile(file_path) and not filename.startswith(prefix):
        new_filename = prefix + filename
        new_file_path = os.path.join(target_dir, new_filename)
        os.rename(file_path, new_file_path)
        print(f"已重命名：{filename} -> {new_filename}")
