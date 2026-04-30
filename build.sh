if [ ! -f blacklist.json ]; then
    echo "[]" > blacklist.json
fi
docker compose up --build -d