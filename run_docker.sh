echo killing old docker processes
/Counting-pixels/docker-compose rm -fs

echo building docker containers
/Counting-pixels/docker-compose up --build -d

