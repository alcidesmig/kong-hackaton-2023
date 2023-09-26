FROM golang:alpine as build

RUN apk add --no-cache git
WORKDIR /build

# Download dependencies
COPY go.mod .
COPY go.sum .
RUN go mod download

# Build the project
COPY . .
RUN go build -o . .

FROM alpine:latest as runner

RUN apk add ca-certificates

COPY --from=build /build/ecommerce /opt/ecommerce

ENTRYPOINT ["/opt/ecommerce"]
