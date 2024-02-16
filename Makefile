.PHONY: css-build run watch-css

# Build the CSS using TailwindCSS
css-build:
	tailwindcss -i static/css/styles.css -o static/css/output.css --minify

# Watch the CSS for changes with TailwindCSS
watch-css:
	tailwindcss -i static/css/styles.css -o static/css/output.css --watch

# Run the Go server
run:
	python3 app.py

