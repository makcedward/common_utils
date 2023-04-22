try:
  from google.colab import drive
except:
  print(f"Not in Colab env?")
improt os


class ColabStore:
  ROOT_DIR = "/content/drive/"
  def __init__(self):
    if not os.path.exists(self.ROOT_DIR):
      drive.mount(self.ROOT_DIR)

  def transfer(self, src_file_paths, dest_file_paths):
    assert len(src_file_paths) == len(dest_file_paths)
    for src, dest in zip(src_file_paths, dest_file_paths):
      os.system(f"cp -s {src} {dest}")