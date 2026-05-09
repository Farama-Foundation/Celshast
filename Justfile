default:
    @just --list

serve host="0.0.0.0" port="8000":
    uvx nox -s docs-live -- --host {{host}} --port {{port}}

build:
    uvx nox -s docs

lint:
    uvx nox -s lint
