try:
  from google.colab import drive
except:
  print(f"Not in Colab env?")
import os


class ColabAuth:
  DRIVE_BASE_DIR = "/content/drive/"

  @staticmethod
  def mount():
    if not os.path.exists(ColabAuth.DRIVE_BASE_DIR):
      drive.mount(ColabAuth.DRIVE_BASE_DIR)

  @staticmethod
  def ssh(
    generate:bool=False,
    regenerate:bool=False,
    show:bool=False,
    algorithm:str="rsa"
  ):
    """Helper function for generating ssh key.
    
    Parameters
    ----------
    generate : bool
      Generate new SSH key if true

    regenerate : bool
      Force generating new SSH key if true. Existing key will be
      deleted if exists.
      
    show : bool
      Show public key if true

    algorithm: str
      Algorithm for generating SSH key.
    """
    
    ColabAuth.mount()
    remote_key_dir = os.path.join(
      ColabAuth.DRIVE_BASE_DIR,
      "MyDrive",
      "config",
      ".colab-github"
    )
    remote_private_key_path = os.path.join(
      remote_key_dir,
      f"id_{algorithm}"
    )
    remote_public_key_path = os.path.join(
      remote_key_dir,
      f"id_{algorithm}.pub"
    )
    local_private_key_path = os.path.join(
      "~/",
      ".ssh",
      f"id_{algorithm}"
    )
    local_public_key_path = os.path.join(
      "~/",
      ".ssh",
      f"id_{algorithm}.pub"
    )

    if generate or regenerate:
      if regenerate:
        if os.path.isfile(remote_private_key_path):
          os.system(f"rm {remote_private_key_path}")
        if os.path.isfile(remote_public_key_path):
          os.system(f"rm {remote_public_key_path}")
      # create folder in google drive
      os.system(f"mkdir -p {remote_key_dir}") 
      # generate ssh key and persisting into google drive
      os.system(f"ssh-keygen -t {algorithm} -f {remote_private_key_path} -N ''")

    # Clone SSH key from google drive
    os.system("mkdir -p ~/.ssh")
    os.system(f"cp -s {remote_private_key_path} {local_private_key_path}")
    os.system(f"cp -s {remote_public_key_path} {local_public_key_path}")
    os.system(f"chmod go-rwx {local_public_key_path}")

    # add github to known hosts
    os.system(f"ssh-keyscan -t {algorithm} github.com >> ~/.ssh/known_hosts")

    if show:
      with open(os.path.expanduser(local_public_key_path), "r") as f:
        print("Public Key")
        print(f.read())

  @staticmethod
  def openai(
    generate=False,
    key=None,
    show:bool=False,
  ):
    ColabAuth.mount()

    remote_file_path = os.path.join(
      ColabAuth.DRIVE_BASE_DIR,
      "MyDrive",
      "config",
      ".openai",
      "api_key.txt"      
    )

    if generate and key is not None:
      with open(remote_file_path, 'w') as f:
        f.write(key)

    if os.path.exists(remote_file_path):
      with open(remote_file_path, 'r') as f:
        key = f.read()
        if show:
          print(key)
        os.environ["OPENAI_API_KEY"] = key
    else:
      print("No OpenAI API Key.")