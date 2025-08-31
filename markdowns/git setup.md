Here's a step-by-step guide to set up SSH authentication for Git/GitHub on Ubuntu Linux:

---

*1. Generate an SSH Key Pair*
bash
# Generate a new SSH key (use Ed25519 algorithm)
ssh-keygen -t ed25519 -C "your_email@example.com"

- Replace your_email@example.com with your GitHub email.
- When prompted for a file name, press Enter to save to the default location (~/.ssh/id_ed25519).
- Optional: Set a passphrase for extra security (you’ll need to enter it once per session).

---

*2. Add the SSH Key to the SSH Agent*
bash
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your SSH private key to the agent
ssh-add ~/.ssh/id_ed25519


---

*3. Add the SSH Public Key to GitHub*
- Copy the public key to your clipboard:
  bash
  sudo apt install xclip -y  # Install xclip if missing
  xclip -selection clipboard < ~/.ssh/id_ed25519.pub
  
  Or manually display and copy:
  bash
  cat ~/.ssh/id_ed25519.pub
  

- Go to *GitHub → Settings → SSH and GPG Keys → New SSH Key*.
- Paste the key (starts with ssh-ed25519 ...) and save.

---

*4. Configure Git to Use SSH*
- If you already have a repository cloned via HTTPS:
  bash
  # Navigate to your repo
  cd /path/to/your/repo

  # Change remote URL to SSH
  git remote set-url origin git@github.com:username/repository.git
  
  Replace username and repository with your GitHub username and repo name.

- For new repositories, always clone using the SSH URL:
  bash
  git clone git@github.com:username/repository.git
  

---

*5. Test the Connection*
bash
ssh -T git@github.com

- If successful, you’ll see: Hi username! You’ve successfully authenticated...

---

*Troubleshooting Tips*
- *Permissions*: Ensure your private key has strict permissions:
  bash
  chmod 600 ~/.ssh/id_ed25519
  chmod 644 ~/.ssh/id_ed25519.pub
  
- *Passphrase*: If you set one, use ssh-add once per session or configure ssh-agent to remember it.
- *Multiple Keys*: Use an SSH config file (~/.ssh/config) if you have multiple accounts.

---

*Done!* Now git push and other commands will use SSH authentication automatically.