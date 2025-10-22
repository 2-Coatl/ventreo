# Multi-stage entrypoint for SecurityRAT allowing image pinning at build time.
ARG SECURITYRAT_IMAGE=securityrat/securityrat:latest
FROM ${SECURITYRAT_IMAGE}

# No additional layers are required; this Dockerfile exists so docker compose can
# build a local image even when the upstream tag needs to be overridden via the
# SECURITYRAT_IMAGE build argument.
