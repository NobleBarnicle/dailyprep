Terminal Commands

Create a virtual environment
python3 -m venv venv

Activate the virtual environment
source venv/bin/activate

Install requirements.txt
pip3 install -r requirements.txt

Git - check current remote repo
git remote -v

Git - add all files to commit
git add .

Git - commit changes
git commit -m "commit message"

Git - push changes to remote repo
git push origin main

List directory contents
ls
ls -la (detailed view with hidden files)

Change directory
cd <directory_name>
cd .. (go up one level)
cd ~ (go to home directory)

Print working directory
pwd

Create directory
mkdir <directory_name>

Remove directory
rmdir <directory_name> (empty directory only)
rm -r <directory_name> (directory and contents)

Create file
touch <filename>

Remove file
rm <filename>

Copy file/directory
cp <source> <destination>
cp -r <source_dir> <destination_dir> (for directories)

Move/rename file/directory
mv <source> <destination>

View file contents
cat <filename>
less <filename> (scrollable)
head -n <num> <filename> (first n lines)
tail -n <num> <filename> (last n lines)

Find files/directories
find . -name "filename"

Search file contents
grep "pattern" <filename>
grep -r "pattern" . (recursive search in current directory)

Check disk usage
df -h (disk space)
du -h (directory size)

Process management
ps aux (list all processes)
top (interactive process viewer)
kill <process_id>

File permissions
chmod <permissions> <filename>
chown <user>:<group> <filename>

Network
ping <host>
ifconfig or ip addr (network interfaces)
netstat -tuln (active ports)

System information
uname -a (system info)
free -h (memory usage)
