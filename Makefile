# This Makefile helps with the automation of common tasks 
# realted to the development and running of a web application

# TARGETS: The set of tasks that can be executed in the terminal 

# tells make that css-build, run, and watch-css are not files; they're phony targets
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

