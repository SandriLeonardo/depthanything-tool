# depthanything-tool

Minimal Docker tool to convert any image to a depth map PNG using **Depth Anything V2** (HuggingFace).

## Structure

```
depthanything-tool/
  Dockerfile                  # Container definition (CPU by default)
  docker-compose-win32.yaml   # Compose for Windows (Docker Desktop)
  docker-compose-unix86.yaml  # Compose for Linux / WSL2
  run_depth.py                # Inference script
  requirements.txt
  input/                      # Drop your image here
  output/                     # Depth PNG appears here
```

## Quick start

### Windows (Docker Desktop)

```bat
docker compose -f docker-compose-win32.yaml build
```

Place your image in `input\photo.jpg`, then:

```bat
docker compose -f docker-compose-win32.yaml run --rm depth ^
  --input /data/input/photo.jpg ^
  --output /data/output/depth.png ^
  --model small
```

### Linux / WSL2

```bash
docker compose -f docker-compose-unix86.yaml build
docker compose -f docker-compose-unix86.yaml run --rm depth \
  --input /data/input/photo.jpg \
  --output /data/output/depth.png \
  --model small
```

## Model sizes

| Flag     | Model                              | Speed  | Quality |
|----------|------------------------------------|--------|---------|
| `small`  | Depth-Anything-V2-Small-hf (default) | fast | good    |
| `base`   | Depth-Anything-V2-Base-hf          | medium | better  |
| `large`  | Depth-Anything-V2-Large-hf         | slow   | best    |

The model is downloaded on first run and cached in the `hf_cache` Docker volume — no re-download on subsequent runs.

## GPU support

Uncomment the `deploy` block in the compose file and ensure:
- **Windows**: WSL2 backend enabled in Docker Desktop + `nvidia-container-toolkit` installed inside WSL2
- **Linux**: `nvidia-container-toolkit` installed on the host

Then remove or comment out `CUDA_VISIBLE_DEVICES=` from the environment section.
