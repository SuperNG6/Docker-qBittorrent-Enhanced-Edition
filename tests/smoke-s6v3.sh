#!/usr/bin/env bash
set -Eeuo pipefail

image=${1:?usage: smoke-s6v3.sh IMAGE PLATFORM SERVICE}
platform=${2:?platform is required}
service=${3:?s6 service directory name is required}
container="qbittorrent-s6v3-smoke-$$"
service_dir="/var/run/s6/services/$service"

cleanup() {
    local status=$?
    if ((status != 0)); then
        docker logs --tail 80 "$container" >&2 || true
    fi
    docker rm -fv "$container" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker run -d --name "$container" --platform "$platform" --network none \
    -e PUID=1234 -e PGID=1235 -e UT=false \
    -e WEBUI_PORT=18080 -e WEBUIPORT=18080 \
    "$image" >/dev/null

wait_for_webui() {
    local previous_pid=${1:-} pid
    for _ in {1..60}; do
        pid=$(docker exec "$container" s6-svstat -o pid "$service_dir" 2>/dev/null || true)
        if [[ $pid =~ ^[1-9][0-9]*$ && $pid != "$previous_pid" ]] &&
            docker exec "$container" curl -fsS --max-time 2 http://127.0.0.1:18080/ >/dev/null 2>&1; then
            printf '%s\n' "$pid"
            return
        fi
        sleep 1
    done
    echo "WebUI failed to become ready for $platform" >&2
    return 1
}

pid=$(wait_for_webui)
[[ $(docker exec "$container" stat -c '%u:%g' /config) == 1234:1235 ]]
[[ $(docker exec "$container" stat -c '%u:%g' /downloads) == 1234:1235 ]]
[[ $(docker exec "$container" awk '/^Uid:/ {print $2}' "/proc/$pid/status") == 1234 ]]
[[ $(docker exec "$container" awk '/^Gid:/ {print $2}' "/proc/$pid/status") == 1235 ]]
docker exec --user abc "$container" test -w /config/qBittorrent/config/qBittorrent.conf
docker exec "$container" s6-svc -r "$service_dir"
replacement_pid=$(wait_for_webui "$pid")

docker stop --time 30 "$container" >/dev/null
[[ $(docker inspect --format '{{.State.ExitCode}}' "$container") == 0 ]]
printf '%s %s: WebUI, ownership, s6 restart (%s -> %s), and shutdown passed\n' \
    "$image" "$platform" "$pid" "$replacement_pid"
