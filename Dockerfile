FROM cgr.dev/chainguard/go:1.20 as build

WORKDIR /work

ADD go.mod .
ADD go.sum .
ADD api api
ADD pkg pkg
ADD api/models.toml .
RUN env
RUN GOOS=linux GOARCH=amd64  CGO_ENABLED=0 go build -ldflags '-extldflags "-static"' -o app api/main.go

FROM cgr.dev/chainguard/static:latest
COPY --from=build /work/app /app
COPY api/models.toml .

EXPOSE 8080
CMD ["/app"]