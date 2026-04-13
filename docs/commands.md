# Commands

## Build the image (once, or after any file change)

```bat
docker compose -f docker-compose-win32.yaml build
```

---

## Run — process a single image (recommended)

Drop your photo into the `input\` folder, then:

```bat
docker compose -f docker-compose-win32.yaml run --rm depth --input /data/input/IMG_1234.heic --output /data/output/depth.png
```

The result appears in `output\depth.png` on your Windows machine.

### Change model size

```bat
docker compose -f docker-compose-win32.yaml run --rm depth --input /data/input/photo.jpg --output /data/output/depth.png --model large
```

| `--model` | Speed  | Quality |
|-----------|--------|---------|
| `small`   | fast   | good    |
| `base`    | medium | better  |
| `large`   | slow   | best    |

---

## Run — open an interactive shell inside the container

```bat
docker compose -f docker-compose-win32.yaml run --rm --entrypoint bash depth
```

Then inside the container:

```bash
python run_depth.py --input /data/input/photo.heic --output /data/output/depth.png --model small
```

---

## Supported input formats

JPEG, PNG, WebP, BMP, TIFF, HEIC/HEIF — no manual conversion needed.

---

## Run — arbitrary path (image anywhere on disk)

Mount the folder containing your image directly as `/data`.
The depth map is written back into the same folder.

```bash
docker run --rm \
  -v "C:/path/to/YOUR_FOLDER:/data" \
  -v depthanything-tool_hf_cache:/cache/huggingface \
  -e HF_HOME=/cache/huggingface -e CUDA_VISIBLE_DEVICES= \
  depthanything-tool \
  --input //data/YOUR_IMAGE.png \
  --output //data/YOUR_IMAGE_DEPTH.png \
  --model small
```

Example — process an image from the portfolio assets folder:

```bash
docker run --rm \
  -v "C:/Users/leosa/Documents/università/curriculum/portfolio/assets:/data" \
  -v depthanything-tool_hf_cache:/cache/huggingface \
  -e HF_HOME=/cache/huggingface -e CUDA_VISIBLE_DEVICES= \
  depthanything-tool \
  --input //data/about-modified.png \
  --output //data/about-modified_DEPTH.png \
  --model small
```

> **Git Bash path mangling:** container-side paths starting with `/` get expanded
> to `C:/Program Files/Git/...` by Git Bash. Use `//data/...` (double slash) to
> prevent this. Host paths in `-v` (left of `:`) must use forward slashes.

> If `depthanything-tool_hf_cache` is not found, run `docker volume ls` to confirm
> the exact volume name (Docker prefixes the compose project name).

---

## Notes

- `/data/input/` inside the container maps to `input\` on Windows (compose workflow).
- When using `docker run` with `:/data`, input and output share the same host folder.
- The HuggingFace model is cached in a Docker named volume (`hf_cache`) — it is only downloaded once.
- `--rm` removes the container after it exits, keeping Docker clean.
