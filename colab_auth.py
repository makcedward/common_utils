import os

try:
  from google.colab import drive
except:
  print(f"Not in Colab env?")

class ColabAuth:
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
    drive.mount('/content/drive/')
    remote_key_dir = "/content/drive/MyDrive/config/.colab-github"
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
